"""
Auto-updater para Netpoint Reports. Suporta Windows e macOS.

Fluxo Windows:
1. Consulta version.json no GitHub
2. Compara com versão atual
3. Se nova versão disponível, pergunta ao usuário
4. Baixa novo .exe para %TEMP%
5. Escreve script .bat que substitui o exe após o app fechar
6. Executa o .bat e encerra o app

Fluxo macOS:
1-3. Igual ao Windows
4. Baixa novo .dmg para /tmp
5. Monta o DMG, copia o .app sobre o atual
6. Escreve script .sh que aguarda o processo, substitui e relança
7. Executa o .sh e encerra o app
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

VERSION_URL = (
    "https://raw.githubusercontent.com/fernandokolmar/"
    "netpoint-report-generator/main/version.json"
)

CHECK_TIMEOUT = 5


def _get_platform() -> str:
    """Retorna 'windows' ou 'macos'."""
    if sys.platform == 'darwin':
        return 'macos'
    return 'windows'


def _resolve_download_url(url_field) -> str:
    """
    Extrai a URL correta para a plataforma atual.
    url_field pode ser string (legado) ou dict {'windows': ..., 'macos': ...}.
    """
    if isinstance(url_field, dict):
        platform = _get_platform()
        return url_field.get(platform, url_field.get('windows', ''))
    return url_field or ''


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
            url_field = data.get('download_url', '')
            download_url = _resolve_download_url(url_field)

            if not latest or not download_url:
                logger.warning("version.json inválido ou sem URL para esta plataforma")
                return

            if not Version(latest) > Version(current_version):
                logger.info(f"Versão atual ({current_version}) está atualizada")
                return

            history = data.get('history', [])
            notes = []
            for entry in history:
                v = entry.get('version', '')
                entry_notes = entry.get('notes', [])
                if v and entry_notes and Version(v) > Version(current_version):
                    notes.append({'version': v, 'notes': [str(n) for n in entry_notes if n]})

            if not notes:
                notes_raw = data.get('release_notes', [])
                if isinstance(notes_raw, str):
                    notes_raw = [notes_raw] if notes_raw else []
                notes = [{'version': latest, 'notes': [str(n) for n in notes_raw if n]}]

            logger.info(f"Nova versão disponível: {latest} (plataforma: {_get_platform()})")
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
    on_done: Optional[Callable[[], None]] = None,
    on_error: Optional[Callable[[str], None]] = None
) -> None:
    """
    Baixa o novo executável e aplica a atualização.
    Detecta a plataforma e usa o método correto (bat no Windows, sh no macOS).
    on_done: chamado na thread principal quando a substituição foi concluída.
    """
    if _get_platform() == 'macos':
        _download_and_apply_macos(download_url, current_exe, on_progress, on_done, on_error)
    else:
        _download_and_apply_windows(download_url, current_exe, on_progress, on_done, on_error)


def _download_file(url, dest: str,
                   on_progress: Optional[Callable[[int], None]]) -> int:
    """Baixa url para dest, reportando progresso. Retorna bytes baixados."""
    # Defesa: garante que url é string mesmo se vier como dict
    url = _resolve_download_url(url)
    if not url:
        raise ValueError("URL de download não disponível para esta plataforma")
    req = urllib.request.urlopen(url, timeout=120)
    total = int(req.headers.get('Content-Length', 0))
    downloaded = 0
    chunk_size = 65536

    with open(dest, 'wb') as f:
        while True:
            chunk = req.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)
            downloaded += len(chunk)
            if total and on_progress:
                on_progress(int(downloaded / total * 100))

    if on_progress:
        on_progress(100)
    return downloaded


def _download_and_apply_windows(
    download_url: str,
    current_exe: str,
    on_progress: Optional[Callable[[int], None]],
    on_done: Optional[Callable[[], None]],
    on_error: Optional[Callable[[str], None]]
) -> None:
    def _run():
        logger = get_logger()
        try:
            tmp_dir = tempfile.gettempdir()
            tmp_exe = os.path.join(tmp_dir, "NetpointReports_update.exe")
            bat_path = os.path.join(tmp_dir, "netpoint_update.bat")

            logger.info(f"[Windows] Baixando de {download_url}")
            downloaded = _download_file(download_url, tmp_exe, on_progress)
            logger.info(f"Download concluído: {downloaded} bytes")

            if os.path.getsize(tmp_exe) < 1_000_000:
                raise ValueError("Arquivo baixado parece corrompido (muito pequeno)")

            # sys._MEIPASS aponta para a pasta _MEI que este processo está usando.
            # Aguardamos ela desaparecer antes de relançar — determinístico, sem delay fixo.
            mei_path = getattr(sys, '_MEIPASS', '')
            logger.info(f"Pasta _MEI monitorada pelo bat: {mei_path!r}")

            bat_content = f"""@echo off
setlocal

set "NEW_EXE={tmp_exe}"
set "CUR_EXE={current_exe}"
set "TARGET_PID={os.getpid()}"
set "MEI_PATH={mei_path}"

rem --- 1. Aguarda o processo principal encerrar ---
:waitloop
tasklist /FI "PID eq %TARGET_PID%" 2>NUL | find /I "%TARGET_PID%" >NUL
if not errorlevel 1 (
    timeout /t 1 /nobreak >NUL
    goto waitloop
)

rem --- 2. Aguarda a pasta _MEI ser deletada pelo bootloader (max 30s) ---
set WAIT_COUNT=0
:meiloop
if "%MEI_PATH%"=="" goto mei_done
if not exist "%MEI_PATH%" goto mei_done
set /a WAIT_COUNT+=1
if %WAIT_COUNT% geq 30 goto mei_done
timeout /t 1 /nobreak >NUL
goto meiloop
:mei_done

rem --- 3. Substitui o executável ---
move /Y "%NEW_EXE%" "%CUR_EXE%" >NUL 2>&1
if errorlevel 1 (
    copy /Y "%NEW_EXE%" "%CUR_EXE%" >NUL 2>&1
    if errorlevel 1 (
        echo Falha ao substituir o executavel. Tente manualmente.
        pause
        exit /b 1
    )
    del "%NEW_EXE%" >NUL 2>&1
)

rem --- 4. NÃO relança automaticamente ---
rem O PyInstaller onefile extrai DLLs para %TEMP% na inicialização.
rem Relançar imediatamente causa conflito com antivírus/sistema ainda
rem liberando a pasta _MEI anterior. O usuário reabre manualmente.
del "%~f0"
endlocal
"""
            with open(bat_path, 'w', encoding='utf-8') as f:
                f.write(bat_content)

            logger.info(f"Script Windows escrito em: {bat_path}")
            subprocess.Popen(
                ['cmd.exe', '/c', bat_path],
                creationflags=subprocess.CREATE_NO_WINDOW,
                close_fds=True
            )
            logger.info("Script de substituição iniciado — fechando app")

            # Notifica UI antes de fechar (on_done roda na thread principal via after)
            if on_done:
                on_done()

            # Pequena pausa para a UI exibir a mensagem antes de fechar
            import time
            time.sleep(2)
            os._exit(0)

        except Exception as e:
            logger.exception(f"Erro durante atualização Windows: {e}")
            if on_error:
                on_error(str(e))

    threading.Thread(target=_run, daemon=True).start()


def _download_and_apply_macos(
    download_url: str,
    current_exe: str,
    on_progress: Optional[Callable[[int], None]],
    on_done: Optional[Callable[[], None]],
    on_error: Optional[Callable[[str], None]]
) -> None:
    def _run():
        logger = get_logger()
        tmp_dmg = None
        mount_point = None
        try:
            tmp_dir = tempfile.gettempdir()
            tmp_dmg = os.path.join(tmp_dir, "NetpointReports_update.dmg")
            sh_path = os.path.join(tmp_dir, "netpoint_update.sh")
            mount_point = os.path.join(tmp_dir, "NetpointUpdate_mnt")

            logger.info(f"[macOS] Baixando DMG de {download_url}")
            downloaded = _download_file(download_url, tmp_dmg, on_progress)
            logger.info(f"Download concluído: {downloaded} bytes")

            if os.path.getsize(tmp_dmg) < 1_000_000:
                raise ValueError("DMG baixado parece corrompido (muito pequeno)")

            # O .app está dentro do bundle — current_exe aponta para o binário
            # Precisamos do caminho do .app (3 níveis acima do binário em Contents/MacOS/)
            # ex: /Applications/Netpoint Report Generator.app/Contents/MacOS/Netpoint Report Generator
            app_path = current_exe
            for _ in range(3):
                parent = os.path.dirname(app_path)
                if parent == app_path:
                    break
                app_path = parent
                if app_path.endswith('.app'):
                    break

            logger.info(f"App path: {app_path}")
            app_dir = os.path.dirname(app_path)
            app_name = os.path.basename(app_path)

            sh_content = f"""#!/bin/bash
set -e

MOUNT_POINT="{mount_point}"
TMP_DMG="{tmp_dmg}"
APP_DIR="{app_dir}"
APP_NAME="{app_name}"
TARGET_PID={os.getpid()}
CUR_EXE="{current_exe}"

# Aguarda o processo encerrar
while kill -0 "$TARGET_PID" 2>/dev/null; do
    sleep 1
done

# Aguarda PyInstaller limpar arquivos temporários
sleep 3

# Monta o DMG
mkdir -p "$MOUNT_POINT"
hdiutil attach "$TMP_DMG" -mountpoint "$MOUNT_POINT" -nobrowse -quiet

# Copia o novo .app sobre o antigo (rsync preserva permissões)
rsync -a --delete "$MOUNT_POINT/$APP_NAME/" "$APP_DIR/$APP_NAME/"

# Desmonta o DMG e limpa
hdiutil detach "$MOUNT_POINT" -quiet || true
rm -f "$TMP_DMG"
rmdir "$MOUNT_POINT" 2>/dev/null || true

# Relança o app
open "$APP_DIR/$APP_NAME"

# Remove este script
rm -f "$0"
"""
            with open(sh_path, 'w') as f:
                f.write(sh_content)
            os.chmod(sh_path, 0o755)

            logger.info(f"Script macOS escrito em: {sh_path}")
            subprocess.Popen(
                ['/bin/bash', sh_path],
                close_fds=True,
                start_new_session=True
            )
            logger.info("Script macOS iniciado — encerrando app")
            os._exit(0)

        except Exception as e:
            logger.exception(f"Erro durante atualização macOS: {e}")
            # Limpeza em caso de erro
            try:
                if mount_point and os.path.exists(mount_point):
                    subprocess.run(['hdiutil', 'detach', mount_point, '-quiet'],
                                   capture_output=True)
                if tmp_dmg and os.path.exists(tmp_dmg):
                    os.remove(tmp_dmg)
            except Exception:
                pass
            if on_error:
                on_error(str(e))

    threading.Thread(target=_run, daemon=True).start()


def get_current_exe() -> str:
    """
    Retorna o caminho do executável atual.
    Funciona tanto rodando como .app/.exe (PyInstaller) quanto como script .py.
    """
    if getattr(sys, 'frozen', False):
        return sys.executable
    else:
        return os.path.abspath(sys.argv[0])


def is_running_as_exe() -> bool:
    """Retorna True se rodando como executável compilado (PyInstaller)."""
    return getattr(sys, 'frozen', False)
