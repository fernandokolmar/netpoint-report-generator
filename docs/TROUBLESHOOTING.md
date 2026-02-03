# ❗ Guia de Solução de Problemas - Gerador de Relatórios PRSA

Guia completo para diagnosticar e resolver problemas comuns do sistema.

---

## 📋 Índice

- [Problemas de Instalação](#-problemas-de-instalação)
- [Problemas de Carregamento de Arquivos](#-problemas-de-carregamento-de-arquivos)
- [Problemas de Processamento](#-problemas-de-processamento)
- [Problemas de Geração de Excel](#-problemas-de-geração-de-excel)
- [Problemas de Performance](#-problemas-de-performance)
- [FAQs](#-faqs-perguntas-frequentes)
- [Debugging Avançado](#-debugging-avançado)

---

## 🔧 Problemas de Instalação

### Problema: "Python não é reconhecido como comando"

**Sintomas**:
```bash
> python --version
'python' não é reconhecido como um comando interno ou externo
```

**Causa**: Python não está instalado ou não está no PATH do sistema

**Solução Windows**:
1. Baixe Python em [python.org](https://www.python.org/downloads/)
2. Durante instalação, **marque** "Add Python to PATH"
3. Reinstale se necessário
4. Reinicie o terminal

**Solução Linux/Mac**:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip

# macOS (Homebrew)
brew install python3
```

**Verificar**:
```bash
python --version  # ou python3 --version
```

---

### Problema: "ModuleNotFoundError: No module named 'pandas'"

**Sintomas**:
```python
ModuleNotFoundError: No module named 'pandas'
```

**Causa**: Dependências não foram instaladas

**Solução**:
```bash
# Instalar todas as dependências
pip install -r requirements.txt

# Ou instalar individualmente
pip install pandas numpy openpyxl
```

**Verificar Instalação**:
```python
python -c "import pandas; print(pandas.__version__)"
python -c "import openpyxl; print(openpyxl.__version__)"
```

---

### Problema: "No module named 'tkinter'"

**Sintomas**:
```python
ModuleNotFoundError: No module named 'tkinter'
```

**Causa**: Tkinter não está instalado (comum em Linux)

**Solução Linux**:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

**Solução macOS**:
```bash
# Reinstalar Python com Homebrew
brew reinstall python-tk
```

**Verificar**:
```python
python -c "import tkinter; print('Tkinter OK')"
```

---

## 📂 Problemas de Carregamento de Arquivos

### Problema: "UnicodeDecodeError" ao carregar CSV

**Sintomas**:
```python
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0
```

**Causa**: Arquivo CSV não está em UTF-8

**Diagnóstico**:
```bash
# Ver encoding do arquivo (Linux/Mac)
file -I arquivo.csv

# Ver primeiros bytes
head -c 50 arquivo.csv | xxd
```

**Solução 1**: Converter para UTF-8 no Excel
1. Abra o CSV no Excel
2. Arquivo → Salvar Como
3. Escolha "CSV UTF-8 (delimitado por vírgulas) (*.csv)"
4. Salvar

**Solução 2**: Converter programaticamente
```python
import pandas as pd

# Ler com encoding original
df = pd.read_csv('arquivo.csv', encoding='latin1', sep=';')

# Salvar em UTF-8 com BOM
df.to_csv('arquivo_utf8.csv', encoding='utf-8-sig', sep=';', index=False)
```

**Solução 3**: Modificar encoding no código (temporário)
```python
# Testar diferentes encodings
encodings = ['utf-8-sig', 'utf-8', 'latin1', 'cp1252']

for enc in encodings:
    try:
        df = pd.read_csv(arquivo, encoding=enc, sep=';')
        print(f"✓ Funcionou com encoding: {enc}")
        break
    except:
        print(f"✗ Falhou com encoding: {enc}")
```

---

### Problema: "ParserError: Error tokenizing data"

**Sintomas**:
```python
pandas.errors.ParserError: Error tokenizing data. C error: Expected X fields in line Y, saw Z
```

**Causa**: Separador incorreto ou dados mal formatados

**Diagnóstico**:
```python
# Ver primeiras linhas do arquivo
with open('arquivo.csv', 'r', encoding='utf-8-sig') as f:
    for i, line in enumerate(f, 1):
        print(f"Linha {i}: {line}")
        if i >= 5:
            break
```

**Solução 1**: Verificar separador
```python
# Testar diferentes separadores
separadores = [';', ',', '\t', '|']

for sep in separadores:
    try:
        df = pd.read_csv(arquivo, encoding='utf-8-sig', sep=sep)
        print(f"✓ Funcionou com separador: '{sep}'")
        print(f"Colunas: {df.columns.tolist()}")
        break
    except:
        print(f"✗ Falhou com separador: '{sep}'")
```

**Solução 2**: Ler linha por linha
```python
# Encontrar linha problemática
with open('arquivo.csv', 'r', encoding='utf-8-sig') as f:
    for i, line in enumerate(f, 1):
        campos = line.split(';')
        if len(campos) != numero_esperado_colunas:
            print(f"Linha {i} tem {len(campos)} campos (esperado {numero_esperado_colunas})")
            print(f"Conteúdo: {line}")
```

---

### Problema: "FileNotFoundError"

**Sintomas**:
```python
FileNotFoundError: [Errno 2] No such file or directory: 'Inscritos.csv'
```

**Causa**: Caminho do arquivo está incorreto

**Diagnóstico**:
```python
import os

# Verificar se arquivo existe
caminho = 'C:\\Users\\ferna\\Desktop\\Inscritos.csv'
print(f"Arquivo existe? {os.path.exists(caminho)}")

# Listar arquivos no diretório
diretorio = 'C:\\Users\\ferna\\Desktop'
arquivos = os.listdir(diretorio)
print(f"Arquivos CSV: {[f for f in arquivos if f.endswith('.csv')]}")
```

**Solução**:
1. Use caminho absoluto em vez de relativo
2. Verifique se o arquivo está no diretório correto
3. Certifique-se de usar barras corretas (`\\` no Windows ou `/`)

---

## 🔄 Problemas de Processamento

### Problema: "KeyError: 'Nome'"

**Sintomas**:
```python
KeyError: 'Nome'
```

**Causa**: Coluna obrigatória está ausente no CSV

**Diagnóstico**:
```python
# Ver todas as colunas do DataFrame
df = pd.read_csv('arquivo.csv', encoding='utf-8-sig', sep=';')
print("Colunas encontradas:")
for i, col in enumerate(df.columns):
    print(f"  {i}: '{col}'")
```

**Solução 1**: Verificar se cabeçalho está correto no CSV

**Solução 2**: Renomear coluna
```python
# Se coluna tem nome parecido
df.rename(columns={'name': 'Nome', 'Nomes': 'Nome'}, inplace=True)
```

**Solução 3**: Tornar coluna opcional no código
```python
# Em vez de:
cols = ['Nome', 'Celular']

# Usar:
cols = []
if 'Nome' in df.columns:
    cols.append('Nome')
if 'Celular' in df.columns:
    cols.append('Celular')
```

---

### Problema: "ValueError: time data does not match format"

**Sintomas**:
```python
ValueError: time data '18-11-2025 19:00' does not match format '%d/%m/%Y %H:%M:%S'
```

**Causa**: Formato de data no CSV está diferente do esperado

**Diagnóstico**:
```python
# Ver formato real das datas
df = pd.read_csv('arquivo.csv', encoding='utf-8-sig', sep=';')
print("Primeiras datas:")
print(df['Data'].head())
```

**Solução 1**: Ajustar formato no código
```python
# Testar diferentes formatos
formatos = [
    '%d/%m/%Y %H:%M:%S',  # 18/11/2025 19:00:00
    '%d-%m-%Y %H:%M',     # 18-11-2025 19:00
    '%Y-%m-%d %H:%M:%S',  # 2025-11-18 19:00:00
    '%d/%m/%Y %H:%M',     # 18/11/2025 19:00
]

for fmt in formatos:
    try:
        df['Data'] = pd.to_datetime(df['Data'], format=fmt)
        print(f"✓ Formato correto: {fmt}")
        break
    except:
        print(f"✗ Não é: {fmt}")
```

**Solução 2**: Usar inferência automática
```python
# Pandas tenta descobrir o formato
df['Data'] = pd.to_datetime(df['Data'], infer_datetime_format=True)
```

---

### Problema: Cálculo de Retenção retorna valores errados

**Sintomas**:
- Retenção mostra "00:00:00" para todos
- Retenção mostra valores negativos
- Retenção mostra valores absurdamente altos

**Diagnóstico**:
```python
# Verificar valores de entrada
print("Coluna 'Tempo':")
print(df['Tempo'].describe())

print("\nPrimeiros valores de Data Inicial e Final:")
print(df[['Data Inicial', 'Data Final']].head())

# Verificar tipo de dado
print(f"\nTipo de 'Tempo': {df['Tempo'].dtype}")
print(f"Tipo de 'Data Inicial': {df['Data Inicial'].dtype}")
```

**Solução (Cenário 1 - Tempo em minutos)**:
```python
# Garantir que Tempo é numérico
df['Tempo'] = pd.to_numeric(df['Tempo'], errors='coerce')

# Calcular retenção
df['Retenção (hh:mm)'] = df['Tempo'].apply(
    lambda x: f"{int(x)//60:02d}:{int(x)%60:02d}:00" if pd.notna(x) else "00:00:00"
)
```

**Solução (Cenário 2 - Datas)**:
```python
# Garantir que são datetime
df['Data Inicial'] = pd.to_datetime(df['Data Inicial'], format='%d/%m/%Y %H:%M:%S')
df['Data Final'] = pd.to_datetime(df['Data Final'], format='%d/%m/%Y %H:%M:%S')

# Calcular diferença
df['Diferenca'] = df['Data Final'] - df['Data Inicial']

# Verificar se há valores negativos
print(f"Valores negativos: {(df['Diferenca'] < pd.Timedelta(0)).sum()}")

# Converter para HH:MM:SS
df['Retenção (hh:mm)'] = df['Diferenca'].apply(
    lambda x: f"{x.seconds//3600:02d}:{(x.seconds//60)%60:02d}:{x.seconds%60:02d}"
    if pd.notna(x) else "00:00:00"
)
```

---

## 📊 Problemas de Geração de Excel

### Problema: "PermissionError" ao salvar Excel

**Sintomas**:
```python
PermissionError: [Errno 13] Permission denied: 'C:\\...\\Relatorio.xlsx'
```

**Causa**: Arquivo está aberto no Excel ou sem permissão de escrita

**Solução 1**: Fechar Excel
1. Feche o arquivo Excel se estiver aberto
2. Tente gerar novamente

**Solução 2**: Salvar com outro nome
1. Use nome diferente
2. Ou salve em outro diretório

**Solução 3**: Verificar permissões
```python
import os

# Verificar permissões de escrita
diretorio = 'C:\\Users\\ferna\\Desktop'
print(f"Pode escrever? {os.access(diretorio, os.W_OK)}")
```

---

### Problema: Fórmulas retornam "#REF!" no Excel

**Sintomas**:
- Células com fórmulas mostram #REF!
- Resumo estatístico não funciona

**Causa**: Nomes de tabelas ou referências incorretas

**Diagnóstico**:
```python
# Verificar nomes de tabelas no Excel gerado
from openpyxl import load_workbook

wb = load_workbook('Relatorio.xlsx')
for ws in wb.worksheets:
    print(f"Planilha: {ws.title}")
    for table in ws.tables.values():
        print(f"  Tabela: {table.name}")
```

**Solução**:
1. Verificar se tabelas estão nomeadas corretamente:
   - `retencao`
   - `mensagens`
   - `Relatorio_de_acesso12`
   - `inscritos`

2. Verificar se colunas existem nas tabelas

---

### Problema: Gráfico não aparece no Excel

**Sintomas**:
- Planilha "Retencao na live" não tem gráfico
- Gráfico aparece vazio

**Diagnóstico**:
```python
# Verificar se dados estão presentes
df = dataframes['totalizado']
print(f"Total de linhas: {len(df)}")
print(f"Colunas: {df.columns.tolist()}")
print(f"Valores de 'Usuarios conectados':\n{df['Usuarios conectados'].describe()}")
```

**Solução**:
1. Verificar se DataFrame totalizado tem pelo menos 2 linhas
2. Verificar se coluna "Usuarios conectados" tem valores numéricos
3. Verificar se coluna "Data" está presente

---

## ⚡ Problemas de Performance

### Problema: Processamento muito lento

**Sintomas**:
- Carregamento de CSV demora muito
- Processamento trava

**Diagnóstico**:
```python
import time

# Medir tempo de cada etapa
inicio = time.time()

df = pd.read_csv('arquivo.csv', encoding='utf-8-sig', sep=';')
print(f"Carregamento: {time.time() - inicio:.2f}s")

inicio = time.time()
df_processado = process_inscritos(df)
print(f"Processamento: {time.time() - inicio:.2f}s")
```

**Solução 1**: Verificar tamanho do arquivo
```python
import os

tamanho_mb = os.path.getsize('arquivo.csv') / (1024 * 1024)
print(f"Tamanho: {tamanho_mb:.2f} MB")

# Se > 100 MB, considerar chunking
```

**Solução 2**: Usar chunking para arquivos grandes
```python
chunks = []
for chunk in pd.read_csv('arquivo.csv', chunksize=10000,
                         encoding='utf-8-sig', sep=';'):
    chunks.append(chunk)

df = pd.concat(chunks, ignore_index=True)
```

**Solução 3**: Otimizar processamento
```python
# Em vez de apply linha por linha
df['Retenção'] = df['Tempo'].apply(lambda x: calcular(x))

# Use operações vetorizadas
minutos = df['Tempo']
horas = minutos // 60
mins = minutos % 60
df['Retenção'] = horas.astype(str).str.zfill(2) + ':' + mins.astype(str).str.zfill(2)
```

---

### Problema: Aplicação trava (não responde)

**Sintomas**:
- Interface congela
- Não é possível clicar em nada

**Causa**: Processamento pesado no thread principal (Tkinter)

**Solução** (não implementado, mas recomendado):
```python
import threading

def processar_em_background():
    # Processar dados
    # ...

# Executar em thread separada
thread = threading.Thread(target=processar_em_background)
thread.start()
```

---

## ❓ FAQs (Perguntas Frequentes)

### Q: Qual o tamanho máximo de arquivo CSV suportado?

**A**: Depende da memória RAM disponível. Recomendado:
- Até 100 MB: Sem problemas
- 100-500 MB: Pode ficar lento
- > 500 MB: Considerar chunking ou otimização

---

### Q: Posso usar vírgula como separador em vez de ponto-e-vírgula?

**A**: Sim, mas precisa modificar o código:

```python
# Alterar em load_dataframes()
df = pd.read_csv(path, encoding='utf-8-sig', sep=',')  # Mudado de ';' para ','
```

---

### Q: Como processar múltiplos eventos de uma vez?

**A**: Atualmente não suportado. Opções:
1. Executar aplicação múltiplas vezes
2. Modificar código para loop:

```python
eventos = ['evento1', 'evento2', 'evento3']

for evento in eventos:
    carregar_csvs(evento)
    processar()
    gerar_excel(f'relatorio_{evento}.xlsx')
```

---

### Q: Posso exportar para PDF em vez de Excel?

**A**: Não nativamente. Opções:
1. Abrir Excel gerado e salvar como PDF manualmente
2. Implementar exportação PDF (requer biblioteca adicional):

```python
pip install openpyxl-to-pdf

# Código adicional necessário
```

---

### Q: Como validar dados antes de processar?

**A**: Adicione validações antes de `process_data()`:

```python
def validar_inscritos(df):
    # Verificar se Nome e Celular existem
    if 'Nome' not in df.columns:
        raise ValueError("Coluna 'Nome' ausente")

    # Verificar se há dados
    if df.empty:
        raise ValueError("DataFrame vazio")

    # Verificar se há duplicatas
    duplicatas = df.duplicated(subset=['Nome'], keep=False)
    if duplicatas.any():
        print(f"Atenção: {duplicatas.sum()} registros duplicados")

    return True
```

---

## 🔍 Debugging Avançado

### Habilitar Logs Detalhados

```python
import logging

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='prsa_debug.log'
)

logger = logging.getLogger(__name__)

# Usar em funções
def process_inscritos(df):
    logger.debug(f"Iniciando processamento de {len(df)} inscritos")
    logger.debug(f"Colunas: {df.columns.tolist()}")
    # ...
    logger.debug("Processamento concluído")
```

### Inspecionar DataFrames

```python
# Ver informações completas
df.info()

# Ver estatísticas
df.describe(include='all')

# Ver primeiras e últimas linhas
print(df.head(10))
print(df.tail(10))

# Ver valores únicos de coluna
print(df['Município'].value_counts())

# Verificar valores nulos
print(df.isnull().sum())

# Ver tipos de dados
print(df.dtypes)
```

### Salvar DataFrames Intermediários

```python
# Salvar após cada etapa para debug
df_bruto = pd.read_csv('Inscritos.csv', encoding='utf-8-sig', sep=';')
df_bruto.to_csv('debug_01_bruto.csv', index=False)

df_processado = process_inscritos(df_bruto)
df_processado.to_csv('debug_02_processado.csv', index=False)
```

### Usar Python Debugger (pdb)

```python
import pdb

def process_inscritos(df):
    # Pausar execução aqui
    pdb.set_trace()

    # Continuar código...
```

**Comandos do pdb**:
- `n` - Próxima linha
- `s` - Entrar em função
- `c` - Continuar até breakpoint
- `p variavel` - Printar variável
- `l` - Listar código ao redor
- `q` - Sair

---

## 📞 Quando Pedir Ajuda

Se nenhuma solução acima funcionou:

1. **Colete informações**:
   ```bash
   python --version
   pip list | grep -E "pandas|openpyxl|numpy"
   ```

2. **Salve logs de erro**:
   - Copie mensagem de erro completa
   - Inclua traceback completo

3. **Descreva o problema**:
   - O que você estava fazendo
   - O que esperava que acontecesse
   - O que realmente aconteceu
   - Arquivos de exemplo (se possível)

4. **Entre em contato** com a equipe de desenvolvimento PRSA

---

**Documento mantido por**: Equipe de Desenvolvimento PRSA
**Última atualização**: 29/01/2025
