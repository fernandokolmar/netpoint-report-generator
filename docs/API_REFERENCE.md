# 🔧 Referência de API - Gerador de Relatórios PRSA

Documentação técnica completa de todas as classes, métodos e funções do sistema.

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Classe VideoConferenceReportGenerator](#-classe-videoconferencereportgenerator)
- [Métodos Públicos](#-métodos-públicos)
- [Métodos Privados](#-métodos-privados)
- [Exemplos de Uso](#-exemplos-de-uso)

---

## 🎯 Visão Geral

### Módulo Principal

**Arquivo**: `prsa_report_generator.py`

**Classe Principal**: `VideoConferenceReportGenerator`

**Ponto de Entrada**:
```python
if __name__ == '__main__':
    root = tk.Tk()
    app = VideoConferenceReportGenerator(root)
    root.mainloop()
```

---

## 📦 Classe VideoConferenceReportGenerator

```python
class VideoConferenceReportGenerator:
    """
    Gerenciador principal de relatórios de videoconferência.

    Responsável por:
    - Interface gráfica (Tkinter)
    - Carregamento e processamento de dados (Pandas)
    - Geração de relatórios Excel (openpyxl)
    """
```

### Atributos de Instância

| Atributo | Tipo | Descrição |
|----------|------|-----------|
| `self.root` | `tk.Tk` | Janela principal Tkinter |
| `self.file_paths` | `Dict[str, str]` | Caminhos dos 4 arquivos CSV |
| `self.file_entries` | `Dict[str, ttk.Entry]` | Widgets Entry para exibir caminhos |
| `self.dataframes` | `Dict[str, pd.DataFrame]` | DataFrames processados |
| `self.log_text` | `tk.Text` | Widget de log com scrollbar |

### Inicialização

```python
def __init__(self, root: tk.Tk) -> None:
    """
    Inicializa a aplicação.

    Args:
        root (tk.Tk): Janela principal Tkinter

    Exemplo:
        >>> root = tk.Tk()
        >>> app = VideoConferenceReportGenerator(root)
    """
```

**Comportamento**:
1. Configura janela (título, tamanho)
2. Inicializa `file_paths` como dict vazio
3. Inicializa `file_entries` como dict vazio
4. Chama `create_widgets()`
5. Exibe mensagem de boas-vindas no log

---

## 🎨 Métodos de Interface (UI)

### create_widgets()

```python
def create_widgets(self) -> None:
    """
    Cria todos os widgets da interface gráfica.

    Widgets criados:
    - Frame principal com padding
    - Labels e Entries para 4 arquivos CSV
    - Botões "Procurar" para cada arquivo
    - Área de log (Text + Scrollbar)
    - Botões de ação (Processar, Limpar, Sair)

    Returns:
        None
    """
```

**Estrutura Criada**:
```
Main Frame
├── Arquivo Inscritos: [Entry] [Procurar]
├── Arquivo Mensagens: [Entry] [Procurar]
├── Relatório de Acesso: [Entry] [Procurar]
├── Arquivo Totalizado: [Entry] [Procurar]
├── [Log Area com Scrollbar]
└── [Processar] [Limpar] [Sair]
```

---

### load_file()

```python
def load_file(self, file_type: str) -> None:
    """
    Abre diálogo para seleção de arquivo CSV.

    Args:
        file_type (str): Tipo do arquivo
            Valores válidos: 'inscritos', 'mensagens', 'relatorio', 'totalizado'

    Side Effects:
        - Atualiza self.file_paths[file_type]
        - Atualiza Entry correspondente com caminho selecionado
        - Adiciona mensagem ao log

    Exemplo:
        >>> self.load_file('inscritos')
        # Abre diálogo, usuário seleciona arquivo
        # self.file_paths['inscritos'] = '/path/to/Inscritos.csv'
    """
```

**Comportamento**:
1. Abre `filedialog.askopenfilename()`
2. Filtro: apenas arquivos `.csv`
3. Se usuário seleciona arquivo:
   - Salva em `self.file_paths[file_type]`
   - Atualiza Entry com caminho
   - Loga: "Arquivo [tipo] carregado"
4. Se usuário cancela: não faz nada

---

### log()

```python
def log(self, message: str) -> None:
    """
    Adiciona mensagem ao log com timestamp.

    Args:
        message (str): Mensagem a ser exibida

    Side Effects:
        - Adiciona linha ao widget log_text
        - Faz scroll automático para o final

    Formato:
        [HH:MM:SS] mensagem

    Exemplo:
        >>> self.log("Processamento iniciado")
        # Adiciona ao log: "[14:30:22] Processamento iniciado"
    """
```

**Implementação**:
```python
timestamp = datetime.now().strftime("%H:%M:%S")
formatted_message = f"[{timestamp}] {message}\n"

self.log_text.config(state=tk.NORMAL)
self.log_text.insert(tk.END, formatted_message)
self.log_text.see(tk.END)  # Auto-scroll
self.log_text.config(state=tk.DISABLED)
```

---

### clear_fields()

```python
def clear_fields(self) -> None:
    """
    Limpa todos os campos e reinicia interface.

    Side Effects:
        - Limpa self.file_paths
        - Limpa todos os Entries
        - Limpa área de log
        - Mostra mensagem de boas-vindas

    Exemplo:
        >>> self.clear_fields()
        # Todos os campos resetados
    """
```

---

## 📁 Métodos de Carregamento de Dados

### validate_files()

```python
def validate_files(self) -> bool:
    """
    Valida se todos os 4 arquivos foram selecionados.

    Returns:
        bool: True se todos selecionados, False caso contrário

    Side Effects:
        - Se falhar: mostra messagebox.showerror

    Exemplo:
        >>> self.file_paths = {'inscritos': '/path/to/file.csv'}
        >>> self.validate_files()
        False  # Faltam 3 arquivos
    """
```

**Lógica**:
```python
required_files = ['inscritos', 'mensagens', 'relatorio', 'totalizado']
missing = [f for f in required_files if not self.file_paths.get(f)]

if missing:
    messagebox.showerror("Erro", f"Faltam arquivos: {missing}")
    return False
return True
```

---

### load_dataframes()

```python
def load_dataframes(self) -> Dict[str, pd.DataFrame]:
    """
    Carrega os 4 arquivos CSV em DataFrames Pandas.

    Returns:
        Dict[str, pd.DataFrame]: Dicionário com os 4 DataFrames
            Keys: 'inscritos', 'mensagens', 'relatorio', 'totalizado'

    Raises:
        FileNotFoundError: Se arquivo não existir
        pd.errors.ParserError: Se CSV estiver mal formatado
        UnicodeDecodeError: Se encoding estiver incorreto

    Exemplo:
        >>> dfs = self.load_dataframes()
        >>> dfs['inscritos'].shape
        (1631, 12)
    """
```

**Implementação**:
```python
dfs = {}

for key, path in self.file_paths.items():
    try:
        df = pd.read_csv(
            path,
            encoding='utf-8-sig',  # Remove BOM
            sep=';'                # Separador brasileiro
        )
        dfs[key] = df
        self.log(f"{key.capitalize()}: {len(df)} registros carregados")
    except Exception as e:
        self.log(f"Erro ao carregar {key}: {str(e)}")
        raise

return dfs
```

---

## 🔄 Métodos de Processamento

### process_data()

```python
def process_data(self) -> None:
    """
    Orquestra o processamento dos 4 DataFrames.

    Side Effects:
        - Atualiza self.dataframes com DataFrames processados
        - Adiciona mensagens ao log

    Ordem de Processamento:
        1. process_inscritos()
        2. process_relatorio()
        3. process_mensagens()
        4. process_totalizado()

    Exemplo:
        >>> self.process_data()
        # self.dataframes contém 4 DataFrames prontos
    """
```

---

### process_inscritos()

```python
def process_inscritos(self, df: pd.DataFrame) -> pd.DataFrame:
    """
    Processa dados de inscritos.

    Transformações:
        1. Renomeia 'Login' → 'Celular'
        2. Renomeia 'Comunidade.1' → 'Comunidade2'
        3. Seleciona apenas colunas existentes

    Args:
        df (pd.DataFrame): DataFrame bruto de inscritos

    Returns:
        pd.DataFrame: DataFrame processado

    Colunas Selecionadas (se existirem):
        - Nome
        - Celular (ex-Login)
        - Município
        - Comunidade
        - Estado
        - Cidade
        - Sou
        - Sobrenome
        - Data de Cadastro
        - LGPD
        - Comunidade2 (ex-Comunidade.1)

    Exemplo:
        >>> df_bruto = pd.read_csv('Inscritos.csv')
        >>> df_processado = self.process_inscritos(df_bruto)
        >>> 'Celular' in df_processado.columns
        True
    """
```

---

### process_relatorio()

```python
def process_relatorio(self, df: pd.DataFrame) -> pd.DataFrame:
    """
    Processa relatório de acesso e calcula retenção.

    Suporta 2 cenários:
        Cenário 1: Coluna 'Tempo' (minutos) existe
        Cenário 2: Colunas 'Data Inicial' e 'Data Final' existem

    Transformações:
        1. Renomeia 'Login' → 'Celular'
        2. Calcula 'Retenção (hh:mm)' em formato HH:MM:SS
        3. Seleciona colunas relevantes

    Args:
        df (pd.DataFrame): DataFrame bruto de acesso

    Returns:
        pd.DataFrame: DataFrame com coluna 'Retenção (hh:mm)' calculada

    Cálculo de Retenção:
        - Cenário 1: Converte minutos para HH:MM:SS
        - Cenário 2: Diferença entre Data Final e Data Inicial

    Exemplo (Cenário 1):
        >>> df = pd.DataFrame({'Tempo': [45, 62]})
        >>> df_proc = self.process_relatorio(df)
        >>> df_proc['Retenção (hh:mm)'].iloc[0]
        '00:45:00'

    Exemplo (Cenário 2):
        >>> df = pd.DataFrame({
        ...     'Data Inicial': ['18/11/2025 19:00:00'],
        ...     'Data Final': ['18/11/2025 19:45:00']
        ... })
        >>> df_proc = self.process_relatorio(df)
        >>> df_proc['Retenção (hh:mm)'].iloc[0]
        '00:45:00'
    """
```

**Implementação (Cenário 1)**:
```python
if 'Tempo' in df.columns:
    df['Retenção (hh:mm)'] = df['Tempo'].apply(
        lambda minutos: f"{int(minutos)//60:02d}:{int(minutos)%60:02d}:00"
    )
```

**Implementação (Cenário 2)**:
```python
elif 'Data Inicial' in df.columns and 'Data Final' in df.columns:
    df['Data Inicial'] = pd.to_datetime(df['Data Inicial'],
                                        format='%d/%m/%Y %H:%M:%S')
    df['Data Final'] = pd.to_datetime(df['Data Final'],
                                      format='%d/%m/%Y %H:%M:%S')

    df['Retenção (hh:mm)'] = (df['Data Final'] - df['Data Inicial']).apply(
        lambda td: f"{td.seconds//3600:02d}:{(td.seconds//60)%60:02d}:{td.seconds%60:02d}"
    )
```

---

### process_mensagens()

```python
def process_mensagens(self, df: pd.DataFrame) -> pd.DataFrame:
    """
    Processa dados de mensagens.

    Transformações:
        1. Renomeia coluna LGPD longa para nome curto
        2. Seleciona colunas relevantes

    Args:
        df (pd.DataFrame): DataFrame bruto de mensagens

    Returns:
        pd.DataFrame: DataFrame processado

    Colunas Selecionadas:
        - Nome
        - Município
        - Comunidade
        - Conteúdo
        - Remetente
        - Email
        - Mensagem
        - Data
        - As informações pessoais coletadas

    Exemplo:
        >>> df = pd.read_csv('Mensagens.csv')
        >>> df_proc = self.process_mensagens(df)
        >>> len(df_proc.columns)
        9
    """
```

---

### process_totalizado()

```python
def process_totalizado(self, df: pd.DataFrame) -> pd.DataFrame:
    """
    Processa dados de audiência minuto a minuto.

    Transformações:
        1. Converte coluna 'Data' para datetime
        2. Cria coluna 'Max' (vazia, será preenchida no Excel)

    Args:
        df (pd.DataFrame): DataFrame bruto de totalizado

    Returns:
        pd.DataFrame: DataFrame com Data convertida e coluna Max

    Exemplo:
        >>> df = pd.DataFrame({
        ...     'Data': ['18/11/2025 19:00:00'],
        ...     'Usuarios conectados': [150]
        ... })
        >>> df_proc = self.process_totalizado(df)
        >>> df_proc['Data'].dtype
        datetime64[ns]
    """
```

---

## 📊 Métodos de Geração de Excel

### create_excel_file()

```python
def create_excel_file(self) -> None:
    """
    Cria arquivo Excel com 4 planilhas.

    Side Effects:
        - Abre diálogo para salvar arquivo
        - Cria e salva arquivo .xlsx
        - Mostra messagebox de sucesso
        - Atualiza log

    Ordem de Criação:
        1. Cria Workbook vazio
        2. Remove planilha padrão
        3. Cria "Retencao na live"
        4. Cria "Mensagens"
        5. Cria "Acessos"
        6. Cria "Inscritos"
        7. Salva arquivo

    Nome Padrão do Arquivo:
        Relatorio_Videoconferencia_YYYYMMDD_HHMMSS.xlsx

    Exemplo:
        >>> self.create_excel_file()
        # Abre diálogo, gera Excel, salva
    """
```

---

### create_retencao_sheet()

```python
def create_retencao_sheet(self, wb: Workbook,
                         df: pd.DataFrame) -> None:
    """
    Cria planilha 'Retencao na live' com dados, gráfico e resumo.

    Args:
        wb (Workbook): Workbook openpyxl
        df (pd.DataFrame): DataFrame de totalizado

    Side Effects:
        - Cria planilha "Retencao na live"
        - Insere dados
        - Cria tabela Excel "retencao"
        - Adiciona gráfico LineChart
        - Insere resumo estatístico (Q2:R7)
        - Ajusta largura de colunas

    Componentes Criados:
        1. Tabela de dados (A1:C[n])
        2. Tabela Excel "retencao"
        3. Gráfico LineChart (posicionado em E2)
        4. Resumo com 6 métricas (Q2:R7)

    Exemplo:
        >>> wb = Workbook()
        >>> df_totalizado = self.dataframes['totalizado']
        >>> self.create_retencao_sheet(wb, df_totalizado)
        >>> 'Retencao na live' in wb.sheetnames
        True
    """
```

**Fórmulas Inseridas no Resumo**:
```python
R2: =inscritos[[#Totals],[Data de Cadastro]]
R3: =Relatório_de_acesso12[[#Totals],[Nome]]
R4: =MAX(retencao[Usuários conectados])
R5: =_xlfn.XLOOKUP(R4,retencao[Usuários conectados],retencao[Data])
R6: =Relatório_de_acesso12[[#Totals],[Retenção (hh:mm)]]
R7: =mensagens[[#Totals],[Data]]
```

---

### create_mensagens_sheet()

```python
def create_mensagens_sheet(self, wb: Workbook,
                          df: pd.DataFrame) -> None:
    """
    Cria planilha 'Mensagens' com dados.

    Args:
        wb (Workbook): Workbook openpyxl
        df (pd.DataFrame): DataFrame de mensagens

    Side Effects:
        - Cria planilha "Mensagens"
        - Insere dados
        - Cria tabela Excel "mensagens"
        - Adiciona linha totalizadora
        - Ajusta largura de colunas

    Fórmula na Linha Total:
        Coluna "Data": =SUBTOTAL(103, mensagens[Data])

    Exemplo:
        >>> self.create_mensagens_sheet(wb, df_mensagens)
    """
```

---

### create_acessos_sheet()

```python
def create_acessos_sheet(self, wb: Workbook,
                        df: pd.DataFrame) -> None:
    """
    Cria planilha 'Acessos' com dados de participação.

    Args:
        wb (Workbook): Workbook openpyxl
        df (pd.DataFrame): DataFrame de relatório de acesso

    Side Effects:
        - Cria planilha "Acessos"
        - Insere dados
        - Cria tabela Excel "Relatorio_de_acesso12"
        - Adiciona linha totalizadora com 2 fórmulas
        - Ajusta largura de colunas

    Fórmulas na Linha Total:
        Coluna "Nome": =SUBTOTAL(103, Relatorio_de_acesso12[Nome])
        Coluna "Retenção (hh:mm)": =SUBTOTAL(101, Relatorio_de_acesso12[Retenção (hh:mm)])

    Exemplo:
        >>> self.create_acessos_sheet(wb, df_relatorio)
    """
```

---

### create_inscritos_sheet()

```python
def create_inscritos_sheet(self, wb: Workbook,
                          df: pd.DataFrame) -> None:
    """
    Cria planilha 'Inscritos' com dados de inscrições.

    Args:
        wb (Workbook): Workbook openpyxl
        df (pd.DataFrame): DataFrame de inscritos

    Side Effects:
        - Cria planilha "Inscritos"
        - Insere dados
        - Cria tabela Excel "inscritos"
        - Adiciona linha totalizadora
        - Ajusta largura de colunas

    Fórmula na Linha Total:
        Última coluna: =SUBTOTAL(103, inscritos[Data de Cadastro])

    Exemplo:
        >>> self.create_inscritos_sheet(wb, df_inscritos)
    """
```

---

### adjust_column_width()

```python
def adjust_column_width(self, ws: Worksheet) -> None:
    """
    Ajusta largura das colunas automaticamente.

    Args:
        ws (Worksheet): Planilha openpyxl

    Lógica:
        - Calcula comprimento máximo de cada coluna
        - Define largura = min(comprimento + 2, 50)

    Side Effects:
        - Modifica ws.column_dimensions[col].width

    Exemplo:
        >>> ws = wb.create_sheet("Exemplo")
        >>> self.adjust_column_width(ws)
        # Colunas ajustadas
    """
```

**Implementação**:
```python
for col in ws.columns:
    max_length = 0
    column = col[0].column_letter

    for cell in col:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))
        except:
            pass

    adjusted_width = min(max_length + 2, 50)
    ws.column_dimensions[column].width = adjusted_width
```

---

## 🚀 Métodos de Orquestração

### process_and_generate()

```python
def process_and_generate(self) -> None:
    """
    Método principal que orquestra todo o fluxo.

    Fluxo:
        1. Valida arquivos selecionados
        2. Carrega DataFrames
        3. Processa dados
        4. Gera arquivo Excel

    Side Effects:
        - Atualiza log em cada etapa
        - Mostra messagebox em caso de erro
        - Cria arquivo Excel

    Este método é chamado quando usuário clica em "Processar e Gerar Relatório".

    Exemplo:
        >>> self.process_and_generate()
        # Fluxo completo executado
    """
```

**Implementação**:
```python
try:
    if not self.validate_files():
        return

    self.log("Carregando arquivos...")
    dfs = self.load_dataframes()

    self.log("Processando dados...")
    self.process_data()

    self.log("Gerando arquivo Excel...")
    self.create_excel_file()

    self.log("✓ Processo concluído com sucesso!")
except Exception as e:
    self.log(f"✗ Erro: {str(e)}")
    traceback.print_exc()
    messagebox.showerror("Erro", f"Erro:\n{str(e)}")
```

---

## 📝 Exemplos de Uso

### Uso Básico (Interface)

```python
import tkinter as tk
from prsa_report_generator import VideoConferenceReportGenerator

# Criar janela principal
root = tk.Tk()

# Criar aplicação
app = VideoConferenceReportGenerator(root)

# Iniciar loop de eventos
root.mainloop()
```

### Uso Programático (Sem Interface)

```python
import pandas as pd
from prsa_report_generator import VideoConferenceReportGenerator

# Criar instância (sem root)
app = VideoConferenceReportGenerator(None)

# Carregar CSVs manualmente
df_inscritos = pd.read_csv('Inscritos.csv', encoding='utf-8-sig', sep=';')
df_mensagens = pd.read_csv('Mensagens.csv', encoding='utf-8-sig', sep=';')
df_relatorio = pd.read_csv('Relatório de acesso.csv', encoding='utf-8-sig', sep=';')
df_totalizado = pd.read_csv('Totalizado.csv', encoding='utf-8-sig', sep=';')

# Processar dados
df_inscritos_proc = app.process_inscritos(df_inscritos)
df_relatorio_proc = app.process_relatorio(df_relatorio)
df_mensagens_proc = app.process_mensagens(df_mensagens)
df_totalizado_proc = app.process_totalizado(df_totalizado)

# Armazenar em self.dataframes
app.dataframes = {
    'inscritos': df_inscritos_proc,
    'mensagens': df_mensagens_proc,
    'relatorio': df_relatorio_proc,
    'totalizado': df_totalizado_proc
}

# Gerar Excel programaticamente
from openpyxl import Workbook

wb = Workbook()
wb.remove(wb.active)

app.create_retencao_sheet(wb, df_totalizado_proc)
app.create_mensagens_sheet(wb, df_mensagens_proc)
app.create_acessos_sheet(wb, df_relatorio_proc)
app.create_inscritos_sheet(wb, df_inscritos_proc)

wb.save('output.xlsx')
```

### Processar Apenas Inscritos

```python
import pandas as pd
from prsa_report_generator import VideoConferenceReportGenerator

app = VideoConferenceReportGenerator(None)

# Carregar e processar apenas inscritos
df = pd.read_csv('Inscritos.csv', encoding='utf-8-sig', sep=';')
df_processado = app.process_inscritos(df)

print(df_processado.head())
print(f"Colunas: {df_processado.columns.tolist()}")
```

---

## 🔗 Dependências Externas

### Imports Necessários

```python
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter
from datetime import datetime
import traceback
```

---

**Documento mantido por**: Equipe de Desenvolvimento PRSA
**Última atualização**: 29/01/2025
