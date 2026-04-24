"""
Configurações gerais do Netpoint Report Generator.
"""

# Informações da aplicação
APP_NAME = "Netpoint Reports"
APP_VERSION = "1.9.7"
APP_AUTHOR = "Netpoint"

# Configurações CSV
CSV_ENCODING = 'utf-8-sig'
CSV_SEPARATOR = ';'
DATE_FORMAT = '%d/%m/%Y %H:%M:%S'

# Validação de arquivos
MAX_FILE_SIZE_MB = 100
MIN_ROWS = 1

# Configurações Excel
EXCEL_TABLE_STYLE = "TableStyleMedium12"
EXCEL_SHOW_TOTALS = True

# Nomes de colunas padrão
COL_NOME = 'Nome'
COL_CELULAR = 'Celular'
COL_LOGIN = 'Login'
COL_MUNICIPIO = 'Município'
COL_COMUNIDADE = 'Comunidade'
COL_ESTADO = 'Estado'
COL_CIDADE = 'Cidade'
COL_DATA_CADASTRO = 'Data de Cadastro'
COL_RETENCAO = 'Retenção (hh:mm)'
COL_TEMPO = 'Tempo'
COL_DATA_INICIAL = 'Data Acesso Inicial'
COL_DATA_FINAL = 'Data Acesso Final'
COL_USUARIOS_CONECTADOS = 'Usuarios conectados'
COL_DATA = 'Data'
COL_MENSAGEM = 'Mensagem'
COL_CONTEUDO = 'Conteudo'
COL_EMAIL = 'Email'
COL_REMETENTE = 'Remetente'
COL_SOU = 'Sou'
COL_SOBRENOME = 'Sobrenome'
COL_PERMANENCIA = 'Permanencia'
COL_NUM_PESSOAS = 'NumPessoas'
COL_TOTAL_ASSISTINDO = 'Total assistindo'

# Nomes de tabelas Excel
# IMPORTANTE: Nomes devem ser simples, sem números no início, sem caracteres especiais
TABLE_RETENCAO = 'tblRetencao'
TABLE_MENSAGENS = 'tblMensagens'
TABLE_CHAT = 'tblChat'
TABLE_ACESSOS = 'tblAcessos'
TABLE_PERMANENCIA = 'tblPermanencia'
TABLE_INSCRITOS = 'tblInscritos'
TABLE_RESUMO = 'tblResumo'

# Colunas a remover do Chat (não são relevantes para o relatório)
CHAT_COLUMNS_TO_REMOVE = ['Cliente', 'Sala']
