# Netpoint Report Generator v1.4.0

Aplicação para processar dados de videoconferência e gerar relatórios profissionais em Excel.

---

## Funcionalidades

### Processamento de Dados
- Importa arquivos CSV de videoconferência:
  - **Inscritos** - Lista de participantes inscritos
  - **Mensagens** (opcional) - Mensagens da sessão
  - **Chat** (opcional) - Chat da sessão
  - **Relatório de Acesso** - Logs de entrada/saída
  - **Totalizado** - Dados agregados por minuto
  - **Enquetes** (opcional, múltiplas) - Resultados de enquetes do evento

### Detecção Automática de Formato
- Suporta diferentes estruturas de CSV de diferentes eventos
- Coluna `Login` preservada como identificador de acesso (independente de Email, Celular ou CPF)
- Remove colunas completamente vazias
- Adapta-se a diferentes formatos de relatório
- **Suporte a Minnit Chat**: Detecta e converte automaticamente arquivos de chat do Minnit
- **Filtro de usuários de sistema**: Remove automaticamente registros de sistema (ex: `Login='visitante'`)

### Relatório Excel Gerado
O arquivo Excel gerado contém até 5 planilhas fixas + N planilhas de enquete:

#### 1. Retenção na Live
- **Tabela de dados**: Horário, Usuários conectados, Max (pico)
- **Gráfico de linha**: Visualização da audiência ao longo do tempo
  - Linha azul sólida (#4472C4)
  - Eixo X: Horários (HH:MM) espaçados a cada 10 minutos
  - Eixo Y: Quantidade de usuários
  - Linhas de grade verticais em cinza claro
  - Marcador vermelho no ponto de pico máximo
  - Rótulo mostrando horário e valor do pico
  - Sem legenda lateral
- **Tabela de resumo estatístico**:
  - Quantidade de Inscritos
  - Usuários distintos na live
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

#### 4. Acessos
- Relatório detalhado de acesso por usuário
- Nome, horários de entrada/saída, tempo de permanência
- Tempo total e médio calculados

#### 5. Inscritos
- Lista completa de inscritos

#### 6+. Enquetes (opcional, uma aba por enquete)
- Gerada automaticamente para cada arquivo de enquete adicionado
- Colunas: Nome, Login, Pergunta, Resposta, Data
- Nomeadas sequencialmente: `Enquete 01`, `Enquete 02`, etc.
- Total de respostas calculado automaticamente
- Data de cadastro, informações de contato
- Contagem total
- Remove colunas irrelevantes (MeuId, UTM, Grupo)

### Interface Gráfica
- Seleção de arquivos com diálogo
- Preview dos dados antes de processar
- Barra de progresso durante processamento
- Histórico de arquivos recentes (menu Arquivo > Recentes)
- Log de status em tempo real
- **Enquetes dinâmicas**: botão "+ Adicionar Enquete" para incluir múltiplos arquivos; botão "×" para remover

---

## Requisitos do Sistema

### Para o Executável (.exe)
- **Sistema Operacional**: Windows 10/11 (64-bit)
- **Espaço em disco**: ~60 MB
- **Memória RAM**: 4 GB (recomendado)
- **NÃO precisa de Python instalado**
- **NÃO precisa de dependências adicionais**

### Para Desenvolvimento (código fonte)
- Python 3.8+
- Dependências: pandas, openpyxl, Pillow

---

## Instalação e Uso

### Opção 1: Executável (Recomendado para Produção)

1. Copie o arquivo `Netpoint Report Generator.exe` para o computador
2. Dê duplo clique para executar
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

1. **Abra o aplicativo** (duplo clique no .exe)
2. **Carregue os 4 arquivos CSV** usando os botões "Procurar"
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
│   └── settings.py               # Configurações (nome, versão, colunas)
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
├── dist/
│   └── Netpoint Report Generator.exe  # Executável
└── docs/
    └── README.md                 # Esta documentação
```

---

## Changelog

### v1.4.0 (2025-03-05)
- **Suporte a Enquetes**: Importação de múltiplos arquivos de enquete (opcional)
  - Botão "+ Adicionar Enquete" na interface — adicione quantas precisar
  - Botão "×" para remover enquetes adicionadas por engano
  - Cada enquete gera uma aba separada no Excel (`Enquete 01`, `Enquete 02`, etc.)
  - Colunas: Nome, Login, Pergunta, Resposta, Data
  - Totalmente opcional — eventos sem enquete funcionam normalmente

### v1.3.0 (2025-03-05)
- **Correção crítica de crash**: Arquivos com colunas `Login` e `Celular` simultâneas causavam `AttributeError` — corrigido
- **Coluna `Login` preservada**: Não é mais renomeada automaticamente; `Login` é o identificador de acesso do usuário, independente do conteúdo
- **Filtro de usuários de sistema**: Registros com `Login='visitante'` (ou variações) são removidos automaticamente antes do processamento
- **Robustez em colunas duplicadas**: `_remove_empty_columns` usa índice posicional (`iloc`) para evitar ambiguidades com nomes de coluna duplicados

### v1.2.0 (2025-02-05)
- **Suporte a Minnit Chat**: Detecta e processa automaticamente arquivos de chat do Minnit
  - Converte timestamp Unix para formato DD/MM/YYYY HH:MM:SS
  - Extrai Nome (nickname) e Mensagem (message)
  - Detecção automática de separador (vírgula ou ponto-e-vírgula)
- Gráfico de retenção com títulos de eixo posicionados dentro da área de plotagem
- Melhorias na detecção automática de formato CSV

### v1.1.0 (2025-02-04)
- Suporte a múltiplos formatos de CSV (diferentes eventos)
- Detecção automática de Email vs Celular na coluna Login
- Remoção automática de colunas vazias
- Arquivo Chat agora é opcional (separado de Mensagens)
- Gráfico de retenção melhorado:
  - Marcador vermelho no ponto de pico máximo
  - Rótulo com horário e valor do pico
  - Linhas de grade verticais em cinza claro
- Campos limpos automaticamente após gerar relatório
- Removidas colunas irrelevantes (MeuId, UTM, Grupo)
- Build automático para macOS via GitHub Actions

### v1.0.0 (2025-02-03)
- Renomeado para "Netpoint Report Generator"
- Adicionado ícone personalizado da Netpoint
- Gráfico de retenção com:
  - Linha azul sólida
  - Horários no eixo horizontal (espaçados a cada 10 min)
  - Sem legenda lateral
  - Tamanho grande (20cm x 10cm)
- Geração de executável standalone (.exe)
- Correção de erros de corrupção do Excel
- Tabelas Excel sem totalsRowShown (evita corrupção)
- Coluna "Horário" formatada como texto HH:MM

---

## Plataformas Suportadas

| Plataforma | Formato | Disponível |
|------------|---------|------------|
| Windows    | .exe    | ✅ |
| macOS      | .dmg    | ✅ (via GitHub Actions) |

---

## Suporte

Para problemas ou sugestões, entre em contato com a equipe de desenvolvimento.

---

**Desenvolvido por**: Netpoint
**Versão**: 1.4.0
**Última atualização**: 05/03/2025
