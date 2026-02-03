# 🏗️ Arquitetura do Sistema - Gerador de Relatórios PRSA

Este documento descreve a arquitetura completa do sistema, incluindo estrutura de classes, fluxo de dados, padrões arquiteturais e decisões de design.

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Arquitetura de Alto Nível](#-arquitetura-de-alto-nível)
- [Estrutura de Classes](#-estrutura-de-classes)
- [Fluxo de Dados](#-fluxo-de-dados)
- [Componentes Principais](#-componentes-principais)
- [Padrões Arquiteturais](#-padrões-arquiteturais)
- [Decisões de Design](#-decisões-de-design)
- [Dependências](#-dependências)
- [Escalabilidade](#-escalabilidade)

---

## 🎯 Visão Geral

### Propósito do Sistema

O **Gerador de Relatórios PRSA** é uma aplicação desktop que automatiza a criação de relatórios estatísticos de videoconferências. O sistema processa dados de múltiplas fontes (CSV) e gera um relatório consolidado em formato Excel com gráficos e análises.

### Características Arquiteturais

- **Arquitetura**: Monolítica com separação de responsabilidades
- **Paradigma**: Orientado a Objetos (OOP)
- **Interface**: Desktop GUI (Tkinter)
- **Processamento**: Batch/Offline (sem streaming)
- **Persistência**: Arquivos (CSV input, Excel output)
- **Deployment**: Standalone (sem servidor)

### Princípios Arquiteturais

1. **Separação de Responsabilidades** - UI, Processamento e Geração separados
2. **Baixo Acoplamento** - Componentes independentes
3. **Alta Coesão** - Funcionalidades relacionadas agrupadas
4. **DRY (Don't Repeat Yourself)** - Reutilização de código
5. **KISS (Keep It Simple, Stupid)** - Simplicidade sobre complexidade

---

## 🌐 Arquitetura de Alto Nível

### Diagrama de Camadas

```
┌─────────────────────────────────────────────────────┐
│          CAMADA DE APRESENTAÇÃO (UI)                │
│                                                       │
│  ┌────────────────────────────────────────────┐    │
│  │     Tkinter GUI Interface                   │    │
│  │  - Widgets de entrada de arquivo            │    │
│  │  - Área de log                              │    │
│  │  - Botões de ação                           │    │
│  └────────────────────────────────────────────┘    │
└───────────────────┬───────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────────────────┐
│         CAMADA DE CONTROLE (Logic)                  │
│                                                       │
│  ┌────────────────────────────────────────────┐    │
│  │  VideoConferenceReportGenerator             │    │
│  │  - Orquestração do fluxo                    │    │
│  │  - Validação de entrada                     │    │
│  │  - Coordenação de processamento             │    │
│  └────────────────────────────────────────────┘    │
└───────────────────┬───────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────────────────┐
│       CAMADA DE PROCESSAMENTO (Data)                │
│                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │  Pandas      │  │   NumPy      │  │ datetime │ │
│  │  DataFrames  │  │  Cálculos    │  │  Datas   │ │
│  └──────────────┘  └──────────────┘  └──────────┘ │
└───────────────────┬───────────────────────────────┘
                    │
                    ↓
┌─────────────────────────────────────────────────────┐
│        CAMADA DE SAÍDA (Output)                     │
│                                                       │
│  ┌────────────────────────────────────────────┐    │
│  │         openpyxl Excel Writer               │    │
│  │  - Criação de planilhas                     │    │
│  │  - Formatação de tabelas                    │    │
│  │  - Geração de gráficos                      │    │
│  │  - Aplicação de fórmulas                    │    │
│  └────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
                    │
                    ↓
              ┌─────────────┐
              │  Excel File │
              └─────────────┘
```

---

## 🧩 Estrutura de Classes

### Classe Principal: `VideoConferenceReportGenerator`

```python
class VideoConferenceReportGenerator:
    """
    Classe principal responsável por gerar relatórios de videoconferência.

    Responsabilidades:
    - Gerenciar interface gráfica (Tkinter)
    - Carregar e validar arquivos CSV
    - Processar dados com Pandas
    - Gerar arquivo Excel com openpyxl
    - Logar operações para o usuário
    """

    # ========== ATRIBUTOS DE INSTÂNCIA ==========

    self.root: tk.Tk                    # Janela principal Tkinter
    self.file_paths: Dict[str, str]     # Caminhos dos 4 arquivos CSV
    self.dataframes: Dict[str, pd.DataFrame]  # DataFrames processados
    self.log_text: tk.Text              # Widget de log

    # ========== MÉTODOS DE INTERFACE ==========

    def __init__(self, root: tk.Tk) -> None:
        """Inicializa a interface e variáveis"""

    def create_widgets(self) -> None:
        """Cria widgets da interface gráfica"""

    def load_file(self, file_type: str) -> None:
        """Abre diálogo de seleção de arquivo"""

    def log(self, message: str) -> None:
        """Adiciona mensagem ao log com timestamp"""

    # ========== MÉTODOS DE VALIDAÇÃO ==========

    def validate_files(self) -> bool:
        """Valida se todos os 4 arquivos foram selecionados"""

    # ========== MÉTODOS DE CARREGAMENTO ==========

    def load_dataframes(self) -> Dict[str, pd.DataFrame]:
        """Carrega os 4 CSVs em DataFrames Pandas"""

    # ========== MÉTODOS DE PROCESSAMENTO ==========

    def process_data(self) -> None:
        """Orquestra o processamento dos 4 DataFrames"""

    def process_inscritos(self, df: pd.DataFrame) -> pd.DataFrame:
        """Processa dados de inscritos"""

    def process_relatorio(self, df: pd.DataFrame) -> pd.DataFrame:
        """Processa relatório de acesso e calcula retenção"""

    def process_mensagens(self, df: pd.DataFrame) -> pd.DataFrame:
        """Processa dados de mensagens"""

    def process_totalizado(self, df: pd.DataFrame) -> pd.DataFrame:
        """Processa dados de audiência minuto a minuto"""

    # ========== MÉTODOS DE GERAÇÃO DE EXCEL ==========

    def create_excel_file(self) -> None:
        """Cria arquivo Excel com 4 planilhas"""

    def create_retencao_sheet(self, wb: Workbook, df: pd.DataFrame) -> None:
        """Cria planilha 'Retencao na live' com gráfico"""

    def create_mensagens_sheet(self, wb: Workbook, df: pd.DataFrame) -> None:
        """Cria planilha 'Mensagens'"""

    def create_acessos_sheet(self, wb: Workbook, df: pd.DataFrame) -> None:
        """Cria planilha 'Acessos'"""

    def create_inscritos_sheet(self, wb: Workbook, df: pd.DataFrame) -> None:
        """Cria planilha 'Inscritos'"""

    # ========== MÉTODOS AUXILIARES ==========

    def adjust_column_width(self, ws: Worksheet) -> None:
        """Ajusta largura das colunas automaticamente"""

    def clear_fields(self) -> None:
        """Limpa campos e reinicia interface"""

    def process_and_generate(self) -> None:
        """Método principal que orquestra todo o fluxo"""
```

### Responsabilidades por Método

| Método | Camada | Responsabilidade |
|--------|--------|------------------|
| `__init__()` | UI | Inicializar interface |
| `create_widgets()` | UI | Criar elementos visuais |
| `load_file()` | UI | Interação de seleção de arquivo |
| `log()` | UI | Feedback visual ao usuário |
| `validate_files()` | Controle | Validar entrada |
| `load_dataframes()` | Data | Ler CSVs |
| `process_*()` | Data | Transformar dados |
| `create_excel_file()` | Output | Orquestrar criação Excel |
| `create_*_sheet()` | Output | Criar planilhas individuais |
| `adjust_column_width()` | Output | Formatação |

---

## 🔄 Fluxo de Dados

### Fluxo Completo End-to-End

```
┌─────────────────┐
│   INÍCIO        │
│  (Usuário abre  │
│   aplicação)    │
└────────┬────────┘
         │
         ↓
┌─────────────────────────────────┐
│  1. INICIALIZAÇÃO               │
│  - root = tk.Tk()               │
│  - app = VideoConference...()   │
│  - create_widgets()             │
│  - root.mainloop()              │
└────────┬────────────────────────┘
         │
         ↓
┌─────────────────────────────────┐
│  2. SELEÇÃO DE ARQUIVOS         │
│  - Usuário clica "Procurar"     │
│  - load_file() abre diálogo     │
│  - Caminho salvo em file_paths  │
│  - Repetir para 4 arquivos      │
└────────┬────────────────────────┘
         │
         ↓
┌─────────────────────────────────┐
│  3. CLIQUE EM "PROCESSAR"       │
│  - process_and_generate()       │
│  - validate_files() → bool      │
│  - Se False: messagebox.error   │
└────────┬────────────────────────┘
         │
         ↓
┌─────────────────────────────────┐
│  4. CARREGAMENTO                │
│  - load_dataframes()            │
│  ┌─────────────────────────┐   │
│  │ pd.read_csv()           │   │
│  │ encoding='utf-8-sig'    │   │
│  │ sep=';'                 │   │
│  └─────────────────────────┘   │
│  - Retorna Dict[str, DataFrame] │
└────────┬────────────────────────┘
         │
         ↓
┌─────────────────────────────────┐
│  5. PROCESSAMENTO               │
│  - process_data()               │
│  ┌─────────────────────────┐   │
│  │ process_inscritos()     │   │
│  │   - Renomeia colunas    │   │
│  │   - Seleciona campos    │   │
│  │                         │   │
│  │ process_relatorio()     │   │
│  │   - Calcula retenção    │   │
│  │   - Converte tempo      │   │
│  │                         │   │
│  │ process_mensagens()     │   │
│  │   - Seleciona colunas   │   │
│  │                         │   │
│  │ process_totalizado()    │   │
│  │   - Converte datas      │   │
│  │   - Cria coluna "Max"   │   │
│  └─────────────────────────┘   │
│  - Armazena em self.dataframes  │
└────────┬────────────────────────┘
         │
         ↓
┌─────────────────────────────────┐
│  6. CRIAÇÃO DE EXCEL            │
│  - create_excel_file()          │
│  - filedialog.asksaveasfilename │
│  ┌─────────────────────────┐   │
│  │ wb = Workbook()         │   │
│  │                         │   │
│  │ create_retencao_sheet() │   │
│  │  - Insere dados         │   │
│  │  - Cria tabela          │   │
│  │  - Adiciona gráfico     │   │
│  │  - Insere fórmulas      │   │
│  │                         │   │
│  │ create_mensagens_sheet()│   │
│  │ create_acessos_sheet()  │   │
│  │ create_inscritos_sheet()│   │
│  │                         │   │
│  │ wb.save(filename)       │   │
│  └─────────────────────────┘   │
└────────┬────────────────────────┘
         │
         ↓
┌─────────────────────────────────┐
│  7. FINALIZAÇÃO                 │
│  - messagebox.showinfo("Sucesso")│
│  - log("Arquivo gerado")        │
└────────┬────────────────────────┘
         │
         ↓
┌─────────────────┐
│   FIM           │
│  (Arquivo Excel │
│   gerado)       │
└─────────────────┘
```

### Fluxo de Transformação de Dados

```
CSV (Inscritos)
  ↓
  read_csv (Pandas)
  ↓
  DataFrame (1631 linhas)
  ↓
  process_inscritos()
    - Renomear: Login → Celular
    - Selecionar colunas existentes
    - Tratar Comunidade.1 → Comunidade2
  ↓
  DataFrame processado
  ↓
  create_inscritos_sheet()
    - Criar planilha
    - Inserir dados linha por linha
    - Criar Table ("inscritos")
    - Adicionar totalizadora
    - Ajustar largura
  ↓
  Planilha Excel "Inscritos"
```

---

## 🔧 Componentes Principais

### 1. Interface Gráfica (Tkinter)

**Arquivo**: `prsa_report_generator.py` (linhas 1-100 aprox.)

**Responsabilidade**: Interação com usuário

**Componentes**:
```python
# Janela principal
root = tk.Tk()
root.geometry("800x600")
root.title("Gerador de Relatórios...")

# Frame principal
main_frame = ttk.Frame(root, padding="10")

# Labels de instrução
ttk.Label(..., text="Arquivo Inscritos:")

# Entries (campos de texto read-only)
entry = ttk.Entry(..., state="readonly")

# Buttons
ttk.Button(..., text="Procurar", command=lambda: load_file("inscritos"))
ttk.Button(..., text="Processar e Gerar Relatório", command=process_and_generate)

# Text widget (log)
log_text = tk.Text(..., height=15, wrap=tk.WORD, state=tk.DISABLED)

# Scrollbar
scrollbar = ttk.Scrollbar(..., command=log_text.yview)
```

**Interações**:
- Click em "Procurar" → `load_file()`
- Click em "Processar" → `process_and_generate()`
- Click em "Limpar" → `clear_fields()`
- Click em "Sair" → `root.quit()`

---

### 2. Carregamento de Dados (Pandas)

**Responsabilidade**: Ler CSVs e criar DataFrames

**Código**:
```python
def load_dataframes(self):
    dfs = {}

    # Inscritos
    dfs['inscritos'] = pd.read_csv(
        self.file_paths['inscritos'],
        encoding='utf-8-sig',
        sep=';'
    )

    # Mensagens
    dfs['mensagens'] = pd.read_csv(...)

    # Relatório de acesso
    dfs['relatorio'] = pd.read_csv(...)

    # Totalizado
    dfs['totalizado'] = pd.read_csv(...)

    return dfs
```

**Características**:
- Encoding: UTF-8 com BOM (`utf-8-sig`)
- Separador: Ponto-e-vírgula (`;`)
- Sem especificação de dtypes (inferência automática)
- Tratamento de erros com try-except

---

### 3. Processamento de Dados

**Responsabilidade**: Transformar DataFrames brutos

**Transformações por Tipo**:

#### Inscritos
```python
# Renomear coluna
if 'Login' in df.columns:
    df.rename(columns={'Login': 'Celular'}, inplace=True)

# Selecionar colunas (flexível)
cols = []
if 'Nome' in df.columns: cols.append('Nome')
if 'Celular' in df.columns: cols.append('Celular')
# ... outras colunas

df = df[cols]
```

#### Relatório de Acesso (Cálculo de Retenção)
```python
# Cenário 1: Coluna "Tempo" em minutos
if 'Tempo' in df.columns:
    df['Retenção (hh:mm)'] = df['Tempo'].apply(
        lambda x: f"{int(x)//60:02d}:{int(x)%60:02d}"
    )

# Cenário 2: Data Inicial e Final
elif 'Data Inicial' in df.columns and 'Data Final' in df.columns:
    df['Data Inicial'] = pd.to_datetime(df['Data Inicial'], format='%d/%m/%Y %H:%M:%S')
    df['Data Final'] = pd.to_datetime(df['Data Final'], format='%d/%m/%Y %H:%M:%S')

    df['Retenção (hh:mm)'] = (df['Data Final'] - df['Data Inicial']).apply(
        lambda x: f"{x.seconds//3600:02d}:{(x.seconds//60)%60:02d}"
    )
```

#### Totalizado
```python
# Converter coluna Data
df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y %H:%M:%S')

# Criar coluna "Max" (vazia, será preenchida por fórmula Excel)
df['Max'] = ''
```

---

### 4. Geração de Excel (openpyxl)

**Responsabilidade**: Criar arquivo Excel formatado

**Estrutura de Criação**:

```python
from openpyxl import Workbook
from openpyxl.chart import LineChart
from openpyxl.worksheet.table import Table, TableStyleInfo

wb = Workbook()
wb.remove(wb.active)  # Remove planilha padrão

# Criar 4 planilhas
create_retencao_sheet(wb, dataframes['totalizado'])
create_mensagens_sheet(wb, dataframes['mensagens'])
create_acessos_sheet(wb, dataframes['relatorio'])
create_inscritos_sheet(wb, dataframes['inscritos'])

wb.save(filename)
```

**Exemplo de Criação de Planilha**:
```python
def create_inscritos_sheet(self, wb, df):
    ws = wb.create_sheet("Inscritos")

    # 1. Inserir cabeçalhos
    for col_idx, col_name in enumerate(df.columns, start=1):
        ws.cell(row=1, column=col_idx, value=col_name)

    # 2. Inserir dados
    for row_idx, row_data in enumerate(df.itertuples(index=False), start=2):
        for col_idx, value in enumerate(row_data, start=1):
            ws.cell(row=row_idx, column=col_idx, value=value)

    # 3. Criar tabela Excel
    tab = Table(
        displayName="inscritos",
        ref=f"A1:{get_column_letter(len(df.columns))}{len(df)+1}"
    )
    tab.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium12",
        showRowStripes=True
    )
    ws.add_table(tab)

    # 4. Adicionar linha totalizadora
    total_row = len(df) + 2
    ws.cell(total_row, data_col_idx,
            value="=SUBTOTAL(103, inscritos[Data de Cadastro])")

    # 5. Ajustar largura
    adjust_column_width(ws)
```

---

## 🎨 Padrões Arquiteturais

### 1. MVC (Model-View-Controller) - Adaptado

**Model** (Dados):
- DataFrames Pandas
- Arquivos CSV (entrada)
- Arquivo Excel (saída)

**View** (Visualização):
- Interface Tkinter
- Widgets (Entry, Button, Text)
- Mensagens de log

**Controller** (Controle):
- Classe `VideoConferenceReportGenerator`
- Métodos de processamento
- Orquestração do fluxo

### 2. Single Responsibility Principle (SRP)

Cada método tem **uma única responsabilidade**:

- `load_file()` → Apenas abre diálogo
- `validate_files()` → Apenas valida
- `process_inscritos()` → Apenas processa inscritos
- `create_excel_file()` → Apenas orquestra criação Excel

### 3. Dependency Injection

Métodos recebem dependências como parâmetros:

```python
def create_inscritos_sheet(self, wb: Workbook, df: pd.DataFrame):
    # wb e df são injetados, não criados internamente
    pass
```

### 4. Template Method Pattern

`create_excel_file()` é um template que chama métodos específicos:

```python
def create_excel_file(self):
    wb = Workbook()

    # Template: sempre criar as 4 planilhas na mesma ordem
    self.create_retencao_sheet(wb, ...)
    self.create_mensagens_sheet(wb, ...)
    self.create_acessos_sheet(wb, ...)
    self.create_inscritos_sheet(wb, ...)

    wb.save(...)
```

---

## 💡 Decisões de Design

### Por que Tkinter?

**Vantagens**:
- ✅ Incluído no Python (sem dependências extras)
- ✅ Multiplataforma (Windows, Linux, Mac)
- ✅ Simples para interfaces básicas
- ✅ Baixa curva de aprendizado

**Desvantagens**:
- ❌ Interface não é moderna/bonita
- ❌ Limitado para UIs complexas

**Alternativas consideradas**:
- PyQt5 (muito pesado para uso simples)
- Web (Flask + HTML) (desnecessário para uso local)
- CLI (menos user-friendly para não-técnicos)

### Por que Pandas?

**Vantagens**:
- ✅ Excelente para manipulação de dados tabulares
- ✅ Leitura de CSV otimizada
- ✅ Operações em batch (vetorizadas)
- ✅ Comunidade grande e documentação rica

**Decisão**: Ideal para o caso de uso (processar CSVs)

### Por que openpyxl?

**Vantagens**:
- ✅ Suporta arquivos .xlsx (Excel moderno)
- ✅ Permite criar fórmulas, gráficos e tabelas
- ✅ Não requer Microsoft Excel instalado
- ✅ Bem mantido e documentado

**Alternativas**:
- xlsxwriter (similar, mas openpyxl mais completo)
- XlsxWriter + Pandas (mais código necessário)

### Por que UTF-8-SIG?

**Razão**: CSV gerados por Excel frequentemente têm BOM (Byte Order Mark)

**Problema sem SIG**: `\ufeff` aparece no primeiro cabeçalho

**Solução**: `encoding='utf-8-sig'` remove BOM automaticamente

### Por que Separador `;`?

**Razão**: Excel em português usa `;` por padrão (vírgula é decimal)

**Problema com `,`**: Conflito com separador decimal brasileiro

---

## 📦 Dependências

### Dependências Diretas

```
pandas>=2.0.0
  ├── numpy>=1.24.0      (instalado automaticamente)
  ├── python-dateutil    (instalado automaticamente)
  └── pytz               (instalado automaticamente)

openpyxl>=3.1.0
  └── et-xmlfile         (instalado automaticamente)

tkinter
  └── (Built-in Python)
```

### Grafo de Dependências

```
prsa_report_generator.py
├── tkinter (UI)
├── pandas (Data Processing)
│   ├── numpy (Numerical)
│   └── datetime (Dates)
├── openpyxl (Excel Generation)
│   └── openpyxl.chart (Charts)
└── traceback (Error Handling)
```

---

## 📈 Escalabilidade

### Limitações Atuais

| Aspecto | Limite Atual | Razão |
|---------|--------------|-------|
| **Tamanho de CSV** | ~100.000 linhas | Memória RAM (Pandas carrega tudo) |
| **Concorrência** | 1 processamento por vez | Interface single-thread |
| **Usuários simultâneos** | 1 | Aplicação desktop standalone |
| **Formatos de entrada** | Apenas CSV | Hardcoded no código |
| **Formatos de saída** | Apenas Excel | Hardcoded no código |

### Estratégias de Escalabilidade

#### Curto Prazo (sem mudanças arquiteturais)

1. **Otimizar leitura de CSV**:
   ```python
   # Usar chunking para CSVs grandes
   chunks = pd.read_csv(file, chunksize=10000)
   df = pd.concat(chunks, ignore_index=True)
   ```

2. **Processar em paralelo** (múltiplos CSVs):
   ```python
   from concurrent.futures import ThreadPoolExecutor

   with ThreadPoolExecutor() as executor:
       futures = [
           executor.submit(pd.read_csv, path)
           for path in file_paths.values()
       ]
       dfs = [f.result() for f in futures]
   ```

#### Longo Prazo (mudanças arquiteturais)

1. **Migrar para arquitetura cliente-servidor**:
   - Backend: Flask/FastAPI
   - Frontend: React/Vue
   - Processamento assíncrono (Celery)
   - Banco de dados (PostgreSQL)

2. **Usar processamento distribuído**:
   - Dask (para DataFrames gigantes)
   - Spark (para Big Data)

3. **Streaming de dados**:
   - Processar linha por linha
   - Evitar carregar tudo em memória

### Recomendações para Escalar

**Se volume < 1 milhão de linhas**: Arquitetura atual é suficiente

**Se volume > 1 milhão de linhas**: Considerar refatoração para:
- Backend separado
- Banco de dados
- Processamento assíncrono
- Cache de resultados

---

## 🔒 Segurança

### Vulnerabilidades Consideradas

1. **Path Traversal**: ✅ Mitigado (filedialog não permite)
2. **Code Injection**: ✅ Não aplicável (sem exec/eval)
3. **SQL Injection**: ✅ Não aplicável (sem banco de dados)
4. **XSS**: ✅ Não aplicável (não é web)

### Boas Práticas Implementadas

- ✅ Validação de entrada (arquivo existe)
- ✅ Try-except em operações de I/O
- ✅ Encoding fixo (evita problemas de charset)
- ✅ Sem execução de código dinâmico

---

## 📝 Notas de Arquitetura

### Trade-offs Realizados

| Decisão | Vantagem | Desvantagem |
|---------|----------|-------------|
| Arquitetura monolítica | Simples, fácil de deployar | Difícil escalar |
| Tkinter | Sem dependências extras | Interface básica |
| Pandas carrega tudo em RAM | Processamento rápido | Limite de tamanho |
| openpyxl | Fórmulas e gráficos | Mais lento que xlsxwriter |

### Evoluções Futuras Sugeridas

1. **Separar UI de lógica** → Facilitar testes
2. **Adicionar testes unitários** → Aumentar confiabilidade
3. **Configurações externas** → Flexibilizar comportamento
4. **Logging estruturado** → Melhor debugging
5. **Versionamento de relatórios** → Rastreabilidade

---

**Documento mantido por**: Equipe de Desenvolvimento PRSA
**Última atualização**: 29/01/2025
