# Netpoint Report Generator v1.5.0

Aplicação desenvolvida pela **Netpoint** para processar dados de videoconferência e gerar relatórios profissionais em Excel.

---

## Funcionalidades

### Processamento de Dados
- Importa arquivos CSV de videoconferência:
  - **Inscritos** - Lista de participantes inscritos
  - **Mensagens** (opcional) - Mensagens da sessão
  - **Chat** (opcional) - Chat da sessão
  - **Permanência** - Logs de permanência dos participantes
  - **Totalizado** - Dados agregados por minuto
  - **Enquetes** (opcional, múltiplas) - Resultados de enquetes do evento

### Detecção Automática de Formato
- Suporta diferentes estruturas de CSV de diferentes eventos
- Coluna `Login` preservada como identificador de acesso
- Remove colunas completamente vazias
- Adapta-se a diferentes formatos de relatório
- **Suporte a Minnit Chat**: Detecta e converte automaticamente arquivos de chat do Minnit
- **Filtro de usuários de sistema**: Remove automaticamente registros de sistema (ex: `Login='visitante'`)

### Relatório Excel Gerado
O arquivo Excel gerado contém até 5 planilhas fixas + N planilhas de enquete:

#### 1. Retenção na Live
- **Tabela de dados**: Horário, Usuários conectados, Max (pico)
- **Gráfico de linha**: Visualização da audiência ao longo do tempo
- **Tabela de resumo estatístico**:
  - Quantidade de Inscritos
  - Usuários distintos na live
  - Total de espectadores (quando aplicável — ver NumPessoas)
  - Pico de audiência
  - Hora de pico
  - Tempo médio assistido (hh:mm)
  - Total de mensagens enviadas (se houver)
  - Total de mensagens no chat (se houver)

#### 2. Mensagens (opcional)
- Tabela com todas as mensagens
- Formatação automática de colunas
- Total de mensagens

#### 3. Chat (opcional)
- Tabela com mensagens do chat
- Remove colunas desnecessárias (Cliente, Sala)
- Total de mensagens
- **Suporta formato Minnit**: Converte automaticamente timestamp Unix para data/hora legível

#### 4. Permanência
- Relatório detalhado de permanência por usuário
- Coluna `Permanencia` com total de minutos por participante
- Suporte a coluna `NumPessoas`:
  - Se todos os valores forem 0, a coluna é ocultada
  - Se houver valores, é gerada coluna `Total assistindo` (NumPessoas + 1)
- Backward compatible com formato legado (`Tempo` em minutos ou datas de acesso)

#### 5. Inscritos
- Lista completa de inscritos
- Todas as colunas com dados são mantidas, independente do formato do evento

#### 6+. Enquetes (opcional, uma aba por enquete)
- Gerada automaticamente para cada arquivo de enquete adicionado
- Colunas: Nome, Login, Pergunta, Resposta, Data
- Nomeadas sequencialmente: `Enquete 01`, `Enquete 02`, etc.
- Total de respostas calculado automaticamente

### Interface Gráfica
- Seleção de arquivos com diálogo
- Preview dos dados antes de processar
- Barra de progresso durante processamento
- Histórico de arquivos recentes (menu Arquivo > Recentes)
- Log de status em tempo real
- **Enquetes dinâmicas**: botão "+ Adicionar Enquete" para incluir múltiplos arquivos; botão "×" para remover

---

## Requisitos do Sistema

### Para o Executável
- **Windows**: Windows 10/11 (64-bit) — arquivo `.exe`
- **macOS**: macOS 12+ — arquivo `.dmg`
- **Espaço em disco**: ~60 MB
- **Memória RAM**: 4 GB (recomendado)
- **NÃO precisa de Python instalado**
- **NÃO precisa de dependências adicionais**

### Para Desenvolvimento (código fonte)
- Python 3.8+
- Dependências: pandas, openpyxl, Pillow

---

## Instalação e Uso

### Opção 1: Executável (Recomendado)

1. Baixe o arquivo do seu sistema (`.exe` para Windows, `.dmg` para macOS)
2. Execute o arquivo
3. Não precisa de instalação adicional

### Opção 2: Código Fonte (Para Desenvolvimento)

```bash
# Instalar dependências
pip install pandas openpyxl Pillow

# Executar
python netpoint_report_generator.py
```

---

## Como Usar

1. **Abra o aplicativo**
2. **Carregue os arquivos CSV** usando os botões "Procurar"
3. **Opcional**: Use "Preview" para verificar os dados
4. **Clique em "Processar e Gerar Relatório"**
5. **Escolha onde salvar** o arquivo Excel
6. **Pronto!** O relatório será gerado

---

## Estrutura do Projeto

```
App Estatisticas/
├── netpoint_report_generator.py  # Aplicação principal
├── config/
│   ├── settings.py               # Configurações (nome, versão, constantes)
│   └── column_mappings.py        # Mapeamento de colunas
├── core/
│   ├── controller.py             # Controlador principal
│   ├── data_loader.py            # Carregamento de CSVs
│   ├── data_processor.py         # Processamento de dados
│   ├── excel_generator.py        # Geração do Excel
│   └── exceptions.py             # Exceções customizadas
├── ui/
│   ├── preview_window.py         # Janela de preview
│   └── stats_window.py           # Janela de estatísticas
├── utils/
│   └── file_history.py           # Histórico de arquivos
├── assets/
│   ├── icon.ico                  # Ícone Windows
│   └── icon.png                  # Ícone PNG
└── dist/
    └── Netpoint Report Generator.exe  # Executável Windows
```

---

## Changelog

### v1.5.0 (2026-03-27)
- **Planilha "Permanência"**: Substitui a aba "Acessos" com dados mais completos
  - Usa coluna `Permanencia` (minutos diretos, sem conversão)
  - Backward compatible com formato legado (`Tempo` ou datas de acesso)
- **Suporte a NumPessoas**: Quando participantes assistem em grupo
  - Se todos os valores forem 0, coluna é ocultada automaticamente
  - Se houver valores, gera coluna `Total assistindo` (NumPessoas + 1)
  - Linha "Total de espectadores" no resumo quando aplicável
- **Inscritos completos**: Todas as colunas com dados são mantidas, independente do formato do evento

### v1.4.0 (2025-03-05)
- **Suporte a Enquetes**: Importação de múltiplos arquivos de enquete (opcional)
  - Botão "+ Adicionar Enquete" na interface
  - Cada enquete gera uma aba separada no Excel

### v1.3.0 (2025-03-05)
- **Correção crítica de crash**: Arquivos com colunas `Login` e `Celular` simultâneas causavam `AttributeError`
- **Coluna `Login` preservada**: Não é mais renomeada automaticamente
- **Filtro de usuários de sistema**: Registros com `Login='visitante'` removidos automaticamente
- **Robustez em colunas duplicadas**: `_remove_empty_columns` usa índice posicional

### v1.2.0 (2025-02-05)
- **Suporte a Minnit Chat**: Detecta e processa automaticamente arquivos de chat do Minnit
- Gráfico de retenção melhorado

### v1.1.0 (2025-02-04)
- Suporte a múltiplos formatos de CSV
- Detecção automática de Email vs Celular na coluna Login
- Remoção automática de colunas vazias
- Build automático para macOS via GitHub Actions

### v1.0.0 (2025-02-03)
- Lançamento inicial — Netpoint Report Generator
- Ícone personalizado, gráfico de retenção, executável standalone

---

## Plataformas Suportadas

| Plataforma | Formato | Disponível |
|------------|---------|------------|
| Windows    | .exe    | ✅ |
| macOS      | .dmg    | ✅ (via GitHub Actions) |

---

## Suporte

Para problemas ou sugestões, entre em contato com a equipe Netpoint.

---

**Desenvolvido por**: Netpoint
**Versão**: 1.5.0
**Última atualização**: 27/03/2026
