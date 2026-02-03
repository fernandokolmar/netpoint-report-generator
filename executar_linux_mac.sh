#!/bin/bash

echo "============================================================"
echo "   Gerador de Relatório PRSA - Estatísticas"
echo "============================================================"
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python não encontrado!"
    echo "Por favor, instale Python 3.8 ou superior"
    echo "https://www.python.org/downloads/"
    exit 1
fi

echo "Verificando dependências..."
echo ""

# Instalar dependências se necessário
pip3 install -r requirements.txt

echo ""
echo "Iniciando aplicação..."
echo ""

# Executar aplicação
python3 prsa_report_generator.py

read -p "Pressione Enter para sair..."
