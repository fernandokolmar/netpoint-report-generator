# 🎨 SPRINT 2 - USABILIDADE

**Objetivo**: Melhorar experiência do usuário com features de produtividade e interface moderna
**Duração**: 10 dias (Sprint 2)
**Prioridade**: 🟡 Alta
**Dependência**: Sprint 1 (Concluída ✅)

---

## 📋 VISÃO GERAL

Agora que temos uma base sólida e confiável (Sprint 1), vamos focar na experiência do usuário, tornando a aplicação mais produtiva, intuitiva e agradável de usar.

### Objetivo da Sprint
Transformar uma aplicação funcional em uma ferramenta **profissional** e **produtiva** através de:
- Preview de dados antes do processamento
- Histórico e atalhos para arquivos frequentes
- Validação em tempo real
- Interface moderna e configurável
- Feedback detalhado de progresso

---

## 📊 RESUMO DAS TAREFAS

| ID | Tarefa | Prioridade | Esforço | Status |
|----|--------|------------|---------|--------|
| S2-01 | Preview de dados (primeiras linhas) | 🟡 | 1.5 dias | ⏳ Pendente |
| S2-02 | Histórico de arquivos recentes | 🟡 | 1 dia | ⏳ Pendente |
| S2-03 | Drag & drop de arquivos | 🟢 | 1 dia | ⏳ Pendente |
| S2-04 | Validação em tempo real | 🟡 | 1.5 dias | ⏳ Pendente |
| S2-05 | Logs salvos em arquivo | 🟢 | 0.5 dia | ⏳ Pendente |
| S2-06 | Configurações persistentes | 🟡 | 1 dia | ⏳ Pendente |
| S2-07 | Indicador de progresso detalhado | 🟡 | 1.5 dias | ⏳ Pendente |
| S2-08 | Modo dark/light (temas) | 🟢 | 1 dia | ⏳ Pendente |
| S2-09 | Atalhos de teclado | 🟢 | 0.5 dia | ⏳ Pendente |
| S2-10 | Estatísticas de processamento | 🟢 | 0.5 dia | ⏳ Pendente |

**Total**: 10 tarefas, ~10 dias

---

## 📝 DETALHAMENTO DAS TAREFAS

### S2-01: Preview de Dados
**Prioridade**: 🟡 Alta
**Esforço**: 1.5 dias
**Responsável**: Frontend Dev

**Objetivo**: Permitir visualizar primeiras linhas dos CSVs antes de processar

**Problema Atual**:
- Usuário não sabe se selecionou arquivo correto até processar tudo
- Processamento pode levar minutos apenas para descobrir arquivo errado

**Solução**:

**Interface**:
```python
# Adicionar botão "Preview" ao lado de cada campo de arquivo
# Adicionar janela modal com Treeview mostrando dados

class PreviewWindow:
    def __init__(self, parent, df: pd.DataFrame, title: str):
        self.window = tk.Toplevel(parent)
        self.window.title(f"Preview: {title}")
        self.window.geometry("800x400")

        # Criar Treeview
        self.tree = ttk.Treeview(self.window)

        # Configurar colunas (primeiras 10)
        columns = df.columns[:10].tolist()
        self.tree['columns'] = columns

        # Adicionar dados (primeiras 100 linhas)
        for idx, row in df.head(100).iterrows():
            values = [str(row[col])[:50] for col in columns]
            self.tree.insert('', 'end', values=values)

        # Mostrar estatísticas
        stats_frame = ttk.Frame(self.window)
        ttk.Label(stats_frame,
                 text=f"Total: {len(df):,} linhas × {len(df.columns)} colunas"
        ).pack()
```

**Backend** (já existe):
```python
# Usar método existente do controller
preview_df = controller.load_data({'inscritos': file_path})
preview = controller.get_preview_data('inscritos', num_rows=100)
```

**Critérios de Aceitação**:
- [ ] Botão "Preview" ao lado de cada campo de arquivo
- [ ] Janela modal mostra primeiras 100 linhas
- [ ] Mostra primeiras 10 colunas (se houver mais)
- [ ] Exibe estatísticas: total de linhas/colunas
- [ ] Preview não bloqueia seleção de outros arquivos
- [ ] Preview pode ser fechado e reaberto

**Benefícios**:
- ✅ Confirma arquivo correto antes de processar
- ✅ Identifica problemas de formato visualmente
- ✅ Economiza tempo (não precisa processar tudo para ver erro)

---

### S2-02: Histórico de Arquivos Recentes
**Prioridade**: 🟡 Alta
**Esforço**: 1 dia
**Responsável**: Backend Dev

**Objetivo**: Lembrar últimos 5 conjuntos de arquivos usados

**Problema Atual**:
- Usuário precisa navegar e selecionar 4 arquivos toda vez
- Processamento frequente dos mesmos conjuntos é tedioso

**Solução**:

**Estrutura de Dados**:
```python
# Salvar em JSON
{
    "recent_sets": [
        {
            "timestamp": "2026-01-29 15:30:00",
            "name": "Evento ABC - Jan 2026",
            "files": {
                "inscritos": "C:/Data/evento_abc/inscritos.csv",
                "mensagens": "C:/Data/evento_abc/mensagens.csv",
                "relatorio_acesso": "C:/Data/evento_abc/acessos.csv",
                "totalizado": "C:/Data/evento_abc/totalizado.csv"
            }
        }
    ],
    "max_history": 5
}
```

**Interface**:
```python
# Adicionar menu "Arquivos Recentes" com submenu
menu_bar = tk.Menu(root)
recent_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Recentes", menu=recent_menu)

# Popular com histórico
for item in history.recent_sets[:5]:
    recent_menu.add_command(
        label=f"{item['name']} ({item['timestamp']})",
        command=lambda item=item: self.load_recent_set(item)
    )
```

**Módulo** (`utils/file_history.py`):
```python
class FileHistory:
    def __init__(self, config_path: str = "~/.prsa/history.json"):
        self.config_path = Path(config_path).expanduser()
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.history = self._load_history()

    def add_set(self, name: str, files: Dict[str, str]) -> None:
        """Adiciona conjunto ao histórico."""
        self.history['recent_sets'].insert(0, {
            'timestamp': datetime.now().isoformat(),
            'name': name,
            'files': files
        })
        # Manter apenas últimos 5
        self.history['recent_sets'] = self.history['recent_sets'][:5]
        self._save_history()

    def get_recent(self, limit: int = 5) -> List[Dict]:
        """Retorna conjuntos recentes."""
        return self.history['recent_sets'][:limit]
```

**Critérios de Aceitação**:
- [ ] Menu "Recentes" na barra de menu
- [ ] Mostra últimos 5 conjuntos usados
- [ ] Cada item mostra nome + timestamp
- [ ] Clicar em item carrega todos os 4 arquivos automaticamente
- [ ] Arquivos não existentes são removidos do histórico
- [ ] Histórico persiste entre sessões (salvo em JSON)

**Benefícios**:
- ✅ Carrega 4 arquivos com 1 clique
- ✅ Economia de tempo para usuários frequentes
- ✅ Reduz erros (não precisa navegar novamente)

---

### S2-03: Drag & Drop de Arquivos
**Prioridade**: 🟢 Média
**Esforço**: 1 dia
**Responsável**: Frontend Dev

**Objetivo**: Permitir arrastar arquivos diretamente para os campos

**Problema Atual**:
- Usuário precisa clicar "Procurar" e navegar
- Fluxo interrompido para selecionar cada arquivo

**Solução**:

**Implementação** (tkinterdnd2):
```python
# Instalar: pip install tkinterdnd2
from tkinterdnd2 import DND_FILES, TkinterDnD

# Usar TkinterDnD.Tk ao invés de tk.Tk
root = TkinterDnD.Tk()

# Configurar drop zone
def on_drop(event, entry_widget, file_type):
    """Callback quando arquivo é dropado."""
    file_path = event.data.strip('{}')

    # Validar extensão
    if not file_path.endswith('.csv'):
        messagebox.showerror("Erro", "Apenas arquivos CSV são permitidos")
        return

    # Atualizar campo
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, file_path)
    self.file_paths[file_type] = file_path
    self.log(f"Arquivo {file_type} dropado: {os.path.basename(file_path)}")

# Registrar cada Entry como drop target
self.inscritos_entry.drop_target_register(DND_FILES)
self.inscritos_entry.dnd_bind('<<Drop>>',
    lambda e: on_drop(e, self.inscritos_entry, 'inscritos'))
```

**Visual Feedback**:
```python
def on_drag_enter(event, entry_widget):
    """Visual feedback ao arrastar sobre campo."""
    entry_widget.config(background='#E3F2FD')  # Azul claro

def on_drag_leave(event, entry_widget):
    """Remover feedback ao sair do campo."""
    entry_widget.config(background='white')
```

**Critérios de Aceitação**:
- [ ] Cada campo Entry aceita drag & drop
- [ ] Feedback visual ao arrastar sobre campo (highlight)
- [ ] Valida extensão .csv antes de aceitar
- [ ] Atualiza campo e file_paths automaticamente
- [ ] Log mostra arquivo dropado
- [ ] Funciona em Windows, Linux, macOS

**Benefícios**:
- ✅ Fluxo mais natural e rápido
- ✅ Experiência moderna e profissional
- ✅ Reduz cliques (não precisa navegar)

---

### S2-04: Validação em Tempo Real
**Prioridade**: 🟡 Alta
**Esforço**: 1.5 dias
**Responsável**: Backend + Frontend Dev

**Objetivo**: Validar arquivos assim que são selecionados (antes de processar)

**Problema Atual**:
- Erros só aparecem ao processar (pode levar minutos)
- Usuário perde tempo descobrindo arquivo errado

**Solução**:

**Backend** (validação assíncrona):
```python
def validate_file_async(self, file_path: str, file_type: str) -> Dict[str, any]:
    """
    Valida arquivo de forma assíncrona.

    Returns:
        {
            'valid': bool,
            'errors': List[str],
            'warnings': List[str],
            'stats': {
                'rows': int,
                'columns': int,
                'size_mb': float
            }
        }
    """
    result = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'stats': {}
    }

    try:
        # Validações rápidas (sem processar tudo)
        df = self.controller.loader.load_csv(file_path)

        # Estatísticas
        result['stats'] = {
            'rows': len(df),
            'columns': len(df.columns),
            'size_mb': os.path.getsize(file_path) / (1024**2)
        }

        # Validar colunas obrigatórias
        required = REQUIRED_COLUMNS.get(file_type, [])
        missing = [col for col in required if col not in df.columns]
        if missing:
            result['valid'] = False
            result['errors'].append(f"Faltam colunas: {', '.join(missing)}")

        # Warnings
        if len(df) < 10:
            result['warnings'].append(f"Poucos registros: apenas {len(df)}")

    except Exception as e:
        result['valid'] = False
        result['errors'].append(str(e))

    return result
```

**Frontend** (indicadores visuais):
```python
# Adicionar ícones ao lado de cada campo
# ✓ verde = válido
# ⚠ amarelo = warning
# ✗ vermelho = erro

def show_validation_result(self, file_type: str, result: Dict):
    """Mostra resultado da validação visualmente."""
    # Criar label de status
    status_label = ttk.Label(files_frame)

    if result['valid']:
        if result['warnings']:
            # Amarelo com warnings
            status_label.config(text="⚠", foreground="orange")
            tooltip = f"Warnings:\n" + "\n".join(result['warnings'])
        else:
            # Verde OK
            status_label.config(text="✓", foreground="green")
            tooltip = (f"{result['stats']['rows']:,} linhas, "
                      f"{result['stats']['columns']} colunas")
    else:
        # Vermelho erro
        status_label.config(text="✗", foreground="red")
        tooltip = f"Erros:\n" + "\n".join(result['errors'])

    # Adicionar tooltip
    ToolTip(status_label, tooltip)

    # Posicionar ao lado do Entry
    status_label.grid(row=row_num, column=3, padx=5)
```

**Threading** (não bloquear UI):
```python
def on_file_selected(self, file_type: str, file_path: str):
    """Callback quando arquivo é selecionado."""
    # Validar em thread separada
    thread = threading.Thread(
        target=self._validate_and_update,
        args=(file_type, file_path),
        daemon=True
    )
    thread.start()

def _validate_and_update(self, file_type: str, file_path: str):
    """Thread de validação."""
    result = self.validate_file_async(file_path, file_type)

    # Atualizar UI na thread principal
    self.root.after(0, self.show_validation_result, file_type, result)
```

**Critérios de Aceitação**:
- [ ] Validação automática ao selecionar arquivo
- [ ] Ícones visuais: ✓ (verde), ⚠ (amarelo), ✗ (vermelho)
- [ ] Tooltip mostra detalhes ao passar mouse
- [ ] Validação não bloqueia UI (threading)
- [ ] Mostra estatísticas: linhas, colunas, tamanho
- [ ] Detecta colunas faltantes
- [ ] Warnings para arquivos suspeitos (poucos registros, etc)

**Benefícios**:
- ✅ Feedback imediato (não precisa esperar processamento)
- ✅ Identifica problemas antes de gastar tempo processando
- ✅ Estatísticas dão confiança que arquivo está correto

---

### S2-05: Logs Salvos em Arquivo
**Prioridade**: 🟢 Média
**Esforço**: 0.5 dia
**Responsável**: Backend Dev

**Objetivo**: Salvar logs de execução em arquivo para debug

**Problema Atual**:
- Logs só aparecem na UI (perdidos ao fechar)
- Difícil debugar problemas relatados por usuários

**Solução**:

**Módulo** (`utils/logger.py`):
```python
import logging
from pathlib import Path
from datetime import datetime

class PRSALogger:
    def __init__(self, log_dir: str = "~/.prsa/logs"):
        self.log_dir = Path(log_dir).expanduser()
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Arquivo de log com timestamp
        log_file = self.log_dir / f"prsa_{datetime.now():%Y%m%d_%H%M%S}.log"

        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()  # Também no console
            ]
        )

        self.logger = logging.getLogger('PRSA')

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str, exc_info=False) -> None:
        self.logger.error(message, exc_info=exc_info)

    def debug(self, message: str) -> None:
        self.logger.debug(message)
```

**Integração**:
```python
# Controller usa logger
class ReportController:
    def __init__(self, progress_callback=None):
        self.logger = PRSALogger()
        self.progress_callback = progress_callback

    def _notify(self, message: str):
        # Logar em arquivo
        self.logger.info(message)

        # Notificar UI
        if self.progress_callback:
            self.progress_callback(message)
```

**Rotação de Logs**:
```python
# Manter apenas últimos 10 arquivos de log
def cleanup_old_logs(self, keep: int = 10):
    """Remove logs antigos."""
    log_files = sorted(self.log_dir.glob("prsa_*.log"),
                      key=lambda p: p.stat().st_mtime,
                      reverse=True)

    # Deletar logs além dos últimos 10
    for log_file in log_files[keep:]:
        log_file.unlink()
```

**Critérios de Aceitação**:
- [ ] Logs salvos em `~/.prsa/logs/prsa_YYYYMMDD_HHMMSS.log`
- [ ] Formato estruturado: timestamp + nível + mensagem
- [ ] Níveis: INFO, WARNING, ERROR, DEBUG
- [ ] Exceções incluem stack trace completo
- [ ] Rotação automática (manter últimos 10 logs)
- [ ] Não impacta performance

**Benefícios**:
- ✅ Debug facilitado
- ✅ Auditoria de execuções
- ✅ Suporte técnico mais eficiente

---

### S2-06: Configurações Persistentes
**Prioridade**: 🟡 Alta
**Esforço**: 1 dia
**Responsável**: Backend Dev

**Objetivo**: Lembrar preferências do usuário entre sessões

**Problema Atual**:
- Usuário precisa reconfigurar tudo toda vez que abre app
- Sem memória de último diretório usado

**Solução**:

**Configurações** (`~/.prsa/config.json`):
```json
{
    "last_directories": {
        "inscritos": "C:/Users/user/Documents/Events",
        "mensagens": "C:/Users/user/Documents/Events",
        "relatorio_acesso": "C:/Users/user/Documents/Events",
        "totalizado": "C:/Users/user/Documents/Events",
        "output": "C:/Users/user/Documents/Reports"
    },
    "window": {
        "width": 800,
        "height": 600,
        "x": 100,
        "y": 100
    },
    "preferences": {
        "theme": "light",
        "show_preview_on_select": true,
        "auto_validate": true,
        "max_recent_files": 5
    }
}
```

**Módulo** (`utils/config_manager.py`):
```python
class ConfigManager:
    def __init__(self, config_path: str = "~/.prsa/config.json"):
        self.config_path = Path(config_path).expanduser()
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Carrega configuração ou cria default."""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return self._default_config()

    def save(self) -> None:
        """Salva configuração em disco."""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def get(self, key: str, default=None):
        """Obtém valor de configuração."""
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, default)
            if value is default:
                return default
        return value

    def set(self, key: str, value) -> None:
        """Define valor de configuração."""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value
        self.save()
```

**Integração na UI**:
```python
class VideoConferenceReportGenerator:
    def __init__(self, root):
        self.config = ConfigManager()

        # Restaurar geometria da janela
        width = self.config.get('window.width', 800)
        height = self.config.get('window.height', 600)
        x = self.config.get('window.x', 100)
        y = self.config.get('window.y', 100)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Registrar callback para salvar ao fechar
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """Salva configurações ao fechar."""
        # Salvar geometria
        geometry = self.root.geometry()
        # Formato: "800x600+100+50"
        match = re.match(r'(\d+)x(\d+)\+(\d+)\+(\d+)', geometry)
        if match:
            width, height, x, y = match.groups()
            self.config.set('window.width', int(width))
            self.config.set('window.height', int(height))
            self.config.set('window.x', int(x))
            self.config.set('window.y', int(y))

        self.root.destroy()

    def load_file(self, file_type, entry_widget):
        """Abre diálogo com último diretório usado."""
        last_dir = self.config.get(f'last_directories.{file_type}', os.getcwd())

        file_path = filedialog.askopenfilename(
            initialdir=last_dir,
            ...
        )

        if file_path:
            # Salvar diretório para próxima vez
            directory = os.path.dirname(file_path)
            self.config.set(f'last_directories.{file_type}', directory)
```

**Critérios de Aceitação**:
- [ ] Configuração salva em `~/.prsa/config.json`
- [ ] Lembra último diretório de cada tipo de arquivo
- [ ] Lembra tamanho e posição da janela
- [ ] Salva preferências do usuário (tema, etc)
- [ ] Carrega configurações ao iniciar
- [ ] Salva configurações ao fechar

**Benefícios**:
- ✅ Experiência personalizada
- ✅ Não precisa reconfigurar toda vez
- ✅ Último diretório facilita navegação

---

### S2-07: Indicador de Progresso Detalhado
**Prioridade**: 🟡 Alta
**Esforço**: 1.5 dias
**Responsável**: Frontend + Backend Dev

**Objetivo**: Mostrar progresso real (%) ao invés de barra indeterminada

**Problema Atual**:
- Barra de progresso indeterminada (não mostra % real)
- Usuário não sabe quanto falta

**Solução**:

**Backend** (reportar progresso com %):
```python
class ReportController:
    def generate_report(self, file_paths, output_path):
        """Gera relatório com callback de progresso detalhado."""
        total_steps = 3 + len(file_paths)  # load + process + generate
        current_step = 0

        # 1. Carregar arquivos (40% do tempo)
        for file_type, path in file_paths.items():
            current_step += 1
            progress_pct = (current_step / total_steps) * 40
            self._notify_progress(
                message=f"Carregando {file_type}...",
                percent=progress_pct
            )
            # ... carregar ...

        # 2. Processar dados (30% do tempo)
        current_step += 1
        self._notify_progress("Processando dados...", 40 + 30)
        # ... processar ...

        # 3. Gerar Excel (30% do tempo)
        current_step += 1
        self._notify_progress("Gerando Excel...", 70)
        # ... gerar ...

        # 4. Finalizado
        self._notify_progress("Concluído!", 100)

    def _notify_progress(self, message: str, percent: float):
        """Notifica progresso com % e mensagem."""
        if self.progress_callback:
            self.progress_callback({
                'message': message,
                'percent': percent
            })
```

**Frontend** (barra determinada + % + ETA):
```python
class VideoConferenceReportGenerator:
    def create_widgets(self):
        # Barra de progresso DETERMINADA
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='determinate',  # ← Mudança aqui
            maximum=100,
            length=600
        )

        # Label para % e ETA
        self.progress_label = ttk.Label(
            progress_frame,
            text="0% - Estimativa: --"
        )
        self.progress_label.grid(row=1, column=0, pady=5)

    def log(self, message):
        """Recebe progresso detalhado."""
        if isinstance(message, dict):
            # Progresso estruturado
            self.progress_bar['value'] = message['percent']

            # Calcular ETA
            eta = self._calculate_eta(message['percent'])
            self.progress_label.config(
                text=f"{message['percent']:.0f}% - {message['message']} - ETA: {eta}"
            )
        else:
            # Mensagem simples (backward compatible)
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
```

**ETA (Estimated Time to Arrival)**:
```python
def _calculate_eta(self, percent: float) -> str:
    """Calcula tempo estimado restante."""
    if not hasattr(self, 'start_time'):
        self.start_time = time.time()
        return "--"

    if percent == 0:
        return "--"

    elapsed = time.time() - self.start_time
    total_estimated = elapsed / (percent / 100)
    remaining = total_estimated - elapsed

    if remaining < 60:
        return f"{remaining:.0f}s"
    else:
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        return f"{minutes}m {seconds}s"
```

**Critérios de Aceitação**:
- [ ] Barra de progresso determinada (mostra % real)
- [ ] Label mostra: "X% - Mensagem - ETA: Ym Zs"
- [ ] ETA calculado dinamicamente
- [ ] Progresso reportado em 3 etapas principais:
  - Carregamento (0-40%)
  - Processamento (40-70%)
  - Geração Excel (70-100%)
- [ ] Progresso atualiza suavemente (sem pulos)

**Benefícios**:
- ✅ Usuário sabe exatamente quanto falta
- ✅ ETA permite planejar melhor o tempo
- ✅ Transparência aumenta confiança

---

### S2-08: Modo Dark/Light (Temas)
**Prioridade**: 🟢 Média
**Esforço**: 1 dia
**Responsável**: Frontend Dev

**Objetivo**: Permitir alternar entre tema claro e escuro

**Problema Atual**:
- Apenas tema claro disponível
- Pode cansar visão em ambientes escuros

**Solução**:

**Temas** (cores):
```python
THEMES = {
    'light': {
        'bg': '#FFFFFF',
        'fg': '#000000',
        'select_bg': '#0078D4',
        'select_fg': '#FFFFFF',
        'entry_bg': '#FFFFFF',
        'entry_fg': '#000000',
        'button_bg': '#E1E1E1',
        'button_fg': '#000000'
    },
    'dark': {
        'bg': '#1E1E1E',
        'fg': '#FFFFFF',
        'select_bg': '#0E639C',
        'select_fg': '#FFFFFF',
        'entry_bg': '#2D2D2D',
        'entry_fg': '#FFFFFF',
        'button_bg': '#3F3F3F',
        'button_fg': '#FFFFFF'
    }
}
```

**Aplicação de Tema**:
```python
class ThemeManager:
    def __init__(self, root, config_manager):
        self.root = root
        self.config = config_manager
        self.current_theme = self.config.get('preferences.theme', 'light')

    def apply_theme(self, theme_name: str):
        """Aplica tema na aplicação inteira."""
        theme = THEMES[theme_name]

        # Configurar estilo TTK
        style = ttk.Style()
        style.theme_use('clam')

        # Configurar cores
        style.configure('TFrame', background=theme['bg'])
        style.configure('TLabel',
                       background=theme['bg'],
                       foreground=theme['fg'])
        style.configure('TButton',
                       background=theme['button_bg'],
                       foreground=theme['button_fg'])
        style.configure('TEntry',
                       fieldbackground=theme['entry_bg'],
                       foreground=theme['entry_fg'])

        # Salvar preferência
        self.config.set('preferences.theme', theme_name)
        self.current_theme = theme_name

    def toggle_theme(self):
        """Alterna entre claro e escuro."""
        new_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.apply_theme(new_theme)
```

**Menu/Botão**:
```python
# Adicionar à barra de menu
menu_bar.add_command(label="🌙 Modo Escuro" if theme == 'light' else "☀ Modo Claro",
                    command=theme_manager.toggle_theme)

# Ou botão no canto superior direito
theme_button = ttk.Button(
    main_frame,
    text="🌙" if theme == 'light' else "☀",
    command=theme_manager.toggle_theme,
    width=3
)
theme_button.grid(row=0, column=2, sticky=tk.E)
```

**Critérios de Aceitação**:
- [ ] 2 temas disponíveis: light e dark
- [ ] Botão/menu para alternar tema
- [ ] Tema aplicado instantaneamente
- [ ] Tema salvo em configuração (persiste)
- [ ] Todos os widgets seguem o tema
- [ ] Contraste adequado (WCAG AAA)

**Benefícios**:
- ✅ Conforto visual em diferentes ambientes
- ✅ Aparência moderna e profissional
- ✅ Acessibilidade (diferentes preferências)

---

### S2-09: Atalhos de Teclado
**Prioridade**: 🟢 Média
**Esforço**: 0.5 dia
**Responsável**: Frontend Dev

**Objetivo**: Adicionar atalhos para operações comuns

**Problema Atual**:
- Apenas mouse/cliques disponíveis
- Usuários avançados querem atalhos

**Solução**:

**Atalhos Definidos**:
```python
KEYBOARD_SHORTCUTS = {
    '<Control-o>': 'open_files',        # Abrir arquivos
    '<Control-g>': 'generate_report',   # Gerar relatório
    '<Control-l>': 'clear_all',         # Limpar campos
    '<Control-q>': 'quit',              # Sair
    '<Control-p>': 'preview',           # Preview de dados
    '<Control-h>': 'show_history',      # Mostrar histórico
    '<Control-t>': 'toggle_theme',      # Alternar tema
    '<F1>': 'show_help',                # Ajuda
    '<F5>': 'refresh'                   # Atualizar
}
```

**Registro de Atalhos**:
```python
class VideoConferenceReportGenerator:
    def __init__(self, root):
        self.root = root
        self._register_shortcuts()

    def _register_shortcuts(self):
        """Registra todos os atalhos de teclado."""
        self.root.bind('<Control-o>', lambda e: self.open_files_dialog())
        self.root.bind('<Control-g>', lambda e: self.process_and_generate())
        self.root.bind('<Control-l>', lambda e: self.clear_all())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<Control-p>', lambda e: self.show_preview())
        self.root.bind('<Control-h>', lambda e: self.show_history())
        self.root.bind('<Control-t>', lambda e: self.theme_manager.toggle_theme())
        self.root.bind('<F1>', lambda e: self.show_help())
        self.root.bind('<F5>', lambda e: self.refresh())
```

**Janela de Ajuda** (F1):
```python
def show_help(self):
    """Mostra janela com atalhos disponíveis."""
    help_window = tk.Toplevel(self.root)
    help_window.title("Atalhos de Teclado")
    help_window.geometry("400x500")

    text = tk.Text(help_window, wrap=tk.WORD, padx=10, pady=10)
    text.pack(fill=tk.BOTH, expand=True)

    help_text = """
    ATALHOS DE TECLADO

    Arquivos:
    • Ctrl+O - Abrir arquivos
    • Ctrl+P - Preview de dados
    • Ctrl+H - Histórico de arquivos recentes

    Ações:
    • Ctrl+G - Gerar relatório
    • Ctrl+L - Limpar campos
    • F5 - Atualizar

    Aparência:
    • Ctrl+T - Alternar tema (claro/escuro)

    Ajuda:
    • F1 - Mostrar esta ajuda

    Sair:
    • Ctrl+Q - Sair da aplicação
    """

    text.insert('1.0', help_text)
    text.config(state='disabled')
```

**Critérios de Aceitação**:
- [ ] 9 atalhos implementados
- [ ] Atalhos funcionam globalmente na janela
- [ ] F1 mostra janela de ajuda com lista completa
- [ ] Tooltips dos botões mostram atalho correspondente
- [ ] Não conflita com atalhos do sistema operacional

**Benefícios**:
- ✅ Produtividade para usuários frequentes
- ✅ Operação sem mouse
- ✅ Experiência profissional

---

### S2-10: Estatísticas de Processamento
**Prioridade**: 🟢 Média
**Esforço**: 0.5 dia
**Responsável**: Backend Dev

**Objetivo**: Mostrar estatísticas após gerar relatório

**Problema Atual**:
- Apenas mensagem "Relatório gerado com sucesso"
- Usuário não sabe quantos registros foram processados

**Solução**:

**Backend** (coletar estatísticas):
```python
class ReportController:
    def generate_report(self, file_paths, output_path):
        """Gera relatório e retorna estatísticas."""
        start_time = time.time()

        # ... processar ...

        # Coletar estatísticas
        stats = {
            'duration_seconds': time.time() - start_time,
            'total_records': sum(len(df) for df in self.raw_dataframes.values()),
            'files_processed': len(file_paths),
            'output_size_mb': os.path.getsize(output_path) / (1024**2),
            'details': {
                'inscritos': len(self.raw_dataframes.get('inscritos', [])),
                'mensagens': len(self.raw_dataframes.get('mensagens', [])),
                'acessos': len(self.raw_dataframes.get('relatorio_acesso', [])),
                'retenção': len(self.raw_dataframes.get('totalizado', []))
            }
        }

        return output_path, stats
```

**Frontend** (mostrar estatísticas):
```python
def _on_success(self, result):
    """Mostra estatísticas de processamento."""
    output_path, stats = result

    # Parar progresso
    self.progress_bar.stop()
    self.process_button.config(state='normal')

    # Criar mensagem com estatísticas
    duration = stats['duration_seconds']
    minutes = int(duration // 60)
    seconds = int(duration % 60)

    message = f"""
Relatório gerado com sucesso!

📄 Arquivo: {os.path.basename(output_path)}
📊 Registros processados: {stats['total_records']:,}
📁 Tamanho: {stats['output_size_mb']:.2f} MB
⏱ Tempo: {minutes}m {seconds}s

Detalhes:
• Inscritos: {stats['details']['inscritos']:,}
• Mensagens: {stats['details']['mensagens']:,}
• Acessos: {stats['details']['acessos']:,}
• Retenção: {stats['details']['retenção']:,}
    """.strip()

    # Mostrar em janela customizada
    StatsWindow(self.root, message, output_path)
```

**Janela de Estatísticas** (customizada):
```python
class StatsWindow:
    def __init__(self, parent, message, output_path):
        self.window = tk.Toplevel(parent)
        self.window.title("Relatório Gerado")
        self.window.geometry("450x350")

        # Ícone de sucesso
        success_label = ttk.Label(
            self.window,
            text="✓",
            font=('Arial', 48, 'bold'),
            foreground='green'
        )
        success_label.pack(pady=20)

        # Mensagem
        text_widget = tk.Text(
            self.window,
            height=10,
            wrap=tk.WORD,
            padx=20,
            pady=10
        )
        text_widget.insert('1.0', message)
        text_widget.config(state='disabled')
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20)

        # Botões
        button_frame = ttk.Frame(self.window)
        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="Abrir Arquivo",
            command=lambda: os.startfile(output_path)
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Abrir Pasta",
            command=lambda: os.startfile(os.path.dirname(output_path))
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Fechar",
            command=self.window.destroy
        ).pack(side=tk.LEFT, padx=5)
```

**Critérios de Aceitação**:
- [ ] Estatísticas coletadas durante processamento
- [ ] Janela customizada mostra estatísticas formatadas
- [ ] Mostra: registros processados, tamanho, tempo, detalhes por tipo
- [ ] Botões: "Abrir Arquivo", "Abrir Pasta", "Fechar"
- [ ] Ícone de sucesso (✓ verde)

**Benefícios**:
- ✅ Transparência do que foi processado
- ✅ Validação visual (números esperados)
- ✅ Atalhos para abrir arquivo/pasta

---

## 📅 CRONOGRAMA

| Dia | Tarefa | Responsável |
|-----|--------|-------------|
| **Dia 1** | S2-01: Preview de dados (parte 1) | Frontend Dev |
| **Dia 2** | S2-01: Preview de dados (parte 2) | Frontend Dev |
| **Dia 3** | S2-02: Histórico de arquivos | Backend Dev |
| **Dia 4** | S2-03: Drag & drop | Frontend Dev |
| **Dia 5** | S2-04: Validação tempo real (parte 1) | Backend Dev |
| **Dia 6** | S2-04: Validação tempo real (parte 2) | Frontend Dev |
| **Dia 7** | S2-05: Logs + S2-10: Estatísticas | Backend Dev |
| **Dia 8** | S2-06: Configurações persistentes | Backend Dev |
| **Dia 9** | S2-07: Progresso detalhado + S2-09: Atalhos | Frontend Dev |
| **Dia 10** | S2-08: Temas + Testes + Review | Frontend Dev |

---

## 🎯 OBJETIVOS DE QUALIDADE

### Métricas de Sucesso

| Métrica | Meta |
|---------|------|
| Satisfação do usuário | +30% (baseado em feedback) |
| Tempo médio para gerar relatório | -20% (com histórico/atalhos) |
| Erros por usuário inexperiente | -50% (com validação tempo real) |
| Taxa de reprocessamento (arquivo errado) | -70% (com preview) |

### Definition of Done

Para cada tarefa ser considerada completa, deve:
- [ ] Código implementado e testado manualmente
- [ ] Documentação atualizada (docstrings)
- [ ] Sem regressões em funcionalidades existentes
- [ ] Interface responsiva (não trava)
- [ ] Funciona em Windows (plataforma principal)
- [ ] Code review aprovado

---

## 🚀 PREPARAÇÃO PARA SPRINT 3

Após Sprint 2, teremos:
- ✅ Base sólida (Sprint 1)
- ✅ Interface moderna e produtiva (Sprint 2)
- 🎯 Próximo foco: **Melhorias avançadas**
  - Testes automatizados
  - Exportação múltiplos formatos
  - Gráficos interativos
  - API REST
  - Documentação técnica

---

## 📋 CHECKLIST DE INÍCIO

Antes de começar Sprint 2:
- [x] Sprint 1 concluída e documentada
- [x] Arquitetura modular funcionando
- [x] Validações básicas implementadas
- [x] Threading implementado
- [ ] Instalar dependências adicionais:
  - [ ] `pip install tkinterdnd2` (drag & drop)
  - [ ] `pip install Pillow` (ícones/imagens)
- [ ] Criar branch `sprint-2` no git
- [ ] Revisar backlog de melhorias

---

**Documento criado**: 2026-01-29
**Status**: ⏳ PRONTO PARA INICIAR
**Próximo passo**: Reunião de planning + início S2-01

---

🎨 **Vamos fazer desta aplicação uma ferramenta PROFISSIONAL!**
