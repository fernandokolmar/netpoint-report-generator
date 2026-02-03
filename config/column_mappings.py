"""
Mapeamentos de colunas para normalização de DataFrames.
"""

# Mapa de renomeação de colunas
COLUMN_RENAMES = {
    'Login': 'Celular',
    'Comunidade.1': 'Comunidade2',
    # Coluna LGPD gigante
    'As informações pessoais coletadas serão utilizadas exclusivamente para fins de interação  por meio de perguntas e respostas  durante a transmissão e  caso necessário  para tratativas futuras quando não houver tempo hábil para responder durante o evento. Em conformidade com a Lei Geral de Proteção de Dados  Lei nº 13.709/2018   a Vale assegura que os dados permanecerão protegidos e não serão utilizados para finalidades distintas da videoconferência  sendo mantidos apenas pelo tempo necessário ao processo de Reparação.': 'As informações pessoais coletadas'
}

# Colunas obrigatórias por tipo de DataFrame
REQUIRED_COLUMNS = {
    'inscritos': ['Nome'],
    'mensagens': ['Nome'],
    'relatorio_acesso': ['Nome'],
    'totalizado': ['Data', 'Usuarios conectados']
}

# Colunas opcionais por tipo de DataFrame
OPTIONAL_COLUMNS = {
    'inscritos': [
        'Celular', 'Município', 'Comunidade', 'Estado', 'Cidade',
        'Sou', 'Sobrenome', 'Comunidade2',
        'As informações pessoais coletadas', 'Data de Cadastro'
    ],
    'mensagens': [
        'Município', 'Comunidade', 'Estado', 'Cidade', 'Sou', 'Sobrenome',
        'Comunidade2', 'Conteudo', 'As informações pessoais coletadas',
        'Remetente', 'Email', 'Mensagem', 'Data'
    ],
    'relatorio_acesso': [
        'Celular', 'Município', 'Comunidade', 'Estado', 'Cidade',
        'Comunidade_1', 'As informações pessoais coletadas',
        'Conteudo', 'Retenção (hh:mm)', 'Tempo_Minutos'
    ],
    'totalizado': []
}
