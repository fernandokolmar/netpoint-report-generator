# 🔴 SPRINT 1: CRÍTICO - Confiabilidade e Integridade

**Duração**: 2 semanas (10 dias úteis)
**Objetivo**: Garantir confiabilidade e integridade de dados
**Meta**: ROI -80% erros de usuário, +30% confiança nos dados

---

## 📋 BACKLOG DA SPRINT

| ID | Tarefa | Prioridade | Esforço | Status |
|----|--------|-----------|---------|--------|
| S1-01 | Separar classes (God Object → 5 classes) | 🔴 | 3 dias | ⏳ Pendente |
| S1-02 | Desacoplar UI da lógica (callbacks) | 🔴 | 2 dias | ⏳ Pendente |
| S1-03 | Validação avançada de dados | 🔴 | 2 dias | ⏳ Pendente |
| S1-04 | Tratamento de erros específicos | 🔴 | 1.5 dias | ⏳ Pendente |
| S1-05 | Adicionar type hints em todas funções | 🔴 | 1 dia | ⏳ Pendente |
| S1-06 | Adicionar docstrings em todos métodos | 🔴 | 1 dia | ⏳ Pendente |
| S1-07 | Corrigir bug: tempo médio (fórmula Excel) | 🔴 | 0.5 dia | ⏳ Pendente |
| S1-08 | Corrigir bug: validação CSV vazio | 🔴 | 0.5 dia | ⏳ Pendente |
| S1-09 | Threading + barra de progresso | 🔴 | 1.5 dias | ⏳ Pendente |
| S1-10 | Eliminar duplicação código (DRY) | 🔴 | 1 dia | ⏳ Pendente |

---

## 📝 DETALHAMENTO DAS TAREFAS

### S1-01: Separar Classes (God Object → 5 Classes)
**Prioridade**: 🔴 Crítica
**Esforço**: 3 dias
**Responsável**: Tech Lead + Backend Dev

**Objetivo**: Refatorar classe monolítica `VideoConferenceReportGenerator` em 5 classes especializadas.

**Estrutura Proposta**:

```python
# core/data_loader.py
class CSVLoader:
    """Responsável exclusivamente por carregar arquivos CSV."""
    def load_csv(self, file_path: str, encoding: str, sep: str) -> pd.DataFrame:
        pass

    def load_all(self, file_paths: Dict[str, str]) -> Dict[str, pd.DataFrame]:
        pass

# core/data_processor.py
class ReportDataProcessor:
    """Responsável exclusivamente por processar/transformar dados."""
    def process_inscritos(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    def process_relatorio_acesso(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    def process_mensagens(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    def process_totalizado(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

# core/excel_generator.py
class ExcelGenerator:
    """Responsável exclusivamente por gerar arquivos Excel."""
    def generate(self, dfs: Dict[str, pd.DataFrame], output_path: str) -> str:
        pass

    def create_retencao_sheet(self, wb: Workbook, df: pd.DataFrame) -> None:
        pass

    # ... outros métodos

# core/controller.py
class ReportController:
    """Orquestra o fluxo sem conhecer implementações."""
    def __init__(
        self,
        loader: CSVLoader,
        processor: ReportDataProcessor,
        generator: ExcelGenerator
    ):
        self.loader = loader
        self.processor = processor
        self.generator = generator

    def generate_report(
        self,
        file_paths: Dict[str, str],
        output_path: str
    ) -> str:
        dfs = self.loader.load_all(file_paths)
        processed = self.processor.process_all(dfs)
        result = self.generator.generate(processed, output_path)
        return result

# prsa_report_generator.py (UI apenas)
class VideoConferenceReportGenerator:
    """Interface gráfica Tkinter - usa ReportController."""
    def __init__(self, root):
        self.root = root

        # Injeção de dependências
        loader = CSVLoader()
        processor = ReportDataProcessor()
        generator = ExcelGenerator()
        self.controller = ReportController(loader, processor, generator)

        self.create_widgets()
```

**Critérios de Aceitação**:
- [ ] 5 classes criadas em arquivos separados
- [ ] Cada classe tem responsabilidade única
- [ ] VideoConferenceReportGenerator apenas UI
- [ ] Injeção de dependências implementada
- [ ] Todos os testes de regressão passam
- [ ] Funcionalidade idêntica à versão anterior

**Testes**:
```python
def test_separacao_classes():
    # Testar que cada classe é independente
    loader = CSVLoader()
    processor = ReportDataProcessor()
    generator = ExcelGenerator()
    controller = ReportController(loader, processor, generator)

    # Deve funcionar sem UI
    result = controller.generate_report({...}, 'output.xlsx')
    assert os.path.exists(result)
```

---

### S1-02: Desacoplar UI da Lógica (Callbacks)
**Prioridade**: 🔴 Crítica
**Esforço**: 2 dias
**Responsável**: Tech Lead

**Objetivo**: Remover chamadas diretas a `self.log()` e `messagebox` de dentro da lógica de negócio.

**Implementação**:

```python
# core/data_loader.py
class CSVLoader:
    def __init__(self, progress_callback: Optional[Callable[[str], None]] = None):
        self.progress_callback = progress_callback

    def _notify(self, message: str) -> None:
        if self.progress_callback:
            self.progress_callback(message)

    def load_all(self, file_paths: Dict[str, str]) -> Dict[str, pd.DataFrame]:
        self._notify("Carregando arquivos CSV...")
        dfs = {}

        for key, path in file_paths.items():
            self._notify(f"Carregando {key}...")
            dfs[key] = self.load_csv(path)
            self._notify(f"{key}: {len(dfs[key])} registros")

        return dfs

# prsa_report_generator.py (UI)
class VideoConferenceReportGenerator:
    def __init__(self, root):
        # ...
        # Passar callback de log para loader
        loader = CSVLoader(progress_callback=self.log)
        # ...
```

**Critérios de Aceitação**:
- [ ] Nenhuma classe em `core/` chama `messagebox` diretamente
- [ ] Nenhuma classe em `core/` chama `self.log()` diretamente
- [ ] Callbacks opcionais (funcionam sem UI)
- [ ] Possível usar classes em CLI/script
- [ ] Testes unitários sem dependência de Tkinter

**Testes**:
```python
def test_loader_sem_callback():
    # Deve funcionar sem callback
    loader = CSVLoader()  # Sem callback
    dfs = loader.load_all({...})
    assert 'inscritos' in dfs

def test_loader_com_callback():
    messages = []
    def callback(msg):
        messages.append(msg)

    loader = CSVLoader(progress_callback=callback)
    dfs = loader.load_all({...})

    assert len(messages) > 0
    assert "Carregando" in messages[0]
```

---

### S1-03: Validação Avançada de Dados
**Prioridade**: 🔴 Crítica
**Esforço**: 2 dias
**Responsável**: Backend Dev + Data Analyst

**Objetivo**: Implementar validações robustas antes de processar dados.

**Implementação**:

```python
# core/validators.py
class DataValidator:
    """Validações de qualidade de dados."""

    @staticmethod
    def validate_not_empty(df: pd.DataFrame, df_name: str) -> None:
        """Valida que DataFrame não está vazio."""
        if df.empty:
            raise EmptyDataFrameError(f"{df_name} está vazio (0 registros)")

    @staticmethod
    def validate_required_columns(
        df: pd.DataFrame,
        required: List[str],
        df_name: str
    ) -> None:
        """Valida colunas obrigatórias."""
        missing = [col for col in required if col not in df.columns]
        if missing:
            available = df.columns.tolist()
            raise MissingColumnsError(
                f"{df_name}: Colunas obrigatórias ausentes: {missing}\n"
                f"Colunas disponíveis: {available}"
            )

    @staticmethod
    def validate_phone_format(df: pd.DataFrame, col_name: str = 'Celular') -> List[str]:
        """Valida formato de celular (10-11 dígitos)."""
        if col_name not in df.columns:
            return []

        invalid = df[
            ~df[col_name].astype(str).str.match(r'^\d{10,11}$', na=False)
        ]

        if len(invalid) > 0:
            return invalid[col_name].tolist()
        return []

    @staticmethod
    def validate_date_format(
        df: pd.DataFrame,
        col_name: str,
        date_format: str = '%d/%m/%Y %H:%M:%S'
    ) -> int:
        """Valida formato de data."""
        try:
            pd.to_datetime(df[col_name], format=date_format, errors='coerce')
            invalid_count = df[col_name].isna().sum()
            return invalid_count
        except Exception as e:
            raise InvalidDateFormatError(
                f"Erro ao validar datas em '{col_name}': {e}"
            )

    @staticmethod
    def detect_duplicates(
        df: pd.DataFrame,
        subset: List[str],
        df_name: str
    ) -> pd.DataFrame:
        """Detecta registros duplicados."""
        duplicates = df[df.duplicated(subset=subset, keep=False)]
        return duplicates

    @staticmethod
    def validate_range(
        df: pd.DataFrame,
        col_name: str,
        min_val: float = 0,
        max_val: Optional[float] = None
    ) -> pd.DataFrame:
        """Valida range de valores numéricos."""
        if col_name not in df.columns:
            return pd.DataFrame()

        invalid = df[df[col_name] < min_val]

        if max_val is not None:
            invalid = pd.concat([invalid, df[df[col_name] > max_val]])

        return invalid

# core/exceptions.py
class PRSAException(Exception):
    """Exceção base do projeto."""
    pass

class EmptyDataFrameError(PRSAException):
    """DataFrame vazio."""
    pass

class MissingColumnsError(PRSAException):
    """Colunas obrigatórias ausentes."""
    pass

class InvalidDateFormatError(PRSAException):
    """Formato de data inválido."""
    pass

# core/data_loader.py
class CSVLoader:
    def load_all(self, file_paths: Dict[str, str]) -> Dict[str, pd.DataFrame]:
        self._notify("Carregando e validando arquivos...")
        dfs = {}

        for key, path in file_paths.items():
            df = self.load_csv(path)

            # Validar DataFrame não vazio
            DataValidator.validate_not_empty(df, key)

            # Validar colunas obrigatórias
            required_cols = self._get_required_columns(key)
            DataValidator.validate_required_columns(df, required_cols, key)

            # Validar formato de celular (se aplicável)
            if 'Celular' in df.columns:
                invalid_phones = DataValidator.validate_phone_format(df)
                if invalid_phones:
                    self._notify(
                        f"⚠️ {key}: {len(invalid_phones)} celulares com formato inválido"
                    )

            # Detectar duplicatas
            if key == 'inscritos' and 'Celular' in df.columns:
                duplicates = DataValidator.detect_duplicates(df, ['Celular'], key)
                if len(duplicates) > 0:
                    self._notify(
                        f"⚠️ {key}: {len(duplicates)} registros duplicados detectados"
                    )

            dfs[key] = df
            self._notify(f"✓ {key}: {len(df)} registros válidos")

        return dfs

    def _get_required_columns(self, df_type: str) -> List[str]:
        """Retorna colunas obrigatórias por tipo de DataFrame."""
        required = {
            'inscritos': ['Nome'],
            'mensagens': ['Nome'],
            'relatorio_acesso': ['Nome'],
            'totalizado': ['Data', 'Usuarios conectados']
        }
        return required.get(df_type, [])
```

**Critérios de Aceitação**:
- [ ] CSV vazio gera erro descritivo
- [ ] Colunas obrigatórias validadas antes de processar
- [ ] Formato de celular validado (10-11 dígitos)
- [ ] Formato de data validado
- [ ] Duplicatas detectadas e alertadas
- [ ] Valores negativos em "Usuarios conectados" detectados
- [ ] Mensagens de erro específicas e acionáveis
- [ ] Todas validações têm testes unitários

**Testes**:
```python
def test_validate_empty_dataframe():
    df = pd.DataFrame()
    with pytest.raises(EmptyDataFrameError):
        DataValidator.validate_not_empty(df, 'Test')

def test_validate_missing_columns():
    df = pd.DataFrame({'Nome': ['João']})
    with pytest.raises(MissingColumnsError) as exc:
        DataValidator.validate_required_columns(df, ['Nome', 'Celular'], 'Test')
    assert 'Celular' in str(exc.value)

def test_validate_phone_format():
    df = pd.DataFrame({
        'Celular': ['31999887766', '31988776655', 'invalid', '123']
    })
    invalid = DataValidator.validate_phone_format(df)
    assert len(invalid) == 2
```

---

### S1-04: Tratamento de Erros Específicos
**Prioridade**: 🔴 Crítica
**Esforço**: 1.5 dias
**Responsável**: Backend Dev

**Objetivo**: Substituir todos os `except:` genéricos por exceções específicas com logging.

**Implementação**:

```python
# Antes (RUIM):
try:
    df = pd.read_csv(file_path)
except:
    return "0:00:00"

# Depois (BOM):
try:
    df = pd.read_csv(file_path, encoding='utf-8-sig', sep=';')
except FileNotFoundError as e:
    logger.error(f"Arquivo não encontrado: {file_path}")
    raise FileNotFoundError(
        f"Arquivo não encontrado: {file_path}\n"
        f"Verifique se o caminho está correto."
    )
except PermissionError as e:
    logger.error(f"Sem permissão para ler: {file_path}")
    raise PermissionError(
        f"Sem permissão para ler: {file_path}\n"
        f"Verifique as permissões do arquivo."
    )
except UnicodeDecodeError as e:
    logger.error(f"Erro de encoding em: {file_path}")
    raise UnicodeDecodeError(
        f"Erro de codificação no arquivo: {file_path}\n"
        f"Tente salvar o arquivo como UTF-8 no Excel."
    )
except pd.errors.ParserError as e:
    logger.error(f"Erro ao parsear CSV: {file_path} - {e}")
    raise pd.errors.ParserError(
        f"Formato CSV inválido em: {file_path}\n"
        f"Verifique se o separador é ';' (ponto-e-vírgula)"
    )
except Exception as e:
    logger.exception(f"Erro inesperado ao carregar {file_path}")
    raise
```

**Locais a Corrigir**:
- Linhas 209-212 (load_dataframes)
- Linhas 266-274 (format_time)
- Linhas 280-291 (calc_time_from_dates)
- Linhas 376-380 (process_data)
- Linhas 421-425 (create_excel_file)

**Critérios de Aceitação**:
- [ ] Nenhum `except:` sem especificar exceção
- [ ] Todas exceções logadas com logger.error/exception
- [ ] Mensagens de erro específicas e acionáveis
- [ ] Contexto do erro incluído (arquivo, linha, etc)
- [ ] Sugestões de correção nas mensagens
- [ ] Testes de cada tipo de exceção

---

### S1-05 e S1-06: Type Hints e Docstrings
**Prioridade**: 🔴 Crítica
**Esforço**: 2 dias (1 dia cada)
**Responsável**: Code Reviewer + Time

**Objetivo**: Adicionar type hints e docstrings em TODAS as funções.

**Template de Docstring**:

```python
def process_inscritos(self, df: pd.DataFrame) -> pd.DataFrame:
    """
    Processa dados de inscritos normalizando colunas e selecionando campos relevantes.

    Realiza as seguintes transformações:
    - Renomeia 'Login' para 'Celular'
    - Renomeia coluna LGPD gigante
    - Seleciona colunas: Nome, Celular, Município, Comunidade, etc.

    Args:
        df: DataFrame bruto de inscritos carregado do CSV

    Returns:
        DataFrame processado com colunas normalizadas

    Raises:
        MissingColumnsError: Se colunas obrigatórias (Nome) estiverem ausentes

    Example:
        >>> df_raw = pd.read_csv('inscritos.csv', sep=';')
        >>> df_processed = processor.process_inscritos(df_raw)
        >>> print(df_processed.columns)
        ['Nome', 'Celular', 'Município', 'Comunidade']
    """
    # ... código
```

**Critérios de Aceitação**:
- [ ] 100% das funções públicas com type hints
- [ ] 100% das funções públicas com docstrings
- [ ] Docstrings seguem formato Google Style
- [ ] Parâmetros, retornos e exceções documentados
- [ ] Exemplos de uso quando apropriado
- [ ] mypy --strict passa sem erros

---

### S1-07: Corrigir Bug Tempo Médio
**Prioridade**: 🔴 Crítica
**Esforço**: 0.5 dia
**Responsável**: Data Analyst

**Problema**: Fórmula tenta fazer AVERAGE de texto (HH:MM:SS)

**Solução**:

```python
# core/data_processor.py
def process_relatorio_acesso(self, df: pd.DataFrame) -> pd.DataFrame:
    # ... código existente de cálculo de retenção

    # ADICIONAR: Coluna auxiliar numérica de tempo em minutos
    df['Tempo_Minutos'] = self._convert_time_to_minutes(df['Retenção (hh:mm)'])

    return df

def _convert_time_to_minutes(self, time_str_series: pd.Series) -> pd.Series:
    """
    Converte série de tempo HH:MM:SS para minutos (numérico).

    Args:
        time_str_series: Série com strings no formato "HH:MM:SS"

    Returns:
        Série com valores numéricos em minutos
    """
    def parse_time(time_str: str) -> float:
        if pd.isna(time_str) or time_str == "0:00:00":
            return 0.0

        try:
            parts = time_str.split(':')
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2]) if len(parts) > 2 else 0

            total_minutes = hours * 60 + minutes + seconds / 60
            return round(total_minutes, 2)
        except Exception:
            return 0.0

    return time_str_series.apply(parse_time)

# core/excel_generator.py
def create_acessos_sheet(self, wb: Workbook, df: pd.DataFrame) -> None:
    # ... código existente

    # Fórmula corrigida na planilha Retencao
    # ws['R6'] = "=Relatorio_de_acesso12[[#Totals],[Retenção (hh:mm)]]"  ❌ ANTES
    ws['R6'] = "=AVERAGE(Relatorio_de_acesso12[Tempo_Minutos])"  # ✅ DEPOIS

    # Formatar como tempo
    ws['R6'].number_format = '[h]:mm'
```

**Critérios de Aceitação**:
- [ ] Coluna "Tempo_Minutos" adicionada aos DataFrames processados
- [ ] Fórmula Excel usa AVERAGE de coluna numérica
- [ ] Resultado formatado como HH:MM
- [ ] Teste unitário validando cálculo

---

### S1-08: Corrigir Bug CSV Vazio
**Prioridade**: 🔴 Crítica
**Esforço**: 0.5 dia
**Responsável**: Backend Dev

**Já coberto por S1-03** (Validação Avançada)

---

### S1-09: Threading + Barra de Progresso
**Prioridade**: 🔴 Crítica
**Esforço**: 1.5 dias
**Responsável**: Frontend Dev

**Implementação**:

```python
# prsa_report_generator.py
import threading
from queue import Queue

class VideoConferenceReportGenerator:
    def __init__(self, root):
        # ... código existente
        self.processing = False
        self.progress_queue = Queue()
        self.create_progress_bar()

    def create_progress_bar(self):
        """Cria barra de progresso (inicialmente oculta)."""
        self.progress_frame = ttk.Frame(self.root)
        self.progress_frame.grid(row=4, column=0, columnspan=3, pady=5)
        self.progress_frame.grid_remove()  # Ocultar

        self.progress_label = ttk.Label(
            self.progress_frame,
            text="",
            font=('Arial', 10)
        )
        self.progress_label.pack()

        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='determinate',
            maximum=100,
            length=500
        )
        self.progress_bar.pack(pady=5)

        self.cancel_btn = ttk.Button(
            self.progress_frame,
            text="⛔ Cancelar",
            command=self.cancel_processing
        )
        self.cancel_btn.pack(pady=5)

    def process_and_generate(self):
        """Iniciar processamento em thread separada."""
        if not self.validate_files():
            return

        if self.processing:
            messagebox.showwarning("Aviso", "Processamento já em andamento!")
            return

        # Desabilitar botões
        self.process_btn.config(state='disabled')
        self.clear_btn.config(state='disabled')

        # Mostrar progresso
        self.progress_frame.grid()
        self.progress_bar['value'] = 0
        self.cancel_processing_flag = False

        # Iniciar thread
        thread = threading.Thread(target=self._process_worker, daemon=True)
        thread.start()

        # Monitorar progresso
        self._check_progress()

    def _process_worker(self):
        """Worker thread para processamento pesado."""
        self.processing = True
        try:
            # Progresso 0-25%
            self.progress_queue.put(('progress', 0, "Validando arquivos..."))
            if self.cancel_processing_flag:
                raise Exception("Cancelado pelo usuário")

            # Progresso 25-50%
            self.progress_queue.put(('progress', 25, "Carregando CSVs..."))
            file_paths = self.file_paths
            if self.cancel_processing_flag:
                raise Exception("Cancelado pelo usuário")

            # Carregar via controller (não UI)
            dfs = self.controller.loader.load_all(file_paths)

            # Progresso 50-75%
            self.progress_queue.put(('progress', 50, "Processando dados..."))
            if self.cancel_processing_flag:
                raise Exception("Cancelado pelo usuário")

            processed = self.controller.processor.process_all(dfs)

            # Progresso 75-100%
            self.progress_queue.put(('progress', 75, "Gerando Excel..."))
            if self.cancel_processing_flag:
                raise Exception("Cancelado pelo usuário")

            # Criar Excel (precisa estar na main thread para filedialog)
            self.progress_queue.put(('ask_save_path', None, None))

        except Exception as e:
            self.progress_queue.put(('error', None, str(e)))
        finally:
            self.processing = False

    def _check_progress(self):
        """Verifica fila de progresso (executada no thread principal)."""
        try:
            while True:
                msg_type, value, text = self.progress_queue.get_nowait()

                if msg_type == 'progress':
                    self.progress_bar['value'] = value
                    self.progress_label.config(text=text)
                    self.log(text, 'info')

                elif msg_type == 'ask_save_path':
                    # Perguntar onde salvar (main thread)
                    output_path = filedialog.asksaveasfilename(...)
                    if output_path:
                        # Continuar processamento
                        result = self.controller.generator.generate(
                            self.controller.processor.processed_dfs,
                            output_path
                        )
                        self.progress_queue.put(('done', 100, f"Salvo em: {result}"))
                    else:
                        self.progress_queue.put(('error', None, "Cancelado"))

                elif msg_type == 'done':
                    self.progress_bar['value'] = value
                    self.log(text, 'success')
                    messagebox.showinfo("Sucesso", text)
                    self._cleanup_progress()
                    return

                elif msg_type == 'error':
                    self.log(f"Erro: {text}", 'error')
                    messagebox.showerror("Erro", text)
                    self._cleanup_progress()
                    return

        except:
            # Fila vazia, verificar novamente em 100ms
            self.root.after(100, self._check_progress)

    def cancel_processing(self):
        """Cancelar processamento."""
        if messagebox.askyesno("Cancelar", "Deseja cancelar o processamento?"):
            self.cancel_processing_flag = True
            self.log("Cancelando...", 'warning')

    def _cleanup_progress(self):
        """Limpar indicadores de progresso."""
        self.progress_frame.grid_remove()
        self.process_btn.config(state='normal')
        self.clear_btn.config(state='normal')
        self.progress_bar['value'] = 0
```

**Critérios de Aceitação**:
- [ ] UI não trava durante processamento
- [ ] Barra de progresso visível e atualizada
- [ ] Progresso em 4 etapas (0%, 25%, 50%, 75%, 100%)
- [ ] Botão "Cancelar" funcional
- [ ] Logs atualizados em tempo real
- [ ] Botões desabilitados durante processamento
- [ ] Teste manual em arquivos grandes (>10k linhas)

---

### S1-10: Eliminar Duplicação Código (DRY)
**Prioridade**: 🔴 Crítica
**Esforço**: 1 dia
**Responsável**: Backend Dev

**Áreas com Duplicação**:

1. **Renomeação coluna LGPD** (3x repetido)
2. **Renomeação Login → Celular** (2x repetido)
3. **Criação de tabelas Excel** (4x repetido)
4. **Ajuste de largura colunas** (3x repetido)
5. **Seleção de colunas dinâmica** (3x repetido)

**Solução**:

```python
# config/column_mappings.py
COLUMN_RENAMES = {
    'Login': 'Celular',
    'Comunidade.1': 'Comunidade2',
    # Coluna LGPD gigante
    'As informações pessoais coletadas serão utilizadas exclusivamente...': 'As informações pessoais coletadas'
}

# utils/dataframe_helpers.py
class DataFrameHelper:
    """Helpers para operações comuns em DataFrames."""

    @staticmethod
    def normalize_columns(df: pd.DataFrame, renames: Dict[str, str]) -> pd.DataFrame:
        """Renomeia colunas baseado em mapa."""
        existing_renames = {
            old: new for old, new in renames.items() if old in df.columns
        }
        return df.rename(columns=existing_renames)

    @staticmethod
    def select_available_columns(
        df: pd.DataFrame,
        required: List[str],
        optional: List[str]
    ) -> List[str]:
        """Seleciona colunas disponíveis."""
        selected = []
        for col in required + optional:
            if col in df.columns:
                selected.append(col)
        return selected

# core/excel_generator.py
class ExcelGenerator:
    def _create_table(
        self,
        ws,
        table_name: str,
        ref: str,
        show_totals: bool = True
    ):
        """Cria tabela Excel formatada (reutilizável)."""
        tab = Table(displayName=table_name, ref=ref)
        tab.totalsRowShown = show_totals
        style = TableStyleInfo(
            name="TableStyleMedium12",
            showFirstColumn=False,
            showLastColumn=False,
            showRowStripes=True,
            showColumnStripes=False
        )
        tab.tableStyleInfo = style
        ws.add_table(tab)

    def _auto_adjust_column_widths(self, ws, max_width: int = 50):
        """Ajusta largura de colunas automaticamente (reutilizável)."""
        for column_cells in ws.columns:
            length = max(len(str(cell.value or '')) for cell in column_cells)
            ws.column_dimensions[column_cells[0].column_letter].width = min(
                length + 2,
                max_width
            )
```

**Critérios de Aceitação**:
- [ ] Código duplicado reduzido em >70%
- [ ] Funções helpers criadas e documentadas
- [ ] Todas as chamadas duplicadas substituídas
- [ ] Testes de regressão passam
- [ ] Nenhuma funcionalidade quebrada

---

## ✅ DEFINIÇÃO DE PRONTO (DoD)

Para considerar a Sprint 1 concluída:

- [ ] Todas as 10 tarefas implementadas
- [ ] Code review aprovado para cada tarefa
- [ ] Testes unitários escritos e passando
- [ ] Cobertura de testes >40%
- [ ] Documentação atualizada (docstrings, README)
- [ ] Sem regressões (funcionalidades antigas funcionam)
- [ ] Demo realizada para Product Owner
- [ ] PO aprovou todas as entregas
- [ ] Código commitado e pushed
- [ ] Release notes escritas

---

## 📊 MÉTRICAS DE SUCESSO

| Métrica | Meta |
|---------|------|
| Taxa de erro em produção | <0.05% |
| Erros detectados antes de processar | >90% |
| Tempo para corrigir erro usuário | <5min |
| Satisfação com mensagens erro | >7/10 |
| Cobertura de testes | >40% |
| UI travada durante processamento | 0 ocorrências |

---

## 📅 CRONOGRAMA

| Dia | Tarefas |
|-----|---------|
| **Dia 1-2** | S1-01: Separar classes |
| **Dia 3-4** | S1-02: Desacoplar UI + S1-03: Validações |
| **Dia 5** | S1-04: Tratamento erros |
| **Dia 6** | S1-05 e S1-06: Type hints + Docstrings |
| **Dia 7** | S1-07 e S1-08: Corrigir bugs |
| **Dia 8** | S1-09: Threading + Progresso |
| **Dia 9** | S1-10: Eliminar duplicações |
| **Dia 10** | Testes, review, ajustes finais |

---

## 🚀 VAMOS COMEÇAR!

**Status**: ⏳ PRONTO PARA INICIAR

Próximo passo: Começar pela tarefa S1-01 (Separar Classes)
