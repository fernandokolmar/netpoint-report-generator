"""
Janela de estatísticas de processamento.

Mostra informações detalhadas após geração bem-sucedida de relatório.
"""

import tkinter as tk
from tkinter import ttk
import os
import subprocess
import platform


class StatsWindow:
    """
    Janela modal que exibe estatísticas de processamento.

    Mostra métricas como tempo de execução, registros processados,
    tamanho do arquivo gerado, com botões para abrir arquivo/pasta.
    """

    def __init__(self, parent: tk.Tk, stats: dict, output_path: str):
        """
        Inicializa janela de estatísticas.

        Args:
            parent: Janela pai
            stats: Dicionário com estatísticas do processamento
            output_path: Caminho do arquivo Excel gerado
        """
        self.window = tk.Toplevel(parent)
        self.window.title("Relatório Gerado com Sucesso")
        self.window.geometry("500x450")
        self.window.transient(parent)
        self.window.resizable(False, False)

        self.stats = stats
        self.output_path = output_path

        self._create_widgets()

        # Centralizar janela
        self.window.update_idletasks()
        self._center_window()

    def _center_window(self) -> None:
        """Centraliza janela na tela."""
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def _create_widgets(self) -> None:
        """Cria todos os widgets da janela."""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Ícone de sucesso
        success_frame = ttk.Frame(main_frame)
        success_frame.pack(pady=(0, 15))

        success_label = ttk.Label(
            success_frame,
            text="✓",
            font=('Arial', 48, 'bold'),
            foreground='green'
        )
        success_label.pack()

        ttk.Label(
            success_frame,
            text="Relatório gerado com sucesso!",
            font=('Arial', 14, 'bold')
        ).pack()

        # Informações do arquivo
        self._create_file_info_section(main_frame)

        # Estatísticas de processamento
        self._create_stats_section(main_frame)

        # Botões de ação
        self._create_buttons_section(main_frame)

    def _create_file_info_section(self, parent: ttk.Frame) -> None:
        """
        Cria seção de informações do arquivo.

        Args:
            parent: Frame pai
        """
        file_frame = ttk.LabelFrame(parent, text="Arquivo Gerado", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 10))

        # Nome do arquivo
        filename = os.path.basename(self.output_path)
        ttk.Label(
            file_frame,
            text=f"📄 {filename}",
            font=('Arial', 10, 'bold')
        ).pack(anchor=tk.W)

        # Caminho completo (truncado se muito longo)
        path_display = self.output_path
        if len(path_display) > 60:
            path_display = "..." + path_display[-57:]

        ttk.Label(
            file_frame,
            text=f"📁 {path_display}",
            foreground='gray'
        ).pack(anchor=tk.W, pady=(5, 0))

        # Tamanho do arquivo
        file_size_mb = self.stats.get('output_size_mb', 0)
        ttk.Label(
            file_frame,
            text=f"💾 Tamanho: {file_size_mb:.2f} MB",
            foreground='gray'
        ).pack(anchor=tk.W)

    def _create_stats_section(self, parent: ttk.Frame) -> None:
        """
        Cria seção de estatísticas.

        Args:
            parent: Frame pai
        """
        stats_frame = ttk.LabelFrame(parent, text="Estatísticas", padding="10")
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Text widget para estatísticas
        text = tk.Text(
            stats_frame,
            height=10,
            wrap=tk.WORD,
            font=('Consolas', 10),
            relief=tk.FLAT,
            background='#F5F5F5'
        )
        text.pack(fill=tk.BOTH, expand=True)

        # Formatar estatísticas
        stats_text = self._format_stats()
        text.insert('1.0', stats_text)
        text.config(state='disabled')

    def _format_stats(self) -> str:
        """
        Formata estatísticas em texto legível.

        Returns:
            String formatada com estatísticas
        """
        duration = self.stats.get('duration_seconds', 0)
        minutes = int(duration // 60)
        seconds = int(duration % 60)

        total_records = self.stats.get('total_records', 0)
        files_processed = self.stats.get('files_processed', 0)
        details = self.stats.get('details', {})

        text = f"""
📊 RESUMO DO PROCESSAMENTO
{'─' * 45}

⏱  Tempo de execução: {minutes}m {seconds}s

📁 Arquivos processados: {files_processed}

📈 Total de registros: {total_records:,}

DETALHES POR TIPO:
"""

        # Detalhes por tipo de arquivo
        if details:
            text += f"\n  • Inscritos:        {details.get('inscritos', 0):,} registros"
            text += f"\n  • Mensagens:        {details.get('mensagens', 0):,} registros"
            text += f"\n  • Acessos:          {details.get('acessos', 0):,} registros"
            text += f"\n  • Retenção na live: {details.get('retencao', 0):,} registros"

        # Velocidade de processamento
        if duration > 0 and total_records > 0:
            records_per_second = total_records / duration
            text += f"\n\n⚡ Velocidade: {records_per_second:.0f} registros/segundo"

        return text.strip()

    def _create_buttons_section(self, parent: ttk.Frame) -> None:
        """
        Cria seção de botões.

        Args:
            parent: Frame pai
        """
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X)

        # Botão Abrir Arquivo
        ttk.Button(
            button_frame,
            text="📂 Abrir Arquivo",
            command=self._open_file,
            width=15
        ).pack(side=tk.LEFT, padx=(0, 5))

        # Botão Abrir Pasta
        ttk.Button(
            button_frame,
            text="📁 Abrir Pasta",
            command=self._open_folder,
            width=15
        ).pack(side=tk.LEFT, padx=5)

        # Botão Fechar
        ttk.Button(
            button_frame,
            text="Fechar",
            command=self.window.destroy,
            width=15
        ).pack(side=tk.RIGHT)

    def _open_file(self) -> None:
        """Abre arquivo Excel gerado."""
        try:
            if platform.system() == 'Windows':
                os.startfile(self.output_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', self.output_path])
            else:  # Linux
                subprocess.run(['xdg-open', self.output_path])
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror(
                "Erro",
                f"Não foi possível abrir o arquivo:\n{str(e)}"
            )

    def _open_folder(self) -> None:
        """Abre pasta contendo o arquivo."""
        try:
            folder_path = os.path.dirname(self.output_path)

            if platform.system() == 'Windows':
                os.startfile(folder_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', folder_path])
            else:  # Linux
                subprocess.run(['xdg-open', folder_path])
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror(
                "Erro",
                f"Não foi possível abrir a pasta:\n{str(e)}"
            )
