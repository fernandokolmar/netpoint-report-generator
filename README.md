# 📊 Gerador de Relatórios - Estatísticas de Videoconferência

> Sistema de automação para geração de relatórios estatísticos de videoconferências do processo PRSA - Vale S.A.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)]()
[![Status](https://img.shields.io/badge/Status-Production-green.svg)]()

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Estrutura dos Dados](#-estrutura-dos-dados)
- [Relatório Gerado](#-relatório-gerado)
- [Arquitetura](#-arquitetura)
- [Scripts Auxiliares](#-scripts-auxiliares)
- [Solução de Problemas](#-solução-de-problemas)
- [Contribuição](#-contribuição)

---

## 🎯 Sobre o Projeto

Este sistema foi desenvolvido para **automatizar a geração de relatórios estatísticos** de videoconferências realizadas no processo de Reparação da Vale S.A. A aplicação processa dados de inscrições, mensagens, acessos e audiência minuto a minuto, gerando um arquivo Excel profissional com múltiplas planilhas, gráficos e análises automáticas.

### Contexto de Uso

O sistema é utilizado para:
- Quantificar o engajamento dos participantes em videoconferências
- Analisar a audiência e participação de comunidades afetadas
- Gerar documentação oficial de eventos de reparação
- Produzir relatórios padronizados com estatísticas detalhadas

### Principais Vantagens

- ✅ **Automação completa**: Elimina processos manuais de consolidação de dados
- ✅ **Padronização**: Relatórios consistentes e profissionais
- ✅ **Eficiência**: Gera relatórios em segundos (processamento de milhares de registros)
- ✅ **Flexibilidade**: Adapta-se a variações nas estruturas de dados de entrada
- ✅ **Interface amigável**: GUI simples e intuitiva (não requer conhecimentos técnicos)
- ✅ **Multiplataforma**: Funciona em Windows, Linux e macOS

---

## ⚡ Funcionalidades

### 📊 Análise de Dados

A aplicação processa quatro tipos de dados e calcula automaticamente:

| Métrica | Descrição |
|---------|-----------|
| **Quantidade de Inscritos** | Total de pessoas que se inscreveram no evento |
| **Usuários Distintos na Live** | Número de participantes únicos que acessaram a transmissão |
| **Pico de Audiência** | Momento de maior número de usuários simultâneos |
| **Hora do Pico** | Data/hora exata em que ocorreu o pico de audiência |
| **Tempo Médio Assistido** | Duração média de permanência dos participantes (hh:mm) |
| **Total de Mensagens** | Quantidade de mensagens enviadas durante o evento |

### 📈 Geração de Relatórios

O relatório Excel gerado contém:

- **4 Planilhas Estruturadas:**
  1. **Retenção na Live**: Gráfico de audiência ao longo do tempo + resumo estatístico
  2. **Mensagens**: Todas as mensagens enviadas durante o evento
  3. **Acessos**: Relatório detalhado de participação (com tempo de retenção)
  4. **Inscritos**: Lista completa de inscritos

- **Recursos Avançados do Excel:**
  - Tabelas nomeadas e formatadas profissionalmente
  - Gráficos de linha (LineChart) mostrando evolução da audiência
  - Fórmulas dinâmicas (SUBTOTAL, XLOOKUP, MAX)
  - Linhas totalizadoras automáticas
  - Formatação condicional e ajuste automático de colunas

### 🖥️ Interface Gráfica

- Interface limpa e intuitiva (Tkinter)
- Seleção de arquivos via diálogo de navegação
- Log em tempo real de todas as operações
- Validação de entrada com mensagens claras de erro
- Botões de ação: Processar, Limpar, Sair

---

## 🛠️ Tecnologias Utilizadas

| Componente | Tecnologia | Versão | Propósito |
|-----------|-----------|---------|-----------|
| **Linguagem** | Python | 3.8+ | Desenvolvimento principal |
| **Interface Gráfica** | Tkinter | Built-in | GUI desktop multiplataforma |
| **Processamento de Dados** | Pandas | ≥ 2.0.0 | Manipulação de dados CSV/tabular |
| **Operações Numéricas** | NumPy | ≥ 1.24.0 | Cálculos estatísticos |
| **Geração de Excel** | openpyxl | ≥ 3.1.0 | Criação de arquivos .xlsx com fórmulas e gráficos |
| **Manipulação de Datas** | datetime | Built-in | Conversão e formatação de datas |
| **Tratamento de Erros** | traceback | Built-in | Debug e logging de exceções |

### Stack Completo

```
Python 3.8+
├── tkinter (GUI)
├── pandas (Data Processing)
├── numpy (Numerical Operations)
├── openpyxl (Excel Generation)
└── datetime + traceback (Utilities)
```

---

## 📥 Instalação

### Pré-requisitos

- **Python 3.8 ou superior** instalado no sistema
- **pip** (gerenciador de pacotes Python)
- **Tkinter** (geralmente já incluído na instalação padrão do Python)

### Verificar Instalação do Python

```bash
# Windows
python --version

# Linux/Mac
python3 --version
```

### Instalação Rápida

#### 🪟 Windows

1. **Duplo clique** no arquivo `executar_windows.bat`
   - O script verificará automaticamente as dependências
   - Instalará os pacotes necessários
   - Iniciará a aplicação

#### 🐧 Linux / 🍎 macOS

1. Abra o terminal na pasta do projeto
2. Dê permissão de execução ao script:
   ```bash
   chmod +x executar_linux_mac.sh
   ```
3. Execute o script:
   ```bash
   ./executar_linux_mac.sh
   ```

### Instalação Manual

Se preferir instalar manualmente:

```bash
# 1. Clone ou baixe o repositório
cd caminho/para/App\ Estatisticas

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute a aplicação
python prsa_report_generator.py
```

### Dependências (requirements.txt)

```
pandas>=2.0.0
numpy>=1.24.0
openpyxl>=3.1.0
```

---

## 🚀 Como Usar

### Passo a Passo

#### 1. **Preparar os Arquivos CSV**

Você precisa de **4 arquivos CSV** no formato correto:

- `Inscritos.csv` - Lista de inscritos no evento
- `Mensagens.csv` - Mensagens enviadas durante a live
- `Relatório de acesso.csv` - Registros de participação
- `Totalizado.csv` - Audiência minuto a minuto

> 💡 **Importante**: Os arquivos devem estar em **UTF-8** com separador **ponto-e-vírgula (;)**

#### 2. **Iniciar a Aplicação**

Execute o script de inicialização ou rode:
```bash
python prsa_report_generator.py
```

#### 3. **Carregar os Arquivos**

Na interface gráfica:
1. Clique em **"Procurar"** ao lado de cada campo
2. Navegue até o arquivo CSV correspondente
3. Selecione o arquivo
4. Repita para os 4 arquivos obrigatórios

#### 4. **Processar e Gerar**

1. Clique no botão **"Processar e Gerar Relatório"**
2. Acompanhe o progresso na área de log
3. Aguarde a mensagem de sucesso
4. Uma janela de diálogo será aberta para salvar o arquivo Excel

#### 5. **Salvar o Relatório**

1. Escolha o local onde deseja salvar
2. O nome padrão será: `Relatorio_Videoconferencia_YYYYMMDD_HHMMSS.xlsx`
3. Clique em **"Salvar"**

#### 6. **Abrir o Relatório**

Abra o arquivo Excel gerado e explore as 4 planilhas:
- **Retencao na live**: Gráfico e resumo estatístico
- **Mensagens**: Todas as mensagens
- **Acessos**: Detalhes de participação
- **Inscritos**: Lista de inscritos

### Exemplo de Uso

```
1. Abrir aplicação
2. Carregar Inscritos.csv (1.631 registros)
3. Carregar Mensagens.csv (607 mensagens)
4. Carregar Relatório de acesso.csv (1.306 acessos)
5. Carregar Totalizado.csv (166 medições)
6. Clicar em "Processar e Gerar Relatório"
7. Salvar como "Relatorio_Evento_PRSA_20250129.xlsx"
8. ✅ Relatório gerado com sucesso!
```

---

## 📄 Estrutura dos Dados

### Formato dos Arquivos CSV

Todos os arquivos devem seguir este padrão:
- **Encoding**: UTF-8 com BOM (`utf-8-sig`)
- **Separador**: Ponto-e-vírgula (`;`)
- **Extensão**: `.csv`

### 1. Inscritos.csv

Colunas obrigatórias e opcionais:

| Coluna | Obrigatória | Descrição |
|--------|------------|-----------|
| Nome | ✅ | Nome completo do inscrito |
| Login / Celular | ✅ | Telefone de contato |
| Município | ⚠️ | Cidade do inscrito |
| Comunidade | ⚠️ | Comunidade a que pertence |
| Estado | ⚠️ | Estado (UF) |
| Data de Cadastro | ⚠️ | Data/hora da inscrição |
| LGPD | ⚠️ | Consentimento LGPD |

**Exemplo de linha:**
```csv
Nome;Login;Município;Comunidade;Data de Cadastro
João Silva;31987654321;Mariana;Centro;18/11/2025 10:30:00
```

### 2. Mensagens.csv

Colunas processadas: Nome, Município, Comunidade, Conteúdo, Remetente, Email, Mensagem, Data

**Exemplo:**
```csv
Nome;Município;Comunidade;Mensagem;Data
Maria Santos;Mariana;Bento Rodrigues;Quando teremos resposta?;18/11/2025 19:45:12
```

### 3. Relatório de acesso.csv

A aplicação suporta **dois formatos** automaticamente:

**Cenário 1**: Coluna "Tempo" em minutos
```csv
Nome;Login;Município;Comunidade;Tempo
João Silva;31987654321;Mariana;Centro;45
```

**Cenário 2**: Data Inicial + Data Final
```csv
Nome;Login;Município;Comunidade;Data Inicial;Data Final
João Silva;31987654321;Mariana;Centro;18/11/2025 19:00:00;18/11/2025 19:45:00
```

### 4. Totalizado.csv

| Coluna | Formato | Descrição |
|--------|---------|-----------|
| Data | DD/MM/YYYY HH:MM:SS | Data/hora da medição |
| Usuarios conectados | Inteiro | Número de usuários conectados |

**Exemplo:**
```csv
Data;Usuarios conectados
18/11/2025 19:00:00;150
18/11/2025 19:01:00;182
18/11/2025 19:02:00;201
```

---

## 📊 Relatório Gerado

### Estrutura do Excel

O arquivo Excel gerado contém **4 planilhas** profissionalmente formatadas:

#### 1️⃣ Retencao na live

**Conteúdo:**
- Tabela com evolução da audiência minuto a minuto
- Gráfico LineChart mostrando audiência ao longo do tempo
- Resumo com 6 métricas estatísticas principais

#### 2️⃣ Mensagens

- Tabela completa com todas as mensagens enviadas
- Inclui informações de remetente, município e comunidade
- Linha totalizadora automática

#### 3️⃣ Acessos

- Relatório detalhado de participação
- Tempo de retenção calculado automaticamente (hh:mm:ss)
- Fórmulas para somar tempo total

#### 4️⃣ Inscritos

- Lista completa de inscritos
- Todas as informações de cadastro
- Contagem total automática

### Formatação Aplicada

- **Estilo**: TableStyleMedium12 (azul claro, linhas alternadas)
- **Largura de Colunas**: Ajuste automático
- **Filtros**: Habilitados em todas as tabelas
- **Fórmulas**: SUBTOTAL para totalizadores

---

## 🏗️ Arquitetura

### Estrutura de Diretórios

```
App Estatisticas/
├── 📄 prsa_report_generator.py      # Aplicação principal
├── 📄 test_prsa.py                  # Script de teste
├── 🔧 Scripts auxiliares (análise)
├── 🚀 executar_windows.bat          # Execução Windows
├── 🚀 executar_linux_mac.sh         # Execução Linux/Mac
├── 📋 requirements.txt              # Dependências
├── 📊 Arquivos CSV de exemplo
└── 📑 Templates de referência
```

### Componentes Principais

```python
VideoConferenceReportGenerator
├── Interface Gráfica (Tkinter)
├── Carregamento de CSVs (Pandas)
├── Processamento de Dados
├── Geração de Excel (openpyxl)
└── Sistema de Log
```

---

## 🔧 Scripts Auxiliares

### test_prsa.py

Testa a aplicação sem interface gráfica e exibe estatísticas no terminal.

```bash
python test_prsa.py
```

### analyze_template.py

Analisa a estrutura do template Excel de referência.

### extract_formulas.py

Extrai todas as fórmulas do template para arquivo de texto.

---

## ❗ Solução de Problemas

### "Python não é reconhecido como comando"

**Solução Windows:**
1. Baixe Python em [python.org](https://www.python.org/downloads/)
2. Marque **"Add Python to PATH"** durante a instalação

**Solução Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt-get install python3 python3-pip

# macOS (Homebrew)
brew install python3
```

### "ModuleNotFoundError: No module named 'pandas'"

```bash
pip install -r requirements.txt
```

### "UnicodeDecodeError ao ler CSV"

Os arquivos devem estar em **UTF-8 com BOM**. Salve novamente com encoding correto.

### "Erro ao calcular tempo de retenção"

Verifique se as datas estão no formato: `DD/MM/YYYY HH:MM:SS`

### Mais problemas?

Execute via terminal para ver logs detalhados:
```bash
python prsa_report_generator.py
```

---

## 🤝 Contribuição

### Como Contribuir

1. Reporte bugs via issues
2. Sugira melhorias
3. Envie pull requests

### Diretrizes

- Seguir PEP 8
- Adicionar comentários em código complexo
- Testar com dados de exemplo

---

## 📝 Licença

Software **propriedade da Vale S.A.** para uso interno no processo de Reparação.

**Restrições:**
- ❌ Distribuição externa sem autorização
- ❌ Uso comercial
- ❌ Modificação sem aprovação

---

## 📞 Suporte

1. Consulte esta documentação
2. Verifique "Solução de Problemas"
3. Execute script de teste
4. Entre em contato com a equipe de desenvolvimento

---

## 📚 Recursos Adicionais

### Documentação do Projeto

- **[docs/README.md](docs/README.md)** - Índice completo da documentação técnica
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Arquitetura do sistema
- **[docs/GUIDELINES.md](docs/GUIDELINES.md)** - Diretrizes de desenvolvimento
- **[docs/DATA_FORMATS.md](docs/DATA_FORMATS.md)** - Especificação de formatos de dados
- **[docs/API_REFERENCE.md](docs/API_REFERENCE.md)** - Referência de API interna
- **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Solução de problemas
- **[docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)** - Como contribuir

### Guias de Instalação

- [INSTALACAO_RAPIDA.md](INSTALACAO_RAPIDA.md) - Guia simplificado

### Documentação Externa

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [openpyxl Documentation](https://openpyxl.readthedocs.io/)
- [Python Tkinter](https://docs.python.org/3/library/tkinter.html)

---

**Desenvolvido para o processo PRSA - Vale S.A.**

*Última atualização: 29/01/2025*
