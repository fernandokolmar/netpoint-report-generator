# Netpoint Report Generator v1.7.0

Aplicação desenvolvida pela **Netpoint** para processar dados de videoconferência e gerar relatórios profissionais em Excel.

---

## Funcionalidades

### Relatório Evento (Aba 1)

Importa arquivos CSV do evento e gera um relatório Excel completo:

| Arquivo | Obrigatório | Descrição |
|---|---|---|
| Inscritos | Opcional | Lista de participantes inscritos |
| Mensagens | Opcional | Mensagens da sessão |
| Chat | Opcional | Chat da sessão |
| Relatório de Acesso | Sim | Logs de acesso/permanência |
| Totalizado | Sim | Dados agregados por minuto |
| Participantes Zoom | Opcional | CSV exportado pelo Zoom Webinar |
| Inscrições Zoom | Opcional | Lista de inscritos exportada pelo Zoom |
| Enquetes | Opcional (múltiplas) | Resultados de enquetes do evento |

### Relatório Zoom (Aba 2)

Gera um relatório Excel exclusivo de dados Zoom, sem precisar dos arquivos do evento:

- Adicione um ou mais arquivos **Participantes Zoom** (CSV exportado pelo Zoom)
- Opcionalmente carregue o arquivo **Inscrições Zoom** para enriquecer o consolidado
- Cada arquivo Zoom gera três abas no Excel:
  - **Consolidado**: resumo da reunião + tabela de participantes enriquecida
  - **Presença Zoom**: detalhe completo linha a linha
  - **Inscrições Zoom**: lista completa de inscritos (quando disponível)

---

## Relatório Excel Gerado

### Abas do Relatório Evento

#### 1. Retenção na Live
- Tabela: Horário, Usuários conectados, Max (pico)
- Gráfico de linha: audiência ao longo do tempo
- Resumo estatístico: Inscritos, usuários distintos, pico, hora de pico, tempo médio, total de mensagens

#### 2. Mensagens (opcional)
- Tabela com todas as mensagens, total calculado automaticamente

#### 3. Chat (opcional)
- Tabela com mensagens do chat
- Suporte a **formato Minnit**: timestamp Unix convertido automaticamente para data/hora legível

#### 4. Permanência
- Permanência total por participante (em minutos)
- Suporte a `NumPessoas`: gera coluna `Total assistindo` quando há valores

#### 5. Inscritos (opcional)
- Lista completa com todas as colunas disponíveis

#### 6. Consolidado (opcional — quando há Participantes Zoom)
- Resumo da reunião Zoom (Tópico, ID, Anfitrião, Duração, Horário)
- Tabela de participantes: Nome, E-mail, Especialidade/Clínica (quando disponível), Permanência (minutos)
- Match inteligente com inscrições: e-mail exato > nome completo > primeiro nome único com validação cruzada

#### 7. Presença Zoom (opcional)
- Detalhe completo de todas as sessões registradas pelo Zoom

#### 8. Inscrições Zoom (opcional)
- Lista completa de inscritos exportada pelo Zoom

#### 9+. Enquetes (opcional, uma aba por enquete)
- Nomeadas: `Enquete 01`, `Enquete 02`, etc.
- Colunas: Nome, Login, Pergunta, Resposta, Data

### Abas do Relatório Zoom (por arquivo)

Quando múltiplos arquivos Zoom são carregados, o sufixo numérico distingue as abas:
`Consolidado 1`, `Presença Zoom 1`, `Inscrições Zoom 1`, `Consolidado 2`, ...

---

## Detecção Automática de Formato

- Detecta separador CSV (`;` padrão ou `,` para Minnit)
- Detecta formato especial de duplo cabeçalho do Zoom (Participantes e Inscrições)
- Remove colunas e linhas completamente vazias
- Filtra usuários de sistema (`Login='visitante'`)
- Colunas de enriquecimento (Telefone, Especialidade) omitidas automaticamente quando não há dados

---

## Requisitos do Sistema

### Para o Executável
- **Windows**: Windows 10/11 (64-bit) — arquivo `.exe`
- **macOS**: macOS 12+ — arquivo `.dmg`
- Espaço em disco: ~60 MB
- Memória RAM: 4 GB (recomendado)
- **Não requer Python ou dependências adicionais**

### Para Desenvolvimento
- Python 3.8+
- Dependências: `pandas`, `openpyxl`, `Pillow`

---

## Instalação e Uso

### Opção 1: Executável (Recomendado)

1. Baixe o arquivo do seu sistema (`.exe` para Windows, `.dmg` para macOS)
2. Execute o arquivo — nenhuma instalação necessária

### Opção 2: Código Fonte

```bash
pip install pandas openpyxl Pillow
python netpoint_report_generator.py
```

---

## Como Usar

### Relatório Evento
1. Abra o aplicativo na aba **Relatório Evento**
2. Carregue os arquivos CSV obrigatórios (Relatório de Acesso, Totalizado)
3. Adicione os opcionais desejados (Inscritos, Mensagens, Chat, Participantes Zoom, Inscrições Zoom, Enquetes)
4. Clique em **"Processar e Gerar Relatório"**
5. Escolha onde salvar o arquivo Excel

### Relatório Zoom
1. Abra o aplicativo na aba **Relatório Zoom**
2. Clique em **"+ Adicionar Participantes Zoom"** para cada arquivo CSV do Zoom
3. Opcionalmente carregue o arquivo **Inscrições Zoom**
4. Clique em **"Gerar Relatório Zoom"**
5. Escolha onde salvar o arquivo Excel

---

## Estrutura do Projeto

```
App Estatisticas/
├── netpoint_report_generator.py  # Aplicação principal (UI)
├── config/
│   ├── settings.py               # Configurações (versão, constantes)
│   └── column_mappings.py        # Mapeamento de colunas
├── core/
│   ├── controller.py             # Orquestração do fluxo
│   ├── data_loader.py            # Carregamento de CSVs
│   ├── data_processor.py         # Processamento de dados
│   ├── excel_generator.py        # Geração do Excel
│   └── exceptions.py             # Exceções customizadas
├── ui/
│   ├── preview_window.py         # Janela de preview
│   └── stats_window.py           # Janela de estatísticas
├── utils/
│   └── file_history.py           # Histórico de arquivos recentes
├── assets/
│   ├── icon.ico                  # Ícone Windows
│   └── icon.png                  # Ícone PNG
├── netpoint.spec                 # Build Windows (PyInstaller)
└── netpoint_macos.spec           # Build macOS (PyInstaller)
```

---

## Changelog

### v1.7.0 (2026-04-24)
- **Relatório Zoom exclusivo** (Aba 2): gera Excel com dados Zoom sem precisar dos arquivos do evento
  - Suporte a múltiplos arquivos Zoom em paralelo
  - **Inscrições Zoom**: carregamento opcional do CSV de inscritos exportado pelo Zoom
  - **Consolidado**: resumo da reunião + tabela de participantes enriquecida com dados das inscrições
  - **Match inteligente**: e-mail exato > nome completo > primeiro nome único (com validação cruzada de nomes e e-mails para evitar matches incorretos)
  - Colunas de enriquecimento (Especialidade, Clínica) exibidas apenas quando há dados
  - Três abas por arquivo Zoom: Consolidado, Presença Zoom, Inscrições Zoom
- **Labels atualizados**: "Participantes Zoom" e "Inscrições Zoom" refletem os nomes reais dos arquivos exportados pelo Zoom

### v1.6.0 (2026-04-10)
- **Inscritos agora opcional**: eventos sem lista de inscritos funcionam normalmente
- **Presença no Zoom**: campo opcional para importar CSV exportado pelo Zoom
  - Detecta automaticamente formato de duplo cabeçalho do Zoom
  - Zoom Consolidado e Presença no Zoom gerados como abas separadas

### v1.5.0 (2026-03-27)
- **Planilha "Permanência"**: substitui a aba "Acessos" com dados mais completos
- **Suporte a NumPessoas**: coluna `Total assistindo` gerada automaticamente quando aplicável
- **Inscritos completos**: todas as colunas com dados são mantidas

### v1.4.0 (2025-03-05)
- **Enquetes**: suporte a múltiplos arquivos de enquete; cada um gera uma aba separada

### v1.3.0 (2025-03-05)
- Correção crítica de crash com colunas `Login` e `Celular` simultâneas
- Coluna `Login` preservada sem renomeação automática
- Filtro de usuários de sistema (`Login='visitante'`)

### v1.2.0 (2025-02-05)
- Suporte a formato Minnit Chat (timestamp Unix → data/hora legível)

### v1.1.0 (2025-02-04)
- Suporte a múltiplos formatos de CSV
- Detecção automática de separador e encoding

### v1.0.0 (2025-02-03)
- Lançamento inicial

---

## Plataformas Suportadas

| Plataforma | Formato | Status |
|------------|---------|--------|
| Windows    | .exe    | ✅ |
| macOS      | .dmg    | ✅ (via GitHub Actions) |

---

**Desenvolvido por**: Netpoint  
**Versão**: 1.7.0  
**Última atualização**: 24/04/2026
