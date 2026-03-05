"""
Controlador principal que orquestra o fluxo de geração de relatórios.
"""

from typing import Dict, Optional, Callable, Tuple
import pandas as pd
import os
import time
from .data_loader import CSVLoader
from .data_processor import ReportDataProcessor
from .excel_generator import ExcelGenerator
from utils.logger import get_logger


class ReportController:
    """
    Orquestra o fluxo completo de geração de relatórios.

    Esta classe coordena as operações entre loader, processor e generator,
    mas não conhece detalhes de implementação de cada um (Dependency Inversion).
    """

    def __init__(
        self,
        loader: Optional[CSVLoader] = None,
        processor: Optional[ReportDataProcessor] = None,
        generator: Optional[ExcelGenerator] = None,
        progress_callback: Optional[Callable[[str], None]] = None
    ):
        """
        Inicializa o controller com suas dependências.

        Args:
            loader: Instância de CSVLoader (cria nova se None)
            processor: Instância de ReportDataProcessor (cria nova se None)
            generator: Instância de ExcelGenerator (cria nova se None)
            progress_callback: Função para reportar progresso

        Example:
            >>> controller = ReportController()
            >>> # Ou com dependências customizadas:
            >>> loader = CSVLoader(progress_callback=print)
            >>> controller = ReportController(loader=loader)
        """
        self.progress_callback = progress_callback

        # Logger
        self.logger = get_logger()

        # Injeção de dependências (cria instâncias se não fornecidas)
        self.loader = loader or CSVLoader(progress_callback=progress_callback)
        self.processor = processor or ReportDataProcessor(progress_callback=progress_callback)
        self.generator = generator or ExcelGenerator(progress_callback=progress_callback)

        # Cache de dados processados (para reutilização)
        self.raw_dataframes: Dict[str, pd.DataFrame] = {}
        self.processed_dataframes: Dict[str, pd.DataFrame] = {}

        # Log de inicialização
        self.logger.info("ReportController inicializado")

    def generate_report(
        self,
        file_paths: Dict[str, str],
        output_path: str
    ) -> Tuple[str, Dict]:
        """
        Gera relatório completo a partir de arquivos CSV.

        Este é o método principal que coordena todo o fluxo:
        1. Carrega CSVs
        2. Processa dados
        3. Gera Excel

        Args:
            file_paths: Dicionário {tipo: caminho}
                       Ex: {'inscritos': 'path/to/inscritos.csv', ...}
            output_path: Caminho onde salvar arquivo Excel

        Returns:
            Tupla (caminho_arquivo, estatísticas)
            - caminho_arquivo: Caminho completo do arquivo Excel gerado
            - estatísticas: Dict com métricas de processamento

        Raises:
            DataLoadError: Se houver erro ao carregar CSVs
            DataProcessingError: Se houver erro ao processar dados
            ExcelGenerationError: Se houver erro ao gerar Excel

        Example:
            >>> controller = ReportController()
            >>> result = controller.generate_report(
            ...     file_paths={
            ...         'inscritos': 'inscritos.csv',
            ...         'mensagens': 'mensagens.csv',
            ...         'relatorio_acesso': 'relatorio.csv',
            ...         'totalizado': 'totalizado.csv'
            ...     },
            ...     output_path='relatorio.xlsx'
            ... )
            >>> print(f"Relatório gerado: {result}")
            Relatório gerado: relatorio.xlsx
        """
        self._notify("Iniciando geração de relatório...")
        self.logger.info(f"Iniciando geração de relatório. Arquivos: {list(file_paths.keys())}")

        # Iniciar cronômetro
        start_time = time.time()

        try:
            # 1. Carregar dados
            self._notify("Etapa 1/3: Carregando arquivos CSV...")
            self.logger.info("Etapa 1/3: Carregando CSVs")
            self.raw_dataframes = self.loader.load_all(file_paths)
            self.logger.info(f"CSVs carregados: {sum(len(df) for df in self.raw_dataframes.values())} registros totais")

            # 2. Processar dados
            self._notify("Etapa 2/3: Processando dados...")
            self.logger.info("Etapa 2/3: Processando dados")
            self.processed_dataframes = self.processor.process_all(self.raw_dataframes)
            self.logger.info("Dados processados com sucesso")

            # 3. Gerar Excel
            self._notify("Etapa 3/3: Gerando arquivo Excel...")
            self.logger.info(f"Etapa 3/3: Gerando Excel em {output_path}")
            result = self.generator.generate(self.processed_dataframes, output_path)
            self.logger.info(f"Excel gerado com sucesso: {result}")

            # Calcular tempo total
            duration = time.time() - start_time

            # Coletar estatísticas
            stats = self._collect_statistics(file_paths, output_path, duration)

            self._notify(f"✓ Relatório gerado com sucesso: {result}")
            self.logger.info(f"Processamento concluído em {duration:.1f}s")

            return result, stats

        except Exception as e:
            self.logger.exception(f"Erro ao gerar relatório: {str(e)}")
            raise

    def load_data(self, file_paths: Dict[str, str]) -> Dict[str, pd.DataFrame]:
        """
        Carrega dados sem processar (útil para preview).

        Args:
            file_paths: Dicionário {tipo: caminho}

        Returns:
            Dicionário com DataFrames brutos

        Example:
            >>> controller = ReportController()
            >>> dfs = controller.load_data({'inscritos': 'inscritos.csv'})
            >>> print(dfs['inscritos'].head())
        """
        self._notify("Carregando dados...")
        self.raw_dataframes = self.loader.load_all(file_paths)
        return self.raw_dataframes

    def process_loaded_data(self) -> Dict[str, pd.DataFrame]:
        """
        Processa dados já carregados.

        Returns:
            Dicionário com DataFrames processados

        Raises:
            ValueError: Se dados não foram carregados antes

        Example:
            >>> controller = ReportController()
            >>> controller.load_data({'inscritos': 'inscritos.csv'})
            >>> processed = controller.process_loaded_data()
        """
        if not self.raw_dataframes:
            raise ValueError(
                "Nenhum dado carregado. Execute load_data() primeiro."
            )

        self._notify("Processando dados...")
        self.processed_dataframes = self.processor.process_all(self.raw_dataframes)
        return self.processed_dataframes

    def generate_excel(self, output_path: str) -> str:
        """
        Gera Excel a partir de dados já processados.

        Args:
            output_path: Caminho onde salvar arquivo Excel

        Returns:
            Caminho completo do arquivo gerado

        Raises:
            ValueError: Se dados não foram processados antes

        Example:
            >>> controller = ReportController()
            >>> controller.load_data({'inscritos': 'inscritos.csv'})
            >>> controller.process_loaded_data()
            >>> result = controller.generate_excel('output.xlsx')
        """
        if not self.processed_dataframes:
            raise ValueError(
                "Nenhum dado processado. Execute process_loaded_data() primeiro."
            )

        self._notify("Gerando arquivo Excel...")
        result = self.generator.generate(self.processed_dataframes, output_path)
        self._notify(f"✓ Arquivo gerado: {result}")
        return result

    def get_preview_data(
        self,
        df_type: str,
        num_rows: int = 5
    ) -> Optional[pd.DataFrame]:
        """
        Retorna preview dos dados brutos (primeiras linhas).

        Args:
            df_type: Tipo do DataFrame ('inscritos', 'mensagens', etc)
            num_rows: Número de linhas para preview (padrão: 5)

        Returns:
            DataFrame com primeiras linhas ou None se não carregado

        Example:
            >>> controller = ReportController()
            >>> controller.load_data({'inscritos': 'inscritos.csv'})
            >>> preview = controller.get_preview_data('inscritos', 5)
            >>> print(preview)
        """
        if df_type in self.raw_dataframes:
            return self.raw_dataframes[df_type].head(num_rows)
        return None

    def get_data_info(self) -> Dict[str, Dict[str, any]]:
        """
        Retorna informações sobre dados carregados.

        Returns:
            Dicionário com informações (registros, colunas, etc)

        Example:
            >>> controller = ReportController()
            >>> controller.load_data({'inscritos': 'inscritos.csv'})
            >>> info = controller.get_data_info()
            >>> print(info['inscritos']['num_rows'])
            1631
        """
        info = {}

        for df_type, df in self.raw_dataframes.items():
            info[df_type] = {
                'num_rows': len(df),
                'num_columns': len(df.columns),
                'columns': df.columns.tolist(),
                'memory_mb': df.memory_usage(deep=True).sum() / (1024 * 1024)
            }

        return info

    def clear_cache(self) -> None:
        """
        Limpa cache de dados carregados e processados.

        Útil para liberar memória após gerar relatório.

        Example:
            >>> controller = ReportController()
            >>> controller.generate_report(...)
            >>> controller.clear_cache()  # Libera memória
        """
        self.raw_dataframes.clear()
        self.processed_dataframes.clear()
        self._notify("Cache limpo")

    def _collect_statistics(
        self,
        file_paths: Dict[str, str],
        output_path: str,
        duration: float
    ) -> Dict:
        """
        Coleta estatísticas do processamento.

        Args:
            file_paths: Dicionário de arquivos processados
            output_path: Caminho do arquivo gerado
            duration: Tempo de execução em segundos

        Returns:
            Dicionário com estatísticas
        """
        stats = {
            'duration_seconds': duration,
            'total_records': sum(len(df) for df in self.raw_dataframes.values()),
            'files_processed': len(file_paths),
            'output_size_mb': 0,
            'details': {}
        }

        # Tamanho do arquivo gerado
        if os.path.exists(output_path):
            stats['output_size_mb'] = os.path.getsize(output_path) / (1024 ** 2)

        # Detalhes por tipo
        stats['details'] = {
            'inscritos': len(self.raw_dataframes.get('inscritos', [])),
            'mensagens': len(self.raw_dataframes.get('mensagens', [])),
            'acessos': len(self.raw_dataframes.get('relatorio_acesso', [])),
            'retencao': len(self.raw_dataframes.get('totalizado', []))
        }

        # Contabilizar enquetes
        enquete_keys = [k for k in self.raw_dataframes if k.startswith('enquete_')]
        if enquete_keys:
            stats['details']['enquetes'] = {
                k: len(self.raw_dataframes[k]) for k in sorted(enquete_keys)
            }

        return stats

    def _notify(self, message: str) -> None:
        """
        Notifica progresso via callback.

        Args:
            message: Mensagem de status
        """
        if self.progress_callback:
            self.progress_callback(message)
