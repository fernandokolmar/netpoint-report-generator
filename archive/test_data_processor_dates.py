"""
Script de teste para ReportDataProcessor - Modo de calculo com datas.

Testa o processamento quando o relatorio usa colunas de data inicial e final.
"""

import pandas as pd
from core.data_processor import ReportDataProcessor


def create_sample_data_with_dates():
    """Cria dados de exemplo com colunas de datas."""

    # DataFrame de inscritos
    inscritos = pd.DataFrame({
        'Nome': ['Pedro Souza'],
        'Login': ['31977665544']
    })

    # DataFrame de relatório de acesso (modo 2: com Data Inicial e Final)
    relatorio_acesso = pd.DataFrame({
        'Nome': ['Pedro Souza'],
        'Login': ['31977665544'],
        'Data Acesso Inicial': ['29/01/2025 14:00:00'],
        'Data Acesso Final': ['29/01/2025 15:35:45']
    })

    # DataFrame de mensagens
    mensagens = pd.DataFrame({
        'Nome': ['Pedro Souza'],
        'Mensagem': ['Excelente!']
    })

    # DataFrame totalizado
    totalizado = pd.DataFrame({
        'Data': ['29/01/2025 14:00:00'],
        'Usuarios conectados': [50]
    })

    return {
        'inscritos': inscritos,
        'relatorio_acesso': relatorio_acesso,
        'mensagens': mensagens,
        'totalizado': totalizado
    }


def test_processor_with_dates():
    """Testa o processador com modo de datas."""

    print("=" * 60)
    print("TESTE: ReportDataProcessor - Modo com Datas")
    print("=" * 60)

    # Criar dados de exemplo
    raw_data = create_sample_data_with_dates()

    print("\n1. Dados brutos criados:")
    print("   Relatorio de acesso com colunas:")
    print(f"      - Data Acesso Inicial: {raw_data['relatorio_acesso']['Data Acesso Inicial'].iloc[0]}")
    print(f"      - Data Acesso Final: {raw_data['relatorio_acesso']['Data Acesso Final'].iloc[0]}")

    # Criar processador
    processor = ReportDataProcessor()

    # Processar dados
    print("\n2. Processando dados...")
    processed_data = processor.process_all(raw_data)

    # Verificar resultado
    print("\n3. Resultado do processamento:")
    relatorio = processed_data['relatorio_processed']

    if 'Retenção (hh:mm)' in relatorio.columns:
        retencao = relatorio['Retenção (hh:mm)'].iloc[0]
        print(f"   [OK] Retencao calculada: {retencao}")
        print(f"   Diferenca esperada: 1:35:45")

        # Verificar se a diferença está correta
        if retencao == "1:35:45":
            print("   [OK] Calculo de tempo correto!")
        else:
            print(f"   [AVISO] Valor esperado: 1:35:45, obtido: {retencao}")
    else:
        print("   [ERRO] Coluna Retencao nao foi criada")

    print("\n" + "=" * 60)
    print("TESTE CONCLUIDO!")
    print("=" * 60)


if __name__ == "__main__":
    test_processor_with_dates()
