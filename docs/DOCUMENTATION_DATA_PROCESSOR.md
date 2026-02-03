# ReportDataProcessor - Documentacao

## Visao Geral

O arquivo `core/data_processor.py` contem a classe `ReportDataProcessor`, responsavel por processar e transformar DataFrames brutos em DataFrames prontos para exportacao Excel.

## Localizacao

```
c:\Users\ferna\Desktop\App Estatisticas\core\data_processor.py
```

## Classe: ReportDataProcessor

### Responsabilidades

1. Normalizar nomes de colunas (ex: "Login" -> "Celular")
2. Calcular metricas de tempo e retencao
3. Selecionar colunas relevantes de forma flexivel
4. Transformar dados em formato adequado para Excel
5. Reportar progresso via callback opcional

### Inicializacao

```python
from core.data_processor import ReportDataProcessor

# Com callback de progresso
def progress_callback(message: str):
    print(f"[LOG] {message}")

processor = ReportDataProcessor(progress_callback=progress_callback)

# Sem callback
processor = ReportDataProcessor()
```

### Metodo Principal: process_all()

Processa todos os DataFrames necessarios para o relatorio.

**Parametros:**
- `dfs: Dict[str, pd.DataFrame]` - Dicionario com DataFrames brutos

**Chaves esperadas:**
- `'inscritos'` - DataFrame de inscritos
- `'relatorio_acesso'` - DataFrame de relatorio de acesso
- `'mensagens'` - DataFrame de mensagens
- `'totalizado'` - DataFrame totalizado (retencao na live)

**Retorna:**
- `Dict[str, pd.DataFrame]` - Dicionario com DataFrames processados

**Chaves retornadas:**
- `'inscritos_processed'`
- `'relatorio_processed'`
- `'mensagens_processed'`
- `'totalizado_processed'`

**Exemplo de uso:**

```python
raw_data = {
    'inscritos': df_inscritos,
    'relatorio_acesso': df_relatorio,
    'mensagens': df_mensagens,
    'totalizado': df_totalizado
}

processed_data = processor.process_all(raw_data)

# Acessar dados processados
inscritos = processed_data['inscritos_processed']
relatorio = processed_data['relatorio_processed']
```

## Metodos Privados

### _process_inscritos()

**Operacoes:**
1. Renomeia 'Login' para 'Celular'
2. Renomeia coluna LGPD longa
3. Renomeia 'Comunidade.1' para 'Comunidade2'
4. Seleciona colunas relevantes

**Colunas obrigatorias:**
- Nome

**Colunas opcionais:**
- Celular
- Municipio
- Comunidade
- Estado
- Cidade
- Sou
- Sobrenome
- Comunidade2
- As informacoes pessoais coletadas
- Data de Cadastro

### _process_relatorio_acesso()

**Operacoes:**
1. Renomeia 'Login' para 'Celular'
2. Renomeia coluna LGPD longa
3. Renomeia 'Comunidade.1' para 'Comunidade_1' (nota: diferente de inscritos)
4. **Calcula tempo de retencao** (hh:mm:ss)
5. Seleciona colunas relevantes

**Modos de calculo de retencao:**

**Modo 1: Coluna 'Tempo' existe (em minutos)**
```python
# Exemplo: 125.5 minutos -> "2:05:00"
df['Retencao (hh:mm)'] = df['Tempo'].apply(TimeCalculator.format_minutes_to_time)
```

**Modo 2: Colunas de data inicial e final**
```python
# Exemplo: 14:00:00 a 15:35:45 -> "1:35:45"
def calc_retention(row):
    return TimeCalculator.calculate_time_from_dates(
        row['Data Acesso Inicial'],
        row['Data Acesso Final']
    )

df['Retencao (hh:mm)'] = df.apply(calc_retention, axis=1)
```

**Colunas obrigatorias:**
- Nome

**Colunas opcionais:**
- Celular
- Municipio
- Comunidade
- Estado
- Cidade
- Comunidade_1
- As informacoes pessoais coletadas
- Conteudo
- Retencao (hh:mm) - criada durante processamento
- Tempo_Minutos

### _process_mensagens()

**Operacoes:**
1. Renomeia coluna LGPD longa
2. Renomeia 'Comunidade.1' para 'Comunidade2'
3. Seleciona colunas relevantes

**Colunas obrigatorias:**
- Nome

**Colunas opcionais:**
- Municipio
- Comunidade
- Estado
- Cidade
- Sou
- Sobrenome
- Comunidade2
- Conteudo
- As informacoes pessoais coletadas
- Remetente
- Email
- Mensagem
- Data

### _process_totalizado()

**Operacoes:**
1. Converte coluna 'Data' para datetime
2. Mantem estrutura original

**Nota:** A coluna 'Max' NAO e criada aqui - sera calculada com formula no Excel.

**Colunas esperadas:**
- Data (convertida para datetime64[ns])
- Usuarios conectados

## Dependencias

### Modulos utilizados:
- `utils.dataframe_helpers.DataFrameHelper` - Normalizacao e selecao de colunas
- `utils.time_calculator.TimeCalculator` - Calculos de tempo
- `config.column_mappings` - Mapas de renomeacao e listas de colunas
- `config.settings` - Constantes e configuracoes

### Metodos do DataFrameHelper:
- `normalize_columns(df, renames)` - Renomeia colunas
- `select_available_columns(df, required, optional)` - Seleciona colunas disponiveis

### Metodos do TimeCalculator:
- `format_minutes_to_time(minutes)` - Converte minutos para HH:MM:SS
- `calculate_time_from_dates(inicial, final)` - Calcula diferenca entre datas

## Configuracoes Utilizadas

### column_mappings.COLUMN_RENAMES
```python
{
    'Login': 'Celular',
    'Comunidade.1': 'Comunidade2',
    'As informacoes pessoais coletadas [texto longo]': 'As informacoes pessoais coletadas'
}
```

### column_mappings.REQUIRED_COLUMNS
```python
{
    'inscritos': ['Nome'],
    'mensagens': ['Nome'],
    'relatorio_acesso': ['Nome'],
    'totalizado': ['Data', 'Usuarios conectados']
}
```

### column_mappings.OPTIONAL_COLUMNS
Listas de colunas opcionais por tipo de DataFrame.

### settings
Constantes como:
- `DATE_FORMAT = '%d/%m/%Y %H:%M:%S'`
- `COL_RETENCAO = 'Retencao (hh:mm)'`
- `COL_TEMPO = 'Tempo'`
- etc.

## Tratamento de Erros

O processador e robusto e lida com:
- Colunas ausentes (usa apenas as disponiveis)
- Valores nulos em calculos de tempo (retorna "0:00:00")
- Formatos de data invalidos (trata com try/except)
- DataFrames vazios

## Testes

Dois scripts de teste foram criados:

1. `test_data_processor.py` - Testa modo com coluna 'Tempo'
2. `test_data_processor_dates.py` - Testa modo com datas inicial/final

**Executar testes:**
```bash
python test_data_processor.py
python test_data_processor_dates.py
```

## Exemplo Completo

```python
import pandas as pd
from core.data_processor import ReportDataProcessor

# Criar dados de exemplo
raw_data = {
    'inscritos': pd.DataFrame({
        'Nome': ['Joao Silva'],
        'Login': ['31999887766']
    }),
    'relatorio_acesso': pd.DataFrame({
        'Nome': ['Joao Silva'],
        'Login': ['31999887766'],
        'Tempo': [125.5]
    }),
    'mensagens': pd.DataFrame({
        'Nome': ['Joao Silva'],
        'Mensagem': ['Otima apresentacao!']
    }),
    'totalizado': pd.DataFrame({
        'Data': ['29/01/2025 14:00:00'],
        'Usuarios conectados': [100]
    })
}

# Processar
processor = ReportDataProcessor()
processed = processor.process_all(raw_data)

# Usar dados processados
print(processed['inscritos_processed'])
# Output:
#          Nome      Celular
# 0  Joao Silva  31999887766

print(processed['relatorio_processed'])
# Output:
#          Nome      Celular  Retencao (hh:mm)
# 0  Joao Silva  31999887766          2:05:00
```

## Diferenca do Codigo Original

O codigo foi refatorado do metodo `process_data()` em `prsa_report_generator.py` (linhas 214-380) com as seguintes melhorias:

1. **Separacao de responsabilidades:** Cada tipo de DataFrame tem seu metodo privado
2. **Reutilizacao de codigo:** Usa helpers em vez de logica duplicada
3. **Type hints completos:** Todas funcoes tem anotacoes de tipo
4. **Docstrings detalhadas:** Documentacao em todas funcoes publicas
5. **Configuracao centralizada:** Usa arquivos de config em vez de strings hardcoded
6. **Testabilidade:** Classe independente facil de testar
7. **Callback de progresso:** Interface clara para reportar status
8. **Tratamento de erros melhorado:** Validacoes e mensagens claras

## Integracao

A classe pode ser usada em:
- Interface grafica (GUI)
- Scripts de linha de comando
- Notebooks Jupyter
- Testes automatizados
- APIs

Basta fornecer o dicionario de DataFrames e receber os dados processados.
