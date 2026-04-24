"""
Auto-updater para Netpoint Report Generator.

Fluxo:
1. Consulta version.json no GitHub
2. Compara com versão atual
3. Se nova versão disponível, pergunta ao usuário
4. Baixa novo .exe para %TEMP%
5. Escreve script .bat que substitui o exe após o app fechar
6. Executa o .bat e encerra o app
"""

import os
import sys
import json
import threading
import tempfile
import subprocess
import urllib.request
import urllib.error
from typing import Optional, Callable
from packaging.version import Version

from utils.logger import get_logger

# URL do arquivo version.json no GitHub (branch main, raw)
VERSION_URL = (
    "https://raw.githubusercontent.com/fernandokolmar/"
    "netpoint-report-generator/main/version.json"
)

# Timeout para a checagem de versão (segundos)
CHECK_TIMEOUT = 5


def check_for_updates(
    current_version: str,
    on_update_available: Callable[[str, str, list], None],
    silent_on_error: bool = True
) -> None:
    """
    Verifica atualizações em background. Não bloqueia a UI.

    Args:
        current_version: Versão instalada (ex: '1.7.0')
        on_update_available: Callback chamado na thread principal quando há
                             nova versão. Recebe (nova_versao, download_url, release_notes).
        silent_on_error: Se True, ignora erros de rede silenciosamente.
    """
    def _check():
        logger = get_logger()
        try:
            logger.info(f"Verificando atualizações em {VERSION_URL}")
            req = urllib.request.urlopen(VERSION_URL, timeout=CHECK_TIMEOUT)
            data = json.loads(req.read().decode('utf-8'))

            latest = data.get('version', '')
            download_url = data.get('download_url', '')

            if not latest or not download_url:
                logger.warning("version.json inválido ou incompleto")
                return

            if not Version(latest) > Version(current_version):
                logger.info(f"Versão atual ({current_version}) está atualizada")
                return

            # Montar notas cumulativas: apenas versões > current_version, ordem decrescente
            history = data.get('history', [])
            notes = []
            for entry in history:
                v = entry.get('version', '')
                entry_notes = entry.get('notes', [])
                if v and entry_notes and Version(v) > Version(current_version):
                    notes.append({'version': v, 'notes': [str(n) for n in entry_notes if n]})

            # Fallback: se não há histórico, usa release_notes antigo
            if not notes:
                notes_raw = data.get('release_notes', [])
                if isinstance(notes_raw, str):
                    notes_raw = [notes_raw] if notes_raw else []
                notes = [{'version': latest, 'notes': [str(n) for n in notes_raw if n]}]

            logger.info(f"Nova versão disponível: {latest} ({len(notes)} versões de novidades)")
            on_update_available(latest, download_url, notes)

        except Exception as e:
            if not silent_on_error:
                raise
            logger.info(f"Verificação de atualização ignorada: {e}")

    thread = threading.Thread(target=_check, daemon=True)
    thread.start()


def download_and_apply(
    download_url: str,
    current_exe: str,
    on_progress: Optional[Callable[[int], None]] = None,
    on_error: Optional[Callable[[str], None]] = None
) -> None:
    """
    Baixa o novo executável e aplica a atualização via script .bat.

    Executado em thread separada para não bloquear a UI.

    Args:
        download_url: URL do novo .exe
        current_exe: Caminho completo do executável atual
        on_progress: Callback com percentual de download (0-100)
        on_error: Callback em caso de erro (recebe mensagem)
    """
    def _download():
        logger = get_logger()
        try:
            # Baixar para arquivo temporário
            tmp_dir = tempfile.gettempdir()
            tmp_exe = os.path.join(tmp_dir, "NetpointReportGenerator_update.exe")
            bat_path = os.path.join(tmp_dir, "netpoint_update.bat")

            logger.info(f"Baixando atualização de {download_url}")
            logger.info(f"Destino temporário: {tmp_exe}")

            req = urllib.request.urlopen(download_url, timeout=60)
            total = int(req.headers.get('Content-Length', 0))
            downloaded = 0
            chunk_size = 65536  # 64 KB

            with open(tmp_exe, 'wb') as f:
                while True:
                    chunk = req.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total and on_progress:
                        pct = int(downloaded / total * 100)
                        on_progress(pct)

            if on_progress:
                on_progress(100)

            logger.info(f"Download concluído: {downloaded} bytes")

            # Verificar que o arquivo baixado tem tamanho razoável (> 1 MB)
            if os.path.getsize(tmp_exe) < 1_000_000:
                raise ValueError("Arquivo baixado parece corrompido (muito pequeno)")

            # Escrever script .bat que:
            # 1. Aguarda o processo atual terminar (loop até não existir)
            # 2. Aguarda 3s extras para o PyInstaller limpar a pasta _MEI
            # 3. Move/copia o novo exe sobre o antigo
            # 4. Relança o app e aguarda sua inicialização completa
            # 5. Se deleta
            bat_content = f"""@echo off
setlocal

set "NEW_EXE={tmp_exe}"
set "CUR_EXE={current_exe}"
set "TARGET_PID={os.getpid()}"

:waitloop
tasklist /FI "PID eq %TARGET_PID%" 2>NUL | find /I "%TARGET_PID%" >NUL
if not errorlevel 1 (
    timeout /t 1 /nobreak >NUL
    goto waitloop
)

rem Aguarda o PyInstaller terminar de limpar a pasta _MEI
timeout /t 3 /nobreak >NUL

rem Tenta mover (renomeia atomicamente se na mesma unidade)
move /Y "%NEW_EXE%" "%CUR_EXE%" >NUL 2>&1
if errorlevel 1 (
    rem Fallback para copy se move falhar (unidades diferentes)
    copy /Y "%NEW_EXE%" "%CUR_EXE%" >NUL 2>&1
    if errorlevel 1 (
        echo Falha ao substituir o executavel. Tente manualmente.
        pause
        exit /b 1
    )
    del "%NEW_EXE%" >NUL 2>&1
)

start "" "%CUR_EXE%"
del "%~f0"
endlocal
"""
            with open(bat_path, 'w', encoding='utf-8') as f:
                f.write(bat_content)

            logger.info(f"Script de atualização escrito em: {bat_path}")

            # Executar o bat em background (janela oculta)
            subprocess.Popen(
                ['cmd.exe', '/c', bat_path],
                creationflags=subprocess.CREATE_NO_WINDOW,
                close_fds=True
            )

            logger.info("Script de atualização iniciado — encerrando app")

            # Encerrar o app atual (o bat vai relançar após substituir)
            os._exit(0)

        except Exception as e:
            logger.exception(f"Erro durante atualização: {e}")
            if on_error:
                on_error(str(e))

    thread = threading.Thread(target=_download, daemon=True)
    thread.start()


def get_current_exe() -> str:
    """
    Retorna o caminho do executável atual.
    Funciona tanto rodando como .exe (PyInstaller) quanto como script .py.
    """
    if getattr(sys, 'frozen', False):
        # Rodando como executável PyInstaller
        return sys.executable
    else:
        # Rodando como script Python — retorna o script principal
        return os.path.abspath(sys.argv[0])


def is_running_as_exe() -> bool:
    """Retorna True se rodando como executável compilado (PyInstaller)."""
    return getattr(sys, 'frozen', False)
