# Netpoint Report Generator v1.0.0

Aplicação para processar dados de videoconferência e gerar relatórios profissionais em Excel.

---

## Funcionalidades

### Processamento de Dados
- Importa 4 arquivos CSV de videoconferência:
  - **Inscritos** - Lista de participantes inscritos
  - **Mensagens** - Chat/mensagens da sessão
  - **Relatório de Acesso** - Logs de entrada/saída
  - **Totalizado** - Dados agregados por minuto

### Relatório Excel Gerado
O arquivo Excel gerado contém 4 planilhas:

#### 1. Retenção na Live
- **Tabela de dados**: Horário, Usuários conectados, Max (pico)
- **Gráfico de linha**: Visualização da audiência ao longo do tempo
  - Linha azul sólida (#4472C4)
  - Eixo X: Horários (HH:MM) espaçados a cada 10 minutos
  - Eixo Y: Quantidade de usuários
  - Sem legenda lateral
- **Tabela de resumo estatístico**:
  - Quantidade de Inscritos
  - Usuários distintos na live
  - Pico de audiência
  - Hora de pico
  - Tempo médio assistido (hh:mm)
  - Total de mensagens enviadas

#### 2. Mensagens
- Tabela com todas as mensagens do chat
- Formatação automática de colunas
- Total de mensagens

#### 3. Acessos
- Relatório detalhado de acesso por usuário
- Nome, horários de entrada/saída, tempo de permanência
- Tempo total e médio calculados

#### 4. Inscritos
- Lista completa de inscritos
- Data de cadastro, informações de contato
- Contagem total

### Interface Gráfica
- Seleção de arquivos com diálogo
- Preview dos dados antes de processar
- Barra de progresso durante processamento
- Histórico de arquivos recentes (menu Arquivo > Recentes)
- Log de status em tempo real

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

## Suporte

Para problemas ou sugestões, entre em contato com a equipe de desenvolvimento.

---

**Desenvolvido por**: Netpoint
**Versão**: 1.0.0
**Última atualização**: 03/02/2025
