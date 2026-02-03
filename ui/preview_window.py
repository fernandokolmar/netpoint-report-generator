"""
Janela de preview de dados CSV.

Permite visualizar primeiras linhas de um DataFrame antes de processar.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional
import pandas as pd


class PreviewWindow:
    """
    Janela modal para preview de dados CSV.

    Mostra primeiras N linhas de um DataFrame em formato de tabela,
    com estatísticas básicas (total de linhas/colunas).
    """

    def __init__(
        self,
        parent: tk.Tk,
        df: pd.DataFrame,
        title: str,
        num_rows: int = 100,
        num_cols: int = 10
    ):
        """
        Inicializa janela de preview.

        Args:
            parent: Janela pai
            df: DataFrame para visualizar
            title: Título da janela
            num_rows: Número máximo de linhas a mostrar (padrão: 100)
            num_cols: Número máximo de colunas a mostrar (padrão: 10)
        """
        self.window = tk.Toplevel(parent)
        self.window.title(f"Preview: {title}")
        self.window.geometry("900x500")
        self.window.transient(parent)  # Manter sempre acima da janela pai

        self.df = df
        self.num_rows = min(num_rows, len(df))
        self.num_cols = min(num_cols, len(df.columns))

        self._create_widgets()

    def _create_widgets(self) -> None:
        """Cria todos os widgets da janela."""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Estatísticas no topo
        self._create_stats_section(main_frame)

        # Tabela de dados
        self._create_table_section(main_frame)

        # Botões na parte inferior
        self._create_buttons_section(main_frame)

    def _create_stats_section(self, parent: ttk.Frame) -> None:
        """
        Cria seção de estatísticas.

        Args:
            parent: Frame pai onde adicionar os widgets
        """
        stats_frame = ttk.LabelFrame(parent, text="Estatísticas", padding="10")
        stats_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # Informações do DataFrame
        total_rows = len(self.df)
        total_cols = len(self.df.columns)
        showing_rows = self.num_rows
        showing_cols = self.num_cols

        info_text = (
            f"📊 Total: {total_rows:,} linhas × {total_cols} colunas  |  "
            f"👁 Mostrando: {showing_rows} linhas × {showing_cols} colunas"
        )

        if showing_rows < total_rows:
            info_text += f"  (primeiras {showing_rows} de {total_rows:,})"

        if showing_cols < total_cols:
            info_text += f"  (primeiras {showing_cols} de {total_cols})"

        ttk.Label(stats_frame, text=info_text).pack()

    def _create_table_section(self, parent: ttk.Frame) -> None:
        """
        Cria seção da tabela com dados.

        Args:
            parent: Frame pai onde adicionar os widgets
        """
        table_frame = ttk.Frame(parent)
        table_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        # Criar Treeview
        columns = self.df.columns[:self.num_cols].tolist()
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='tree headings',
            height=20
        )

        # Configurar coluna #0 (índice)
        self.tree.heading('#0', text='#', anchor=tk.W)
        self.tree.column('#0', width=50, minwidth=50, stretch=False)

        # Configurar colunas de dados
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.W)
            # Largura baseada no tamanho do nome da coluna
            col_width = max(len(str(col)) * 8, 100)
            self.tree.column(col, width=col_width, minwidth=80)

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Grid layout
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # Adicionar dados
        self._populate_table(columns)

    def _populate_table(self, columns: list) -> None:
        """
        Popula tabela com dados do DataFrame.

        Args:
            columns: Lista de colunas a exibir
        """
        # Adicionar primeiras N linhas
        for idx, row in self.df.head(self.num_rows).iterrows():
            # Valores da linha (truncar strings longas)
            values = []
            for col in columns:
                value = str(row[col])
                # Truncar strings longas
                if len(value) > 50:
                    value = value[:47] + "..."
                values.append(value)

            # Inserir na árvore (índice na coluna #0)
            self.tree.insert('', 'end', text=str(idx), values=values)

    def _create_buttons_section(self, parent: ttk.Frame) -> None:
        """
        Cria seção de botões.

        Args:
            parent: Frame pai onde adicionar os widgets
        """
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, pady=(10, 0))

        # Botão Fechar
        ttk.Button(
            button_frame,
            text="Fechar",
            command=self.window.destroy
        ).pack(side=tk.LEFT, padx=5)

        # Botão Exportar Info (opcional - para debug)
        ttk.Button(
            button_frame,
            text="Ver Info do DataFrame",
            command=self._show_dataframe_info
        ).pack(side=tk.LEFT, padx=5)

    def _show_dataframe_info(self) -> None:
        """Mostra informações detalhadas do DataFrame em nova janela."""
        info_window = tk.Toplevel(self.window)
        info_window.title("DataFrame Info")
        info_window.geometry("500x400")

        # Text widget com scrollbar
        text_frame = ttk.Frame(info_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        text = tk.Text(text_frame, wrap=tk.NONE)
        vsb = ttk.Scrollbar(text_frame, orient="vertical", command=text.yview)
        hsb = ttk.Scrollbar(text_frame, orient="horizontal", command=text.xview)
        text.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))

        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        # Coletar informações
        info_text = f"""DataFrame Information
{'=' * 50}

Shape: {self.df.shape[0]:,} rows × {self.df.shape[1]} columns

Columns ({len(self.df.columns)}):
"""
        for i, col in enumerate(self.df.columns, 1):
            dtype = self.df[col].dtype
            non_null = self.df[col].notna().sum()
            null_count = self.df[col].isna().sum()
            info_text += f"\n{i}. {col}"
            info_text += f"\n   Type: {dtype}"
            info_text += f"\n   Non-Null: {non_null:,} ({non_null/len(self.df)*100:.1f}%)"
            if null_count > 0:
                info_text += f"\n   Null: {null_count:,} ({null_count/len(self.df)*100:.1f}%)"
            info_text += "\n"

        # Adicionar info sobre memória
        memory_usage = self.df.memory_usage(deep=True).sum() / (1024**2)
        info_text += f"\n{'=' * 50}\n"
        info_text += f"Memory Usage: {memory_usage:.2f} MB\n"

        text.insert('1.0', info_text)
        text.config(state='disabled')

        # Botão fechar
        ttk.Button(
            info_window,
            text="Fechar",
            command=info_window.destroy
        ).pack(pady=10)


def show_preview(parent: tk.Tk, df: pd.DataFrame, title: str) -> None:
    """
    Função auxiliar para mostrar preview de DataFrame.

    Args:
        parent: Janela pai
        df: DataFrame para visualizar
        title: Título da janela

    Example:
        >>> show_preview(root, df_inscritos, "Inscritos")
    """
    PreviewWindow(parent, df, title)
