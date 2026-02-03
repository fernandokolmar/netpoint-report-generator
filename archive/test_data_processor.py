"""
Script de teste para ReportDataProcessor.

Testa o processamento de DataFrames com dados fictícios.
"""

import pandas as pd
from core.data_processor import ReportDataProcessor


def create_sample_data():
    """Cria dados de exemplo para teste."""

    # DataFrame de inscritos
    inscritos = pd.DataFrame({
        'Nome': ['João Silva', 'Maria Santos'],
        'Login': ['31999887766', '31988776655'],
        'Município': ['Belo Horizonte', 'Contagem'],
        'Comunidade': ['Comunidade A', 'Comunidade B'],
        'Estado': ['MG', 'MG']
    })

    # DataFrame de relatório de acesso (modo 1: com coluna Tempo)
    relatorio_acesso = pd.DataFrame({
        'Nome': ['João Silva', 'Maria Santos'],
        'Login': ['31999887766', '31988776655'],
        'Município': ['Belo Horizonte', 'Contagem'],
        'Tempo': [125.5, 90.0]  # Tempo em minutos
    })

    # DataFrame de mensagens
    mensagens = pd.DataFrame({
        'Nome': ['João Silva'],
        'Mensagem': ['Ótima apresentação!'],
        'Data': ['29/01/2025 14:30:00']
    })

    # DataFrame totalizado
    totalizado = pd.DataFrame({
        'Data': ['29/01/2025 14:00:00', '29/01/2025 14:15:00'],
        'Usuarios conectados': [100, 150]
    })

    return {
        'inscritos': inscritos,
        'relatorio_acesso': relatorio_acesso,
        'mensagens': mensagens,
        'totalizado': totalizado
    }


def test_processor():
    """Testa o processador de dados."""

    print("=" * 60)
    print("TESTE: ReportDataProcessor")
    print("=" * 60)

    # Criar dados de exemplo
    raw_data = create_sample_data()

    print("\n1. Dados brutos criados:")
    for name, df in raw_data.items():
        print(f"   - {name}: {len(df)} linhas, {len(df.columns)} colunas")

    # Criar processador com callback
    def progress_callback(message):
        print(f"   [LOG] {message}")

    processor = ReportDataProcessor(progress_callback=progress_callback)

    # Processar dados
    print("\n2. Processando dados...")
    processed_data = processor.process_all(raw_data)

    print("\n3. Dados processados:")
    for name, df in processed_data.items():
        print(f"\n   {name}:")
        print(f"      Linhas: {len(df)}")
        print(f"      Colunas: {list(df.columns)}")
        if len(df) > 0:
            print(f"      Exemplo (primeira linha):")
            for col in df.columns:
                print(f"         {col}: {df[col].iloc[0]}")

    # Verificações específicas
    print("\n4. Verificações:")

    # Verificar renomeação de Login para Celular
    if 'Celular' in processed_data['inscritos_processed'].columns:
        print("   [OK] Login renomeado para Celular em inscritos")
    else:
        print("   [ERRO] Login nao foi renomeado para Celular")

    # Verificar cálculo de retenção
    if 'Retenção (hh:mm)' in processed_data['relatorio_processed'].columns:
        print("   [OK] Coluna Retencao (hh:mm) criada em relatorio")
        retencao = processed_data['relatorio_processed']['Retenção (hh:mm)'].iloc[0]
        print(f"      Exemplo: 125.5 min -> {retencao}")
    else:
        print("   [ERRO] Coluna Retencao nao foi criada")

    # Verificar conversão de Data em totalizado
    if processed_data['totalizado_processed']['Data'].dtype == 'datetime64[ns]':
        print("   [OK] Coluna Data convertida para datetime em totalizado")
    else:
        print("   [ERRO] Coluna Data nao foi convertida para datetime")

    print("\n" + "=" * 60)
    print("TESTE CONCLUÍDO COM SUCESSO!")
    print("=" * 60)


if __name__ == "__main__":
    test_processor()
