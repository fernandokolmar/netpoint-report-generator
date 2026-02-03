# 📊 Especificação de Formatos de Dados - Gerador de Relatórios PRSA

Este documento descreve detalhadamente a estrutura de todos os arquivos de entrada (CSV) e saída (Excel) do sistema.

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Arquivos CSV de Entrada](#-arquivos-csv-de-entrada)
- [Arquivo Excel de Saída](#-arquivo-excel-de-saída)
- [Regras de Validação](#-regras-de-validação)
- [Casos Especiais](#-casos-especiais)
- [Exemplos Completos](#-exemplos-completos)

---

## 🎯 Visão Geral

### Formatos Suportados

| Direção | Formato | Encoding | Separador | Obrigatório |
|---------|---------|----------|-----------|-------------|
| **Entrada** | CSV | UTF-8 com BOM | `;` (ponto-e-vírgula) | ✅ Sim (4 arquivos) |
| **Saída** | XLSX (Excel) | N/A | N/A | ✅ Sim (1 arquivo) |

### Fluxo de Dados

```
[Inscritos.csv]    ─┐
[Mensagens.csv]    ─┤
[Relatório.csv]    ─┼─→ [PROCESSAMENTO] ─→ [Relatorio_YYYYMMDD.xlsx]
[Totalizado.csv]   ─┘
```

---

## 📥 Arquivos CSV de Entrada

### Especificações Gerais

**Todas os CSVs devem seguir**:

```yaml
Encoding: UTF-8 com BOM (utf-8-sig)
Separador: ; (ponto-e-vírgula)
Extensão: .csv
Cabeçalho: Primeira linha (obrigatório)
Formato de Data: DD/MM/YYYY HH:MM:SS
Formato Numérico: Vírgula como decimal (padrão brasileiro)
```

### Validação Automática

A aplicação **automaticamente**:
- ✅ Remove BOM (Byte Order Mark) se presente
- ✅ Detecta encoding UTF-8
- ✅ Usa ponto-e-vírgula como separador
- ✅ Infere tipos de dados (strings, números, datas)

---

## 1️⃣ Inscritos.csv

### Descrição

Lista de pessoas que se inscreveram no evento de videoconferência.

### Estrutura

| Coluna | Tipo | Obrigatória | Descrição | Exemplo |
|--------|------|-------------|-----------|---------|
| **Nome** | String | ✅ Sim | Nome completo do inscrito | `João Silva Santos` |
| **Login** | String | ✅ Sim | Telefone celular (será renomeado para "Celular") | `31987654321` |
| **Empresa** | String | ⚠️ Opcional | Empresa do inscrito | `Vale S.A.` |
| **Cargo** | String | ⚠️ Opcional | Cargo/função | `Analista` |
| **Município** | String | ⚠️ Recomendado | Município de residência | `Mariana` |
| **Comunidade** | String | ⚠️ Recomendado | Comunidade a que pertence | `Bento Rodrigues` |
| **Estado** | String | ⚠️ Opcional | Estado (UF) | `MG` |
| **Cidade** | String | ⚠️ Opcional | Cidade (alternativa a Município) | `Mariana` |
| **Sou** | String | ⚠️ Opcional | Auto-identificação | `Morador` |
| **Sobrenome** | String | ⚠️ Opcional | Sobrenome separado | `Silva` |
| **Data de Cadastro** | DateTime | ⚠️ Recomendado | Data/hora da inscrição | `18/11/2025 10:30:00` |
| **LGPD** | String | ⚠️ Opcional | Consentimento LGPD (`sim`/`não`) | `sim` |
| **Comunidade.1** | String | ⚠️ Opcional | Segunda comunidade (será renomeada para "Comunidade2") | `Centro` |

### Exemplo de Arquivo

```csv
Nome;Login;Empresa;Cargo;Município;Comunidade;Estado;Data de Cadastro;LGPD
João Silva Santos;31987654321;Vale S.A.;Analista;Mariana;Bento Rodrigues;MG;18/11/2025 10:30:00;sim
Maria Oliveira;21912345678;Prefeitura;Coordenadora;Mariana;Centro;MG;18/11/2025 11:15:22;sim
Pedro Costa;11998877665;;Autônomo;Ouro Preto;Passagem;MG;18/11/2025 12:45:10;não
```

### Transformações Aplicadas

1. **Renomeação de Coluna**:
   ```python
   'Login' → 'Celular'
   'Comunidade.1' → 'Comunidade2'
   ```

2. **Seleção de Colunas** (apenas as existentes):
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

3. **Validações**:
   - Se "Nome" ausente → Erro
   - Se "Login" ausente → Erro
   - Outras colunas ausentes → Ignora silenciosamente

---

## 2️⃣ Mensagens.csv

### Descrição

Mensagens enviadas pelos participantes durante a videoconferência.

### Estrutura

| Coluna | Tipo | Obrigatória | Descrição | Exemplo |
|--------|------|-------------|-----------|---------|
| **Nome** | String | ✅ Sim | Nome do remetente | `Maria Oliveira` |
| **Município** | String | ⚠️ Recomendado | Município do remetente | `Mariana` |
| **Comunidade** | String | ⚠️ Recomendado | Comunidade do remetente | `Bento Rodrigues` |
| **Conteúdo** | String | ⚠️ Opcional | Tipo de mensagem | `Pergunta` ou `Comentário` |
| **Remetente** | String | ⚠️ Opcional | Identificação adicional | `maria.oliveira` |
| **Email** | String | ⚠️ Opcional | E-mail do remetente | `maria@email.com` |
| **Mensagem** | String | ✅ Sim | Texto da mensagem | `Quando teremos a resposta?` |
| **Data** | DateTime | ✅ Sim | Data/hora de envio | `18/11/2025 19:45:12` |
| **As informações pessoais coletadas...** | String | ⚠️ Opcional | Campo LGPD (nome longo) | `sim` |

### Exemplo de Arquivo

```csv
Nome;Município;Comunidade;Conteúdo;Remetente;Email;Mensagem;Data
Maria Oliveira;Mariana;Bento Rodrigues;Pergunta;maria.oliveira;maria@email.com;Quando teremos a resposta?;18/11/2025 19:45:12
João Silva;Mariana;Centro;Comentário;joao.silva;joao@email.com;Muito esclarecedor!;18/11/2025 19:50:33
```

### Transformações Aplicadas

1. **Renomeação de Coluna LGPD**:
   ```python
   'As informações pessoais coletadas...' → 'As informações pessoais coletadas'
   ```

2. **Seleção de Colunas**:
   - Nome
   - Município
   - Comunidade
   - Conteúdo
   - Remetente
   - Email
   - Mensagem
   - Data
   - As informações pessoais coletadas

---

## 3️⃣ Relatório de acesso.csv

### Descrição

Relatório de participação individual com tempo de permanência na videoconferência.

### Estrutura

**⚠️ A aplicação suporta DOIS formatos diferentes:**

#### Cenário 1: Coluna "Tempo" (minutos)

| Coluna | Tipo | Obrigatória | Descrição | Exemplo |
|--------|------|-------------|-----------|---------|
| **Nome** | String | ✅ Sim | Nome do participante | `João Silva` |
| **Login** | String | ✅ Sim | Celular | `31987654321` |
| **Município** | String | ⚠️ Recomendado | Município | `Mariana` |
| **Comunidade** | String | ⚠️ Recomendado | Comunidade | `Bento Rodrigues` |
| **Tempo** | Número | ✅ Sim | Tempo em minutos | `45` |

**Exemplo**:
```csv
Nome;Login;Município;Comunidade;Tempo
João Silva;31987654321;Mariana;Bento Rodrigues;45
Maria Oliveira;21912345678;Mariana;Centro;62
```

#### Cenário 2: Data Inicial + Data Final

| Coluna | Tipo | Obrigatória | Descrição | Exemplo |
|--------|------|-------------|-----------|---------|
| **Nome** | String | ✅ Sim | Nome do participante | `João Silva` |
| **Login** | String | ✅ Sim | Celular | `31987654321` |
| **Município** | String | ⚠️ Recomendado | Município | `Mariana` |
| **Comunidade** | String | ⚠️ Recomendado | Comunidade | `Bento Rodrigues` |
| **Data Inicial** | DateTime | ✅ Sim | Entrada na live | `18/11/2025 19:00:00` |
| **Data Final** | DateTime | ✅ Sim | Saída da live | `18/11/2025 19:45:00` |

**Exemplo**:
```csv
Nome;Login;Município;Comunidade;Data Inicial;Data Final
João Silva;31987654321;Mariana;Bento Rodrigues;18/11/2025 19:00:00;18/11/2025 19:45:00
Maria Oliveira;21912345678;Mariana;Centro;18/11/2025 19:10:00;18/11/2025 20:12:00
```

### Transformações Aplicadas

1. **Renomeação**:
   ```python
   'Login' → 'Celular'
   ```

2. **Cálculo de Retenção** (nova coluna):

   **Se Cenário 1** (coluna "Tempo" existe):
   ```python
   # Converter minutos para HH:MM:SS
   Retenção (hh:mm) = f"{int(tempo)//60:02d}:{int(tempo)%60:02d}:00"

   # Exemplo: 45 minutos → "00:45:00"
   ```

   **Se Cenário 2** (colunas "Data Inicial" e "Data Final"):
   ```python
   # Calcular diferença
   diferenca = Data Final - Data Inicial

   # Converter para HH:MM:SS
   Retenção (hh:mm) = f"{horas:02d}:{minutos:02d}:{segundos:02d}"

   # Exemplo: 19:00 até 19:45 → "00:45:00"
   ```

3. **Colunas Finais**:
   - Nome
   - Celular (ex-Login)
   - Município
   - Comunidade
   - Retenção (hh:mm) ← **NOVA COLUNA CALCULADA**

---

## 4️⃣ Totalizado.csv

### Descrição

Dados de audiência minuto a minuto (ou em intervalos regulares).

### Estrutura

| Coluna | Tipo | Obrigatória | Descrição | Exemplo |
|--------|------|-------------|-----------|---------|
| **Data** | DateTime | ✅ Sim | Data/hora da medição | `18/11/2025 19:00:00` |
| **Usuarios conectados** | Inteiro | ✅ Sim | Quantidade de usuários simultâneos | `150` |

### Exemplo de Arquivo

```csv
Data;Usuarios conectados
18/11/2025 19:00:00;150
18/11/2025 19:01:00;182
18/11/2025 19:02:00;201
18/11/2025 19:03:00;245
18/11/2025 19:04:00;238
18/11/2025 19:05:00;221
```

### Transformações Aplicadas

1. **Conversão de Data**:
   ```python
   df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y %H:%M:%S')
   ```

2. **Criação de Coluna "Max"** (vazia, preenchida por fórmula Excel):
   ```python
   df['Max'] = ''
   ```

3. **Colunas Finais**:
   - Data (convertida para datetime)
   - Usuarios conectados
   - Max (vazia, será preenchida no Excel)

---

## 📤 Arquivo Excel de Saída

### Estrutura Geral

```
Relatorio_Videoconferencia_YYYYMMDD_HHMMSS.xlsx
├── Planilha 1: "Retencao na live"
├── Planilha 2: "Mensagens"
├── Planilha 3: "Acessos"
└── Planilha 4: "Inscritos"
```

---

## 📊 Planilha 1: "Retencao na live"

### Conteúdo

1. **Tabela de Dados** (colunas A-C):
   - Data
   - Usuarios conectados
   - Max

2. **Gráfico LineChart** (posicionado à direita da tabela)

3. **Resumo Estatístico** (células Q2:R7):

| Célula | Métrica | Fórmula |
|--------|---------|---------|
| Q2 | Quantidade de Inscritos | - |
| R2 | - | `=inscritos[[#Totals],[Data de Cadastro]]` |
| Q3 | Usuários distintos na live | - |
| R3 | - | `=Relatório_de_acesso12[[#Totals],[Nome]]` |
| Q4 | Pico de audiência | - |
| R4 | - | `=MAX(retencao[Usuários conectados])` |
| Q5 | Hora de pico | - |
| R5 | - | `=_xlfn.XLOOKUP(R4,retencao[Usuários conectados],retencao[Data])` |
| Q6 | Tempo médio assistido (hh:mm) | - |
| R6 | - | `=Relatório_de_acesso12[[#Totals],[Retenção (hh:mm)]]` |
| Q7 | Total mensagens enviadas | - |
| R7 | - | `=mensagens[[#Totals],[Data]]` |

### Tabela Excel

```yaml
Nome da Tabela: retencao
Estilo: TableStyleMedium12
Linha Totalizadora: Habilitada
Filtros: Habilitados
```

### Gráfico

```yaml
Tipo: LineChart
Título: Retenção de Audiência ao Longo do Tempo
Eixo X: Data
Eixo Y: Usuarios conectados
Posição: Adjacente à tabela (coluna E)
```

---

## 📋 Planilha 2: "Mensagens"

### Estrutura

| Coluna | Conteúdo | Fórmula na Linha Total |
|--------|----------|------------------------|
| A | Nome | - |
| B | Município | - |
| C | Comunidade | - |
| D | Conteúdo | - |
| E | Remetente | - |
| F | Email | - |
| G | Mensagem | - |
| H | Data | `=SUBTOTAL(103, mensagens[Data])` |
| I | As informações pessoais coletadas | - |

### Tabela Excel

```yaml
Nome da Tabela: mensagens
Estilo: TableStyleMedium12
Linha Totalizadora: Habilitada (conta mensagens na coluna "Data")
Filtros: Habilitados
```

---

## 📝 Planilha 3: "Acessos"

### Estrutura

| Coluna | Conteúdo | Fórmula na Linha Total |
|--------|----------|------------------------|
| A | Nome | `=SUBTOTAL(103, Relatorio_de_acesso12[Nome])` |
| B | Celular | - |
| C | Município | - |
| D | Comunidade | - |
| E-G | (Outras colunas se existirem) | - |
| H | Retenção (hh:mm) | `=SUBTOTAL(101, Relatorio_de_acesso12[Retenção (hh:mm)])` |

### Tabela Excel

```yaml
Nome da Tabela: Relatorio_de_acesso12
Estilo: TableStyleMedium12
Linha Totalizadora: Habilitada
  - Coluna Nome: Conta registros (SUBTOTAL 103)
  - Coluna Retenção: Soma tempos (SUBTOTAL 101)
Filtros: Habilitados
```

---

## 👥 Planilha 4: "Inscritos"

### Estrutura

Todas as colunas do CSV processado + linha totalizadora.

| Última Coluna | Fórmula na Linha Total |
|---------------|------------------------|
| Data de Cadastro | `=SUBTOTAL(103, inscritos[Data de Cadastro])` |

### Tabela Excel

```yaml
Nome da Tabela: inscritos
Estilo: TableStyleMedium12
Linha Totalizadora: Habilitada (conta inscritos)
Filtros: Habilitados
```

---

## ✅ Regras de Validação

### Validações na Entrada

| Validação | Ação se Falhar |
|-----------|----------------|
| 4 arquivos selecionados | Erro: "Selecione todos os 4 arquivos" |
| Arquivo existe | Erro: "Arquivo não encontrado: [caminho]" |
| Encoding UTF-8 | Tenta ler mesmo assim (pode falhar) |
| Separador `;` | Tenta ler mesmo assim (pode falhar) |
| Colunas obrigatórias | Erro específico: "Coluna X não encontrada" |
| DataFrame vazio | Aviso no log, continua processamento |

### Validações Durante Processamento

| Validação | Ação se Falhar |
|-----------|----------------|
| Data em formato correto | Erro: "Formato de data inválido" |
| Números são numéricos | Pandas converte automaticamente |
| Tempo > 0 | Aceita qualquer valor (incluindo 0) |

---

## 🔄 Casos Especiais

### Caso 1: Coluna "Comunidade.1" no CSV de Inscritos

**Situação**: Excel às vezes duplica nomes de colunas como "Comunidade.1"

**Tratamento**:
```python
if 'Comunidade.1' in df.columns:
    df.rename(columns={'Comunidade.1': 'Comunidade2'}, inplace=True)
```

**Resultado**: Coluna aparece como "Comunidade2" no Excel final

### Caso 2: Coluna LGPD com Nome Muito Longo

**Nome completo**:
```
"As informações pessoais coletadas (nome, telefone, e-mail, cidade e etc.) e divulgadas nesta videoconferência poderão ser utilizadas?"
```

**Tratamento**:
```python
lgpd_col = 'As informações pessoais coletadas'
if any('As informações' in col for col in df.columns):
    # Encontra coluna que começa com "As informações"
    df.rename(columns={old_col: lgpd_col}, inplace=True)
```

### Caso 3: Arquivos com BOM (Byte Order Mark)

**Problema**: Excel em português adiciona `\ufeff` no início

**Solução**:
```python
pd.read_csv(file, encoding='utf-8-sig')  # Remove BOM automaticamente
```

### Caso 4: Dados Ausentes (NaN)

**Tratamento**:
- Strings vazias → Mantém como vazias
- Números ausentes → NaN (Pandas)
- Datas inválidas → NaT (Pandas)

**No Excel**:
- Células vazias permanecem vazias
- Não afeta fórmulas totalizadoras

### Caso 5: Caracteres Especiais (Acentos)

**Garantido por**:
- UTF-8 encoding em leitura
- UTF-8 encoding em escrita (openpyxl padrão)

**Caracteres suportados**:
- Acentos: á, é, í, ó, ú, ã, õ, ç
- Símbolos: ®, ©, °, §
- Emojis: ✅ ❌ 📊 (se necessário)

---

## 📝 Exemplos Completos

### Exemplo 1: CSV Mínimo Válido (Inscritos)

```csv
Nome;Login
João Silva;31987654321
Maria Santos;21912345678
```

**Resultado no Excel**: 2 linhas de dados + cabeçalho + total

### Exemplo 2: CSV Completo (Inscritos)

```csv
Nome;Login;Empresa;Cargo;Município;Comunidade;Estado;Cidade;Sou;Sobrenome;Data de Cadastro;LGPD;Comunidade.1
João Silva Santos;31987654321;Vale S.A.;Analista;Mariana;Bento Rodrigues;MG;Mariana;Morador;Santos;18/11/2025 10:30:00;sim;Centro
```

**Resultado**: Todos os campos preenchidos + "Comunidade2"

### Exemplo 3: Cálculo de Retenção

**Entrada (Cenário 1)**:
```csv
Nome;Login;Tempo
João Silva;31999999999;45
```

**Saída no Excel**:
```
Nome: João Silva
Celular: 31999999999
Retenção (hh:mm): 00:45:00
```

**Entrada (Cenário 2)**:
```csv
Nome;Login;Data Inicial;Data Final
João Silva;31999999999;18/11/2025 19:00:00;18/11/2025 19:45:00
```

**Saída no Excel**:
```
Nome: João Silva
Celular: 31999999999
Retenção (hh:mm): 00:45:00
```

---

## 📋 Sumário de Fórmulas Excel Geradas

| Localização | Fórmula | Propósito |
|-------------|---------|-----------|
| Retencao!R2 | `=inscritos[[#Totals],[Data de Cadastro]]` | Conta inscritos |
| Retencao!R3 | `=Relatório_de_acesso12[[#Totals],[Nome]]` | Conta usuários únicos |
| Retencao!R4 | `=MAX(retencao[Usuários conectados])` | Pico de audiência |
| Retencao!R5 | `=_xlfn.XLOOKUP(R4,...)` | Hora do pico |
| Retencao!R6 | `=Relatório_de_acesso12[[#Totals],[Retenção (hh:mm)]]` | Tempo médio |
| Retencao!R7 | `=mensagens[[#Totals],[Data]]` | Total de mensagens |
| Mensagens (Total) | `=SUBTOTAL(103, mensagens[Data])` | Conta mensagens |
| Acessos (Total Nome) | `=SUBTOTAL(103, Relatorio_de_acesso12[Nome])` | Conta acessos |
| Acessos (Total Retenção) | `=SUBTOTAL(101, Relatorio_de_acesso12[Retenção (hh:mm)])` | Soma tempo total |
| Inscritos (Total) | `=SUBTOTAL(103, inscritos[Data de Cadastro])` | Conta inscritos |

---

**Documento mantido por**: Equipe de Desenvolvimento PRSA
**Última atualização**: 29/01/2025
