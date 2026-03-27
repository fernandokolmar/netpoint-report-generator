"""
Mapeamentos de colunas para normalização de DataFrames.

Este módulo suporta diferentes estruturas de CSV de diferentes eventos.
A detecção é automática baseada nas colunas presentes no arquivo.
"""

# Mapa de renomeação de colunas (nomes longos -> curtos)
COLUMN_RENAMES = {
    'Comunidade.1': 'Comunidade2',
    # Coluna LGPD gigante
    'As informações pessoais coletadas serão utilizadas exclusivamente para fins de interação  por meio de perguntas e respostas  durante a transmissão e  caso necessário  para tratativas futuras quando não houver tempo hábil para responder durante o evento. Em conformidade com a Lei Geral de Proteção de Dados  Lei nº 13.709/2018   a Vale assegura que os dados permanecerão protegidos e não serão utilizados para finalidades distintas da videoconferência  sendo mantidos apenas pelo tempo necessário ao processo de Reparação.': 'LGPD'
}

# Mapeamento inteligente de Login -> tipo correto
# Se Login contém @ é Email, senão é Celular
# Isso é detectado dinamicamente no data_processor

# Colunas obrigatórias por tipo de DataFrame (mínimo necessário)
REQUIRED_COLUMNS = {
    'inscritos': ['Nome'],
    'mensagens': ['Nome'],
    'relatorio_acesso': ['Nome'],
    'totalizado': ['Data', 'Usuarios conectados']
}

# Colunas opcionais conhecidas por tipo de DataFrame
# Todas as colunas que podem aparecer em diferentes variantes de CSV
OPTIONAL_COLUMNS = {
    'inscritos': [
        # Identificação
        'Email', 'Celular', 'Login',
        # Localização
        'Município', 'Comunidade', 'Estado', 'Cidade',
        # Dados pessoais
        'Sou', 'Sobrenome', 'CPF', 'Empresa', 'Cargo',
        # Dados profissionais
        'Categoria do Conselho', 'UF do Conselho', 'Número Registro Profissional',
        # Outros
        'Comunidade2', 'LGPD', 'Data de Cadastro',
        # Nota: 'UTM', 'Grupo', 'MeuId' removidos intencionalmente (não relevantes)
        # Redes sociais
        'LinkedIn', 'Site', 'WhatsApp', 'Instagram', 'Facebook'
    ],
    'mensagens': [
        'Email', 'Celular', 'Login',
        'Município', 'Comunidade', 'Estado', 'Cidade',
        'Sou', 'Sobrenome',
        'Comunidade2', 'Conteudo', 'LGPD',
        'Remetente', 'Mensagem', 'Data'
    ],
    'relatorio_acesso': [
        # Identificação
        'Email', 'Celular', 'Login',
        # Localização
        'Município', 'Comunidade', 'Estado', 'Cidade', 'Comunidade_1',
        # Dados pessoais
        'Sou', 'Sobrenome', 'CPF', 'Empresa', 'Cargo',
        # Dados profissionais
        'Categoria do Conselho', 'UF do Conselho', 'Número Registro Profissional',
        # Tempo (calculados)
        'Conteudo', 'Retenção (hh:mm)', 'Tempo_Minutos',
        # Permanência (novo formato)
        'Permanencia', 'NumPessoas', 'Total assistindo',
        # Dados de acesso
        'Data Acesso Inicial', 'Data Acesso Final', 'HostAddress', 'Numero de Pessoas',
        # Outros
        'LGPD', 'UTM',
        'Você faz parte de alguma rede franqueada?',
        # Redes sociais
        'LinkedIn', 'Site', 'WhatsApp', 'Instagram', 'Facebook'
    ],
    'totalizado': []
}

# Colunas que devem ser removidas se estiverem completamente vazias
REMOVE_IF_EMPTY = [
    'Empresa', 'Cargo', 'LinkedIn', 'Site', 'WhatsApp', 'Instagram', 'Facebook',
    'UTM', 'HostAddress', 'Numero de Pessoas', 'MeuId', 'Grupo',
    'Você faz parte de alguma rede franqueada?'
]

# Colunas prioritárias para exibição (ordem de importância)
PRIORITY_COLUMNS = {
    'inscritos': ['Nome', 'Email', 'Celular', 'Estado', 'Cidade', 'Data de Cadastro'],
    'relatorio_acesso': ['Nome', 'Email', 'Celular', 'Estado', 'Cidade', 'Retenção (hh:mm)', 'Tempo_Minutos']
}
