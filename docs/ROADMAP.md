# Roadmap - Netpoint Report Generator

## Versão Atual: v1.4.0

---

## Próximas Melhorias Planejadas

### v1.4.0 - Suporte Multi-Evento
- [ ] Aceitar múltiplos arquivos de Acessos (consolidar dados de vários eventos)
- [ ] Aceitar múltiplos arquivos Totalizado (mesclar dados minuto a minuto)
- [ ] Aceitar múltiplos arquivos de Inscritos (unificar listas)
- [ ] Aceitar múltiplos arquivos de Mensagens/Chat
- [ ] Interface para adicionar/remover arquivos dinamicamente
- [ ] Opção de gerar relatório consolidado ou separado por evento
- [ ] Identificação de evento por nome do arquivo ou coluna "Conteudo"

---

## Melhorias Futuras (Backlog)

### Interface
- [ ] Drag and drop de arquivos
- [ ] Modo escuro
- [ ] Configurações persistentes (último diretório, preferências)

### Relatório
- [ ] Exportação para PDF
- [ ] Gráficos comparativos entre eventos
- [ ] Dashboard com métricas consolidadas

### Performance
- [ ] Cache de arquivos processados
- [ ] Processamento em background para arquivos grandes

---

## Histórico de Versões

### v1.4.0 (2025-03-05)
- ✅ Suporte a múltiplas enquetes por evento
  - ✅ Botão "+ Adicionar Enquete" na interface
  - ✅ Botão "×" para remover enquetes
  - ✅ Cada enquete gera aba separada no Excel
  - ✅ Totalmente opcional (compatível com eventos sem enquete)

### v1.3.0 (2025-03-05)
- ✅ Correção crítica de crash com colunas Login + Celular simultâneas
- ✅ Coluna Login preservada como identificador de acesso (sem renomeação automática)
- ✅ Filtro de usuários de sistema (Login='visitante' removido antes do processamento)
- ✅ Robustez em colunas duplicadas (uso de iloc no _remove_empty_columns)

### v1.2.0 (2025-02-05)
- ✅ Suporte a Minnit Chat
  - ✅ Detecção automática do formato Minnit
  - ✅ Conversão de timestamp Unix para data/hora
  - ✅ Mapeamento de colunas (nickname → Nome, message → Mensagem)
  - ✅ Detecção automática de separador CSV (vírgula ou ponto-e-vírgula)
- ✅ Títulos de eixo do gráfico posicionados dentro da área de plotagem
- ✅ Melhorias na detecção de formato CSV

### v1.1.0 (2025-02-04)
- ✅ Suporte a múltiplos formatos de CSV
- ✅ Detecção automática Email/Celular
- ✅ Remoção de colunas vazias
- ✅ Chat opcional separado de Mensagens
- ✅ Marcador vermelho no pico do gráfico
- ✅ Linhas de grade verticais
- ✅ Build macOS via GitHub Actions

### v1.0.0 (2025-02-03)
- ✅ Versão inicial
- ✅ Geração de relatório Excel
- ✅ Gráfico de retenção
- ✅ Executável Windows

---

*Última atualização: 05/03/2025*
