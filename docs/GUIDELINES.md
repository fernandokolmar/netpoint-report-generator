# 📝 Diretrizes de Desenvolvimento - Gerador de Relatórios PRSA

Este documento define os padrões e convenções de código para o projeto, garantindo consistência, manutenibilidade e qualidade.

---

## 📋 Índice

- [Convenções de Código Python](#-convenções-de-código-python)
- [Estrutura de Arquivos](#-estrutura-de-arquivos)
- [Nomenclatura](#-nomenclatura)
- [Documentação de Código](#-documentação-de-código)
- [Boas Práticas](#-boas-práticas)
- [Controle de Versão](#-controle-de-versão)
- [Testes](#-testes)

---

## 🐍 Convenções de Código Python

### PEP 8 - Style Guide

Este projeto segue as diretrizes do **PEP 8** (Python Enhancement Proposal 8).

**Referência**: [https://pep8.org/](https://pep8.org/)

### Indentação

```python
# ✅ CORRETO: 4 espaços
def exemplo():
    if condicao:
        return True
    return False

# ❌ ERRADO: Tabs ou 2 espaços
def exemplo():
  if condicao:
      return True
```

**Regra**: Use **4 espaços** por nível de indentação (nunca tabs).

### Comprimento de Linha

```python
# ✅ CORRETO: Máximo 88 caracteres (seguindo Black formatter)
def processar_dados(df, colunas_selecionadas, encoding='utf-8',
                    separador=';'):
    pass

# ✅ CORRETO: Quebra de linha em listas longas
colunas = [
    'Nome', 'Celular', 'Município',
    'Comunidade', 'Data de Cadastro'
]

# ❌ EVITAR: Linhas muito longas
def processar_dados(dataframe, colunas_selecionadas, encoding_tipo='utf-8', separador_csv=';', validar_entrada=True, registrar_log=True):
    pass
```

**Regra**: Máximo **88 caracteres** por linha.

### Espaçamento

```python
# ✅ CORRETO: Espaços ao redor de operadores
x = 10
y = x + 5
resultado = funcao(a, b, c)

# ❌ ERRADO: Sem espaços
x=10
y=x+5
resultado=funcao(a,b,c)

# ✅ CORRETO: Sem espaço em argumentos padrão
def funcao(x, y=10, z=20):
    pass

# ❌ ERRADO: Espaço em argumentos padrão
def funcao(x, y = 10, z = 20):
    pass
```

### Imports

```python
# ✅ CORRETO: Ordem de imports
# 1. Biblioteca padrão
import os
import sys
from datetime import datetime

# 2. Bibliotecas de terceiros
import pandas as pd
import numpy as np
from openpyxl import Workbook

# 3. Imports locais
from .utils import helper_function

# ✅ CORRETO: Um import por linha para clareza
from openpyxl.chart import LineChart, Reference
from openpyxl.worksheet.table import Table, TableStyleInfo

# ❌ EVITAR: Import com *
from pandas import *
```

### Strings

```python
# ✅ CORRETO: Aspas duplas para strings de usuário
mensagem = "Erro ao processar arquivo"
titulo = "Gerador de Relatórios"

# ✅ CORRETO: Aspas simples para keys/constantes
config = {'encoding': 'utf-8', 'sep': ';'}

# ✅ CORRETO: f-strings para formatação
nome = "João"
mensagem = f"Olá, {nome}! Bem-vindo."

# ❌ EVITAR: Concatenação com +
mensagem = "Olá, " + nome + "! Bem-vindo."

# ✅ CORRETO: Strings multi-linha
texto = """
Este é um texto
muito longo que
ocupa várias linhas.
"""
```

---

## 📁 Estrutura de Arquivos

### Organização de Diretórios

```
App Estatisticas/
├── prsa_report_generator.py     # Arquivo principal
├── requirements.txt              # Dependências
├── README.md                     # Documentação principal
├── INSTALACAO_RAPIDA.md         # Guia de instalação
│
├── docs/                         # Documentação técnica
│   ├── README.md
│   ├── ARCHITECTURE.md
│   ├── GUIDELINES.md
│   └── ...
│
├── tests/                        # Testes (se houver)
│   ├── test_prsa.py
│   └── ...
│
├── scripts/                      # Scripts auxiliares
│   ├── analyze_template.py
│   ├── extract_formulas.py
│   └── ...
│
└── data/                         # Dados de exemplo
    ├── Inscritos.csv
    └── ...
```

### Convenções de Nomes de Arquivos

| Tipo | Convenção | Exemplo |
|------|-----------|---------|
| **Módulo Python** | snake_case | `prsa_report_generator.py` |
| **Classe** | PascalCase | `VideoConferenceReportGenerator` |
| **Constante** | UPPER_SNAKE_CASE | `MAX_ROWS = 100000` |
| **Documentação** | UPPERCASE.md | `README.md`, `GUIDELINES.md` |
| **Dados** | PascalCase.csv | `Inscritos.csv` |

---

## 🏷️ Nomenclatura

### Classes

```python
# ✅ CORRETO: PascalCase (primeira letra maiúscula)
class VideoConferenceReportGenerator:
    pass

class ExcelFileWriter:
    pass

# ❌ ERRADO: snake_case ou camelCase
class video_conference_report_generator:
    pass

class videoConferenceReportGenerator:
    pass
```

### Funções e Métodos

```python
# ✅ CORRETO: snake_case (minúsculas com underscores)
def process_data(df):
    pass

def create_excel_file(workbook, dataframe):
    pass

# ❌ ERRADO: camelCase ou PascalCase
def processData(df):
    pass

def CreateExcelFile(workbook, dataframe):
    pass
```

### Variáveis

```python
# ✅ CORRETO: snake_case descritivo
file_path = "/path/to/file.csv"
total_rows = 1000
user_name = "João Silva"

# ✅ CORRETO: Variáveis booleanas com prefixos is_, has_, can_
is_valid = True
has_data = False
can_process = True

# ❌ EVITAR: Nomes curtos não descritivos
fp = "/path/to/file.csv"
n = 1000
x = "João Silva"

# ❌ EVITAR: camelCase
fileName = "file.csv"
totalRows = 1000
```

### Constantes

```python
# ✅ CORRETO: UPPER_SNAKE_CASE
MAX_FILE_SIZE = 10_000_000  # 10 MB
DEFAULT_ENCODING = 'utf-8-sig'
CSV_SEPARATOR = ';'

# Agrupar constantes relacionadas
class Config:
    ENCODING = 'utf-8-sig'
    SEPARATOR = ';'
    MAX_ROWS = 100_000
```

### DataFrames Pandas

```python
# ✅ CORRETO: Sufixo _df para DataFrames
inscritos_df = pd.read_csv('Inscritos.csv')
mensagens_df = pd.read_csv('Mensagens.csv')

# ✅ CORRETO: Variável genérica
df = process_data(input_df)

# ❌ EVITAR: Nomes ambíguos
data = pd.read_csv('Inscritos.csv')  # data de que?
inscritos = pd.read_csv(...)  # DataFrame ou lista?
```

---

## 📖 Documentação de Código

### Docstrings

Use **docstrings** em todas as classes e funções públicas.

**Formato**: Google Style ou NumPy Style

#### Classe

```python
class VideoConferenceReportGenerator:
    """
    Gerenciador de relatórios de videoconferência.

    Esta classe é responsável por carregar dados de CSVs,
    processá-los e gerar relatórios em formato Excel.

    Attributes:
        root (tk.Tk): Janela principal Tkinter
        file_paths (dict): Caminhos dos arquivos CSV
        dataframes (dict): DataFrames processados

    Example:
        >>> root = tk.Tk()
        >>> app = VideoConferenceReportGenerator(root)
        >>> root.mainloop()
    """
```

#### Função/Método

```python
def process_inscritos(self, df: pd.DataFrame) -> pd.DataFrame:
    """
    Processa dados de inscritos.

    Renomeia colunas, seleciona campos relevantes e trata
    dados ausentes conforme regras de negócio.

    Args:
        df (pd.DataFrame): DataFrame bruto de inscritos

    Returns:
        pd.DataFrame: DataFrame processado com colunas selecionadas

    Raises:
        KeyError: Se colunas obrigatórias estiverem ausentes
        ValueError: Se DataFrame estiver vazio

    Example:
        >>> df = pd.read_csv('Inscritos.csv')
        >>> df_processado = self.process_inscritos(df)
        >>> print(df_processado.columns)
    """
    pass
```

### Comentários

```python
# ✅ CORRETO: Comentários explicam "por quê", não "o quê"
# Removemos BOM porque Excel em português adiciona ao exportar CSV
df = pd.read_csv(file, encoding='utf-8-sig')

# Calculamos retenção em dois cenários para suportar formatos legados
if 'Tempo' in df.columns:
    # Formato antigo: minutos diretos
    df['Retenção'] = calc_from_minutes(df['Tempo'])
else:
    # Formato novo: data inicial e final
    df['Retenção'] = calc_from_dates(df['Data Inicial'], df['Data Final'])

# ❌ EVITAR: Comentários que apenas repetem o código
# Lê o CSV
df = pd.read_csv(file)

# Cria uma variável x com valor 10
x = 10
```

### TODOs e FIXMEs

```python
# TODO: Adicionar validação de tamanho de arquivo
def load_file(self, path):
    pass

# FIXME: Tratamento de erro não captura FileNotFoundError específico
try:
    df = pd.read_csv(path)
except Exception as e:
    log(f"Erro: {e}")

# NOTE: Esta função pode ser lenta com DataFrames grandes
def process_large_df(df):
    pass
```

---

## ✅ Boas Práticas

### Type Hints (Anotações de Tipo)

```python
from typing import Dict, List, Optional
import pandas as pd

# ✅ CORRETO: Type hints em funções
def load_dataframes(file_paths: Dict[str, str]) -> Dict[str, pd.DataFrame]:
    """Carrega CSVs em DataFrames."""
    return {}

def process_data(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """Processa DataFrame."""
    return df

def get_config(key: str) -> Optional[str]:
    """Retorna configuração ou None."""
    return None
```

### Tratamento de Erros

```python
# ✅ CORRETO: Capturar exceções específicas
try:
    df = pd.read_csv(file_path, encoding='utf-8-sig', sep=';')
except FileNotFoundError:
    self.log(f"Arquivo não encontrado: {file_path}")
    raise
except pd.errors.EmptyDataError:
    self.log("Arquivo CSV está vazio")
    raise
except Exception as e:
    self.log(f"Erro inesperado: {str(e)}")
    traceback.print_exc()
    raise

# ❌ EVITAR: Capturar Exception genérico sem re-raise
try:
    df = pd.read_csv(file_path)
except Exception:
    pass  # Silencia erro (muito perigoso!)
```

### Validação de Entrada

```python
# ✅ CORRETO: Validar entrada cedo (fail fast)
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        raise ValueError("DataFrame não pode ser vazio")

    required_columns = ['Nome', 'Celular']
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise KeyError(f"Colunas obrigatórias ausentes: {missing}")

    # Processar dados...
    return df
```

### Separação de Responsabilidades

```python
# ✅ CORRETO: Funções fazem UMA coisa
def load_csv(path: str) -> pd.DataFrame:
    """Apenas carrega CSV."""
    return pd.read_csv(path, encoding='utf-8-sig', sep=';')

def validate_columns(df: pd.DataFrame, required: List[str]) -> bool:
    """Apenas valida colunas."""
    return all(col in df.columns for col in required)

def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Apenas processa."""
    # ...
    return df

# ❌ EVITAR: Função que faz tudo
def load_validate_and_process(path: str) -> pd.DataFrame:
    """Faz muitas coisas (difícil de testar e manter)."""
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError()
    # processar...
    return df
```

### DRY (Don't Repeat Yourself)

```python
# ✅ CORRETO: Extrair lógica repetida
def create_table(ws, data, table_name, start_cell, end_cell):
    """Função reutilizável para criar tabelas."""
    tab = Table(displayName=table_name, ref=f"{start_cell}:{end_cell}")
    tab.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium12",
        showRowStripes=True
    )
    ws.add_table(tab)

# Usar em múltiplas planilhas
create_table(ws1, data1, "inscritos", "A1", "F100")
create_table(ws2, data2, "mensagens", "A1", "H500")

# ❌ EVITAR: Copiar e colar o mesmo código
# Código duplicado em create_inscritos_sheet, create_mensagens_sheet, etc.
```

---

## 🔄 Controle de Versão

### Git Commit Messages

Siga o padrão **Conventional Commits**:

```
tipo(escopo): descrição curta

Descrição detalhada (opcional)

Rodapé (opcional)
```

#### Tipos de Commit

- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Alteração em documentação
- `style`: Formatação (sem mudança de código)
- `refactor`: Refatoração de código
- `test`: Adicionar/modificar testes
- `chore`: Tarefas de build, dependências, etc.

#### Exemplos

```bash
# ✅ CORRETO
feat(excel): adicionar gráfico de barras na planilha Retencao
fix(csv): corrigir encoding para arquivos com acentos
docs(readme): atualizar seção de instalação
refactor(process): simplificar cálculo de retenção
test(inscritos): adicionar teste para validação de colunas

# ✅ CORRETO: Commit com corpo
feat(export): adicionar exportação para PDF

Implementa geração de PDF usando reportlab.
Adiciona botão "Exportar PDF" na interface.

Closes #42

# ❌ EVITAR
git commit -m "fix"
git commit -m "mudanças"
git commit -m "corrigindo bug do João"
```

### Branching Strategy

```
main (produção)
  ├── develop (desenvolvimento)
  │     ├── feature/adicionar-pdf-export
  │     ├── feature/melhorar-validacao
  │     └── fix/corrigir-calculo-retencao
  │
  └── hotfix/corrigir-crash-inicializacao
```

**Regras**:
- `main`: Código em produção (sempre estável)
- `develop`: Integração de features
- `feature/*`: Novas funcionalidades
- `fix/*`: Correções de bugs
- `hotfix/*`: Correções urgentes em produção

---

## 🧪 Testes

### Estrutura de Testes

```python
import unittest
import pandas as pd
from prsa_report_generator import VideoConferenceReportGenerator

class TestProcessInscritos(unittest.TestCase):
    """Testes para process_inscritos."""

    def setUp(self):
        """Configuração antes de cada teste."""
        self.app = VideoConferenceReportGenerator(None)
        self.df_mock = pd.DataFrame({
            'Nome': ['João', 'Maria'],
            'Login': ['11999999999', '11988888888'],
            'Município': ['São Paulo', 'Rio de Janeiro']
        })

    def test_renomeia_coluna_login(self):
        """Testa se coluna Login é renomeada para Celular."""
        result = self.app.process_inscritos(self.df_mock)
        self.assertIn('Celular', result.columns)
        self.assertNotIn('Login', result.columns)

    def test_levanta_erro_se_vazio(self):
        """Testa se ValueError é levantado para DataFrame vazio."""
        df_vazio = pd.DataFrame()
        with self.assertRaises(ValueError):
            self.app.process_inscritos(df_vazio)

if __name__ == '__main__':
    unittest.main()
```

### Nomenclatura de Testes

```python
# ✅ CORRETO: Nome descritivo do que está sendo testado
def test_process_inscritos_renomeia_login_para_celular(self):
    pass

def test_load_csv_levanta_erro_se_arquivo_nao_existe(self):
    pass

# ❌ EVITAR: Nomes genéricos
def test_1(self):
    pass

def test_process(self):
    pass
```

### Cobertura de Testes

**Meta**: Mínimo **80% de cobertura** de código

**Prioridade de testes**:
1. ✅ Funções de processamento de dados
2. ✅ Validações críticas
3. ✅ Cálculos complexos (retenção, etc.)
4. ⚠️ Geração de Excel (difícil de testar)
5. ⚠️ UI Tkinter (difícil de testar)

---

## 📋 Checklist de Code Review

Antes de fazer commit, verifique:

- [ ] Código segue PEP 8
- [ ] Funções têm docstrings
- [ ] Type hints adicionados (quando aplicável)
- [ ] Tratamento de erros adequado
- [ ] Sem código duplicado (DRY)
- [ ] Nomes descritivos de variáveis/funções
- [ ] Comentários explicam "por quê", não "o quê"
- [ ] Testes passam (se houver)
- [ ] Sem prints de debug esquecidos
- [ ] Imports organizados
- [ ] Commit message segue padrão

---

## 🛠️ Ferramentas Recomendadas

### Linters e Formatters

```bash
# Black (formatador automático)
pip install black
black prsa_report_generator.py

# Flake8 (linter)
pip install flake8
flake8 prsa_report_generator.py

# mypy (type checker)
pip install mypy
mypy prsa_report_generator.py

# isort (organizar imports)
pip install isort
isort prsa_report_generator.py
```

### Configuração (pyproject.toml)

```toml
[tool.black]
line-length = 88
target-version = ['py38']

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
```

---

**Documento mantido por**: Equipe de Desenvolvimento PRSA
**Última atualização**: 29/01/2025
