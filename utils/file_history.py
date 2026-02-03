"""
Gerenciamento de histórico de arquivos recentes.

Mantém registro dos últimos conjuntos de arquivos usados para
facilitar reprocessamento.
"""

import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime
import os


class FileHistory:
    """
    Gerencia histórico de conjuntos de arquivos recentemente usados.

    Salva histórico em arquivo JSON para persistência entre sessões.
    """

    def __init__(self, config_path: str = "~/.prsa/history.json", max_history: int = 5):
        """
        Inicializa gerenciador de histórico.

        Args:
            config_path: Caminho do arquivo de configuração JSON
            max_history: Número máximo de conjuntos a manter (padrão: 5)
        """
        self.config_path = Path(config_path).expanduser()
        self.max_history = max_history

        # Criar diretório se não existir
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        # Carregar histórico existente
        self.history = self._load_history()

    def _load_history(self) -> Dict:
        """
        Carrega histórico do arquivo JSON.

        Returns:
            Dicionário com histórico ou estrutura padrão se arquivo não existir
        """
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                # Se arquivo corrompido, criar novo
                return self._default_history()
        else:
            return self._default_history()

    def _default_history(self) -> Dict:
        """
        Retorna estrutura padrão do histórico.

        Returns:
            Dicionário com estrutura padrão
        """
        return {
            'recent_sets': [],
            'max_history': self.max_history
        }

    def _save_history(self) -> None:
        """Salva histórico no arquivo JSON."""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Erro ao salvar histórico: {e}")

    def add_set(self, name: str, files: Dict[str, str]) -> None:
        """
        Adiciona conjunto de arquivos ao histórico.

        Se conjunto já existir (mesmo conjunto de caminhos),
        atualiza timestamp ao invés de duplicar.

        Args:
            name: Nome descritivo do conjunto
            files: Dicionário {tipo: caminho}
                  Ex: {'inscritos': 'path/to/file.csv', ...}

        Example:
            >>> history = FileHistory()
            >>> history.add_set(
            ...     "Evento ABC - Jan 2026",
            ...     {
            ...         'inscritos': 'C:/Data/inscritos.csv',
            ...         'mensagens': 'C:/Data/mensagens.csv',
            ...         'relatorio_acesso': 'C:/Data/acessos.csv',
            ...         'totalizado': 'C:/Data/totalizado.csv'
            ...     }
            ... )
        """
        # Verificar se conjunto já existe (mesmos arquivos)
        for i, existing_set in enumerate(self.history['recent_sets']):
            if existing_set['files'] == files:
                # Remover duplicata antiga
                self.history['recent_sets'].pop(i)
                break

        # Criar novo registro
        new_set = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'name': name,
            'files': files
        }

        # Adicionar no início da lista
        self.history['recent_sets'].insert(0, new_set)

        # Manter apenas últimos N conjuntos
        self.history['recent_sets'] = self.history['recent_sets'][:self.max_history]

        # Salvar
        self._save_history()

    def get_recent(self, limit: int = 5) -> List[Dict]:
        """
        Retorna conjuntos recentes, removendo arquivos inexistentes.

        Args:
            limit: Número máximo de conjuntos a retornar (padrão: 5)

        Returns:
            Lista de dicionários com conjuntos recentes válidos

        Example:
            >>> history = FileHistory()
            >>> recent = history.get_recent(limit=3)
            >>> for item in recent:
            ...     print(f"{item['name']} - {item['timestamp']}")
        """
        valid_sets = []

        for item in self.history['recent_sets'][:limit]:
            # Verificar se todos os arquivos ainda existem
            all_exist = all(
                os.path.exists(path) for path in item['files'].values()
            )

            if all_exist:
                valid_sets.append(item)
            else:
                # Marcar para remoção (arquivos não existem mais)
                # Vamos limpar na próxima vez que add_set for chamado
                pass

        # Se encontramos conjuntos inválidos, limpar histórico
        if len(valid_sets) < len(self.history['recent_sets'][:limit]):
            self._cleanup_invalid_sets()

        return valid_sets

    def _cleanup_invalid_sets(self) -> None:
        """Remove conjuntos cujos arquivos não existem mais."""
        valid_sets = []

        for item in self.history['recent_sets']:
            # Verificar se todos os arquivos existem
            all_exist = all(
                os.path.exists(path) for path in item['files'].values()
            )

            if all_exist:
                valid_sets.append(item)

        # Atualizar histórico apenas com conjuntos válidos
        self.history['recent_sets'] = valid_sets
        self._save_history()

    def clear(self) -> None:
        """Limpa todo o histórico."""
        self.history['recent_sets'] = []
        self._save_history()

    def remove_set(self, index: int) -> None:
        """
        Remove conjunto específico do histórico.

        Args:
            index: Índice do conjunto a remover (0-based)

        Raises:
            IndexError: Se índice for inválido
        """
        if 0 <= index < len(self.history['recent_sets']):
            self.history['recent_sets'].pop(index)
            self._save_history()
        else:
            raise IndexError(f"Índice inválido: {index}")

    def get_by_index(self, index: int) -> Dict:
        """
        Retorna conjunto específico por índice.

        Args:
            index: Índice do conjunto (0-based)

        Returns:
            Dicionário com informações do conjunto

        Raises:
            IndexError: Se índice for inválido
        """
        if 0 <= index < len(self.history['recent_sets']):
            return self.history['recent_sets'][index]
        else:
            raise IndexError(f"Índice inválido: {index}")

    def generate_name(self, files: Dict[str, str]) -> str:
        """
        Gera nome automático baseado nos arquivos.

        Args:
            files: Dicionário de arquivos

        Returns:
            Nome sugerido para o conjunto

        Example:
            >>> history = FileHistory()
            >>> name = history.generate_name({
            ...     'inscritos': 'C:/Events/2026/Jan/evento_abc/inscritos.csv',
            ...     'mensagens': 'C:/Events/2026/Jan/evento_abc/mensagens.csv',
            ...     ...
            ... })
            >>> print(name)
            'evento_abc - 2026-01-29 15:30'
        """
        # Tentar usar nome da pasta pai
        if files:
            first_file = list(files.values())[0]
            folder_name = Path(first_file).parent.name

            # Adicionar timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
            return f"{folder_name} - {timestamp}"
        else:
            return f"Conjunto - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
