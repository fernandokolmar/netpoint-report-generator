#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Netpoint Report Generator
Aplicação para processar dados de videoconferência e gerar relatórios em Excel
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import os
from typing import Dict
import threading

# Importar módulos do core
from core.controller import ReportController
from core.exceptions import PRSAException
from ui.preview_window import show_preview
from ui.stats_window import StatsWindow
from utils.file_history import FileHistory
from utils.updater import check_for_updates, download_and_apply, get_current_exe, is_running_as_exe
from config import settings


class VideoConferenceReportGenerator:
    """
    Interface gráfica para geração de relatórios de videoconferência.

    Classe focada apenas em UI, delegando lógica de negócio ao ReportController.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"{settings.APP_NAME} v{settings.APP_VERSION}")
        self.root.geometry("820x680")

        # Configurar ícone da aplicação
        self._set_app_icon()

        # Variáveis para armazenar caminhos dos arquivos (aba Evento)
        self.file_paths: Dict[str, str] = {
            'inscritos': '',
            'mensagens': '',
            'chat': '',
            'relatorio_acesso': '',
            'totalizado': '',
            'presenca_zoom': '',
            'inscritos_zoom': ''
        }

        # Lista de enquetes dinâmicas (aba Evento)
        self.enquete_rows = []

        # Lista de arquivos Zoom dinâmicos (aba Zoom)
        self.zoom_rows = []
        self.zoom_file_paths: Dict[str, str] = {}
        self.zoom_inscritos_path: str = ''  # inscritos Zoom da aba Zoom

        # Controller (Dependency Injection)
        self.controller = ReportController(progress_callback=self.log)

        # Histórico de arquivos
        self.file_history = FileHistory()

        self.create_widgets()
        self.create_menu()

        # Verificar atualizações em background (apenas quando rodando como .exe)
        if is_running_as_exe():
            self.root.after(2000, self._check_for_updates)

    def _set_app_icon(self) -> None:
        """Configura o ícone da aplicação."""
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
            else:
                icon_png = os.path.join(os.path.dirname(__file__), 'assets', 'icon.png')
                if os.path.exists(icon_png):
                    icon = tk.PhotoImage(file=icon_png)
                    self.root.iconphoto(True, icon)
        except Exception:
            pass

    def create_widgets(self):
        """Criar interface gráfica com duas abas."""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Título
        title_label = ttk.Label(main_frame, text=settings.APP_NAME, font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 8))

        # Notebook (abas)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.rowconfigure(1, weight=1)

        # --- Aba 1: Relatório Evento ---
        self.tab_evento = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.tab_evento, text="  Relatório Evento  ")
        self.tab_evento.columnconfigure(0, weight=1)
        self.tab_evento.rowconfigure(1, weight=1)
        self._build_evento_tab(self.tab_evento)

        # --- Aba 2: Relatório Zoom ---
        self.tab_zoom = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.tab_zoom, text="  Relatório Zoom  ")
        self.tab_zoom.columnconfigure(0, weight=1)
        self.tab_zoom.rowconfigure(1, weight=1)
        self._build_zoom_tab(self.tab_zoom)

    # -------------------------------------------------------------------------
    # Aba 1: Relatório Evento
    # -------------------------------------------------------------------------

    def _build_evento_tab(self, parent: ttk.Frame) -> None:
        """Constrói o conteúdo da aba Relatório Evento."""
        # Seção de arquivos
        files_frame = ttk.LabelFrame(parent, text="Carregar Arquivos CSV", padding="10")
        files_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 8))
        files_frame.columnconfigure(1, weight=1)

        # Inscritos (opcional)
        ttk.Label(files_frame, text="Arquivo Inscritos (opcional):").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=4)
        self.inscritos_entry = ttk.Entry(files_frame, width=50)
        self.inscritos_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=4)
        ttk.Button(files_frame, text="Procurar",
                   command=lambda: self.load_file('inscritos', self.inscritos_entry)).grid(
            row=0, column=2, padx=5, pady=4)
        ttk.Button(files_frame, text="Preview",
                   command=lambda: self.show_file_preview('inscritos')).grid(
            row=0, column=3, padx=5, pady=4)

        # Mensagens (opcional)
        ttk.Label(files_frame, text="Arquivo Mensagens (opcional):").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=4)
        self.mensagens_entry = ttk.Entry(files_frame, width=50)
        self.mensagens_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=4)
        ttk.Button(files_frame, text="Procurar",
                   command=lambda: self.load_file('mensagens', self.mensagens_entry)).grid(
            row=1, column=2, padx=5, pady=4)
        ttk.Button(files_frame, text="Preview",
                   command=lambda: self.show_file_preview('mensagens')).grid(
            row=1, column=3, padx=5, pady=4)

        # Chat (opcional)
        ttk.Label(files_frame, text="Arquivo Chat (opcional):").grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=4)
        self.chat_entry = ttk.Entry(files_frame, width=50)
        self.chat_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=4)
        ttk.Button(files_frame, text="Procurar",
                   command=lambda: self.load_file('chat', self.chat_entry)).grid(
            row=2, column=2, padx=5, pady=4)
        ttk.Button(files_frame, text="Preview",
                   command=lambda: self.show_file_preview('chat')).grid(
            row=2, column=3, padx=5, pady=4)

        # Relatório de Acesso
        ttk.Label(files_frame, text="Relatório de Acesso:").grid(
            row=3, column=0, sticky=tk.W, padx=5, pady=4)
        self.relatorio_entry = ttk.Entry(files_frame, width=50)
        self.relatorio_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=4)
        ttk.Button(files_frame, text="Procurar",
                   command=lambda: self.load_file('relatorio_acesso', self.relatorio_entry)).grid(
            row=3, column=2, padx=5, pady=4)
        ttk.Button(files_frame, text="Preview",
                   command=lambda: self.show_file_preview('relatorio_acesso')).grid(
            row=3, column=3, padx=5, pady=4)

        # Totalizado
        ttk.Label(files_frame, text="Arquivo Totalizado:").grid(
            row=4, column=0, sticky=tk.W, padx=5, pady=4)
        self.totalizado_entry = ttk.Entry(files_frame, width=50)
        self.totalizado_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=5, pady=4)
        ttk.Button(files_frame, text="Procurar",
                   command=lambda: self.load_file('totalizado', self.totalizado_entry)).grid(
            row=4, column=2, padx=5, pady=4)
        ttk.Button(files_frame, text="Preview",
                   command=lambda: self.show_file_preview('totalizado')).grid(
            row=4, column=3, padx=5, pady=4)

        # Participantes Zoom (opcional)
        ttk.Label(files_frame, text="Participantes Zoom (opcional):").grid(
            row=5, column=0, sticky=tk.W, padx=5, pady=4)
        self.zoom_entry = ttk.Entry(files_frame, width=50)
        self.zoom_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), padx=5, pady=4)
        ttk.Button(files_frame, text="Procurar",
                   command=lambda: self.load_file('presenca_zoom', self.zoom_entry)).grid(
            row=5, column=2, padx=5, pady=4)
        ttk.Button(files_frame, text="Preview",
                   command=lambda: self.show_file_preview('presenca_zoom')).grid(
            row=5, column=3, padx=5, pady=4)

        # Inscrições Zoom (opcional)
        ttk.Label(files_frame, text="Inscrições Zoom (opcional):").grid(
            row=6, column=0, sticky=tk.W, padx=5, pady=4)
        self.inscritos_zoom_entry = ttk.Entry(files_frame, width=50)
        self.inscritos_zoom_entry.grid(row=6, column=1, sticky=(tk.W, tk.E), padx=5, pady=4)
        ttk.Button(files_frame, text="Procurar",
                   command=lambda: self.load_file('inscritos_zoom', self.inscritos_zoom_entry)).grid(
            row=6, column=2, padx=5, pady=4)
        ttk.Button(files_frame, text="Preview",
                   command=lambda: self.show_file_preview('inscritos_zoom')).grid(
            row=6, column=3, padx=5, pady=4)

        # Separador e seção de Enquetes
        ttk.Separator(files_frame, orient='horizontal').grid(
            row=7, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=6)

        enquetes_header = ttk.Frame(files_frame)
        enquetes_header.grid(row=8, column=0, columnspan=4, sticky=(tk.W, tk.E), padx=5, pady=2)
        ttk.Label(enquetes_header, text="Enquetes (opcional):", font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
        ttk.Button(enquetes_header, text="+ Adicionar Enquete",
                   command=self._add_enquete_row).pack(side=tk.LEFT, padx=10)

        self.enquetes_container = ttk.Frame(files_frame)
        self.enquetes_container.grid(row=9, column=0, columnspan=4, sticky=(tk.W, tk.E))
        self.enquetes_container.columnconfigure(1, weight=1)

        # Log
        log_frame = ttk.LabelFrame(parent, text="Status", padding="8")
        log_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 8))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)

        self.log_text = tk.Text(log_frame, height=7, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=scrollbar.set)

        # Barra de progresso
        self.progress_bar = ttk.Progressbar(parent, mode='indeterminate', length=600)
        self.progress_bar.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 6))

        # Botões
        action_frame = ttk.Frame(parent)
        action_frame.grid(row=3, column=0, pady=(0, 4))

        self.process_button = ttk.Button(
            action_frame,
            text="Processar e Gerar Relatório",
            command=self.process_and_generate,
            style='Accent.TButton'
        )
        self.process_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Limpar", command=self.clear_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Sair", command=self.root.quit).pack(side=tk.LEFT, padx=5)

        self.log("Sistema pronto. Carregue os arquivos CSV para começar.")

    # -------------------------------------------------------------------------
    # Aba 2: Relatório Zoom
    # -------------------------------------------------------------------------

    def _build_zoom_tab(self, parent: ttk.Frame) -> None:
        """Constrói o conteúdo da aba Relatório Zoom."""
        desc_frame = ttk.LabelFrame(parent, text="Sobre", padding="8")
        desc_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 8))
        ttk.Label(
            desc_frame,
            text=(
                "Gere um relatório Excel com presença consolidada do Zoom, sem precisar dos\n"
                "arquivos do evento. Adicione um ou mais relatórios CSV exportados pelo Zoom."
            ),
            justify=tk.LEFT
        ).pack(anchor=tk.W)

        # Seção de arquivos Zoom
        zoom_files_frame = ttk.LabelFrame(parent, text="Arquivos Zoom", padding="10")
        zoom_files_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 8))
        zoom_files_frame.columnconfigure(0, weight=1)

        # Botão para adicionar arquivos
        add_btn_frame = ttk.Frame(zoom_files_frame)
        add_btn_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 6))
        ttk.Button(add_btn_frame, text="+ Adicionar Participantes Zoom",
                   command=self._add_zoom_row).pack(side=tk.LEFT)

        # Container dinâmico
        self.zoom_container = ttk.Frame(zoom_files_frame)
        self.zoom_container.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.zoom_container.columnconfigure(1, weight=1)

        # Inscritos Zoom (opcional)
        ttk.Separator(zoom_files_frame, orient='horizontal').grid(
            row=2, column=0, sticky=(tk.W, tk.E), pady=6)
        inscritos_zoom_frame = ttk.Frame(zoom_files_frame)
        inscritos_zoom_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        inscritos_zoom_frame.columnconfigure(1, weight=1)
        ttk.Label(inscritos_zoom_frame, text="Inscrições Zoom (opcional):").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=4)
        self.zoom_inscritos_entry = ttk.Entry(inscritos_zoom_frame, width=50)
        self.zoom_inscritos_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=4)
        ttk.Button(inscritos_zoom_frame, text="Procurar",
                   command=self._load_zoom_inscritos_file).grid(row=0, column=2, padx=5, pady=4)

        # Log do Zoom
        zoom_log_frame = ttk.LabelFrame(parent, text="Status", padding="8")
        zoom_log_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 8))
        zoom_log_frame.columnconfigure(0, weight=1)
        zoom_log_frame.rowconfigure(0, weight=1)
        parent.rowconfigure(2, weight=1)

        self.zoom_log_text = tk.Text(zoom_log_frame, height=7, width=70)
        self.zoom_log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        zoom_scrollbar = ttk.Scrollbar(zoom_log_frame, orient="vertical",
                                       command=self.zoom_log_text.yview)
        zoom_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.zoom_log_text.configure(yscrollcommand=zoom_scrollbar.set)

        # Barra de progresso
        self.zoom_progress_bar = ttk.Progressbar(parent, mode='indeterminate', length=600)
        self.zoom_progress_bar.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 6))

        # Botões
        zoom_action_frame = ttk.Frame(parent)
        zoom_action_frame.grid(row=4, column=0, pady=(0, 4))

        self.zoom_process_button = ttk.Button(
            zoom_action_frame,
            text="Gerar Relatório Zoom",
            command=self.process_zoom_report,
            style='Accent.TButton'
        )
        self.zoom_process_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(zoom_action_frame, text="Limpar", command=self.clear_zoom).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(zoom_action_frame, text="Sair", command=self.root.quit).pack(
            side=tk.LEFT, padx=5)

        self.zoom_log("Aba Relatório Zoom pronta. Adicione arquivos CSV do Zoom para começar.")

    def _add_zoom_row(self) -> None:
        """Adiciona uma nova linha de arquivo Zoom na aba Relatório Zoom."""
        idx = len(self.zoom_rows) + 1
        key = f'zoom_{idx}'

        row_frame = ttk.Frame(self.zoom_container)
        row_frame.grid(row=idx - 1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=2)
        row_frame.columnconfigure(1, weight=1)

        ttk.Label(row_frame, text=f"Zoom {idx:02d}:").grid(row=0, column=0, sticky=tk.W, padx=5)

        entry = ttk.Entry(row_frame, width=50)
        entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

        ttk.Button(row_frame, text="Procurar",
                   command=lambda k=key, e=entry: self._load_zoom_file(k, e)).grid(
            row=0, column=2, padx=5)

        ttk.Button(row_frame, text="×",
                   command=lambda k=key, f=row_frame: self._remove_zoom_row(k, f)).grid(
            row=0, column=3, padx=2)

        self.zoom_rows.append((key, entry, row_frame))
        self.zoom_file_paths[key] = ''
        self.zoom_log(f"Zoom {idx:02d} adicionado. Selecione o arquivo CSV do Zoom.")

    def _remove_zoom_row(self, key: str, row_frame: ttk.Frame) -> None:
        """Remove uma linha de arquivo Zoom e renumera as restantes."""
        self.zoom_file_paths.pop(key, None)
        self.zoom_rows = [(k, e, f) for k, e, f in self.zoom_rows if k != key]
        row_frame.destroy()

        old_rows = self.zoom_rows[:]
        self.zoom_rows = []
        for new_idx, (old_key, entry, frame) in enumerate(old_rows, start=1):
            new_key = f'zoom_{new_idx}'
            old_path = self.zoom_file_paths.pop(old_key, '')
            self.zoom_file_paths[new_key] = old_path
            self.zoom_rows.append((new_key, entry, frame))
            for widget in frame.winfo_children():
                if isinstance(widget, ttk.Label):
                    widget.config(text=f"Zoom {new_idx:02d}:")
                    break

        self.zoom_log(f"Arquivo Zoom removido. Total: {len(self.zoom_rows)} arquivo(s).")

    def _load_zoom_file(self, key: str, entry: ttk.Entry) -> None:
        """Abre diálogo para selecionar arquivo CSV do Zoom."""
        file_path = filedialog.askopenfilename(
            title="Selecionar Relatório CSV do Zoom",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.zoom_file_paths[key] = file_path
            entry.delete(0, tk.END)
            entry.insert(0, file_path)
            self.zoom_log(f"Arquivo {key} carregado: {os.path.basename(file_path)}")

    def _load_zoom_inscritos_file(self) -> None:
        """Abre diálogo para selecionar arquivo CSV de inscrições Zoom (aba Zoom)."""
        file_path = filedialog.askopenfilename(
            title="Selecionar Inscrições Zoom (CSV)",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.zoom_inscritos_path = file_path
            self.zoom_inscritos_entry.delete(0, tk.END)
            self.zoom_inscritos_entry.insert(0, file_path)
            self.zoom_log(f"Inscrições Zoom carregado: {os.path.basename(file_path)}")

    def zoom_log(self, message: str) -> None:
        """Adiciona mensagem ao log da aba Zoom."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.zoom_log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.zoom_log_text.see(tk.END)
        self.root.update()

    def clear_zoom(self) -> None:
        """Limpa todos os campos da aba Relatório Zoom."""
        for _, _, frame in self.zoom_rows:
            frame.destroy()
        self.zoom_rows = []
        self.zoom_file_paths = {}
        self.zoom_inscritos_path = ''
        self.zoom_inscritos_entry.delete(0, tk.END)
        self.zoom_log("Campos limpos.")

    def process_zoom_report(self) -> None:
        """Coordena a geração do Relatório Zoom."""
        # Verificar se há pelo menos um arquivo
        valid_paths = {k: v for k, v in self.zoom_file_paths.items() if v}
        if not valid_paths:
            messagebox.showerror(
                "Erro",
                "Adicione pelo menos um arquivo Zoom antes de gerar o relatório."
            )
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile=f"Netpoint_Zoom_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
        if not output_path:
            self.zoom_log("Operação cancelada pelo usuário.")
            return

        self.zoom_process_button.config(state='disabled')
        self.zoom_progress_bar.start(10)

        thread = threading.Thread(
            target=self._process_zoom_in_background,
            args=(valid_paths, output_path),
            daemon=True
        )
        thread.start()

    def _process_zoom_in_background(self, zoom_paths: dict, output_path: str) -> None:
        """Executa geração do Relatório Zoom em background thread."""
        # Redirecionar log do controller para a aba Zoom durante este processamento
        original_callback = self.controller.progress_callback

        def zoom_log_redirect(msg):
            self.root.after(0, self.zoom_log, msg)

        self.controller.progress_callback = zoom_log_redirect
        self.controller.loader.progress_callback = zoom_log_redirect
        self.controller.processor.progress_callback = zoom_log_redirect
        self.controller.generator.progress_callback = zoom_log_redirect

        try:
            result_path, stats = self.controller.generate_zoom_report(
                zoom_file_paths=zoom_paths,
                output_path=output_path,
                inscritos_zoom_path=self.zoom_inscritos_path
            )
            self.root.after(0, self._on_zoom_success, result_path, stats)

        except PRSAException as e:
            self.root.after(0, self._on_zoom_error, "Erro", str(e))
        except Exception as e:
            self.root.after(0, self._on_zoom_error, "Erro inesperado", str(e))
        finally:
            # Restaurar callbacks originais
            self.controller.progress_callback = original_callback
            self.controller.loader.progress_callback = original_callback
            self.controller.processor.progress_callback = original_callback
            self.controller.generator.progress_callback = original_callback

    def _on_zoom_success(self, result_path: str, stats: dict) -> None:
        """Callback de sucesso da aba Zoom."""
        self.zoom_progress_bar.stop()
        self.zoom_process_button.config(state='normal')

        duration = stats.get('duration_seconds', 0)
        records = stats.get('total_records', 0)
        size_mb = stats.get('output_size_mb', 0)

        self.zoom_log(f"Relatório Zoom gerado em {duration:.1f}s")
        self.zoom_log(f"Registros processados: {records:,}")
        self.zoom_log(f"Tamanho do arquivo: {size_mb:.2f} MB")

        messagebox.showinfo(
            "Relatório Zoom Gerado",
            f"Relatório Zoom gerado com sucesso!\n\n"
            f"Arquivo: {os.path.basename(result_path)}\n"
            f"Local: {result_path}"
        )
        self.clear_zoom()

    def _on_zoom_error(self, title: str, message: str) -> None:
        """Callback de erro da aba Zoom."""
        self.zoom_progress_bar.stop()
        self.zoom_process_button.config(state='normal')
        self.zoom_log(f"Erro: {message}")
        messagebox.showerror(title, message)

    # -------------------------------------------------------------------------
    # Enquetes dinâmicas (aba Evento)
    # -------------------------------------------------------------------------

    def _add_enquete_row(self) -> None:
        """Adiciona uma nova linha de enquete na interface."""
        idx = len(self.enquete_rows) + 1
        key = f'enquete_{idx}'

        row_frame = ttk.Frame(self.enquetes_container)
        row_frame.grid(row=idx - 1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=2)
        row_frame.columnconfigure(1, weight=1)

        ttk.Label(row_frame, text=f"Enquete {idx:02d}:").grid(row=0, column=0, sticky=tk.W, padx=5)

        entry = ttk.Entry(row_frame, width=50)
        entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

        ttk.Button(row_frame, text="Procurar",
                   command=lambda k=key, e=entry: self.load_file(k, e)).grid(row=0, column=2, padx=5)

        ttk.Button(row_frame, text="Preview",
                   command=lambda k=key: self.show_file_preview(k)).grid(row=0, column=3, padx=5)

        ttk.Button(row_frame, text="×",
                   command=lambda k=key, f=row_frame: self._remove_enquete_row(k, f)).grid(
            row=0, column=4, padx=2)

        self.enquete_rows.append((key, entry, row_frame))
        self.file_paths[key] = ''

        self.log(f"Enquete {idx:02d} adicionada. Selecione o arquivo CSV.")

    def _remove_enquete_row(self, key: str, row_frame: ttk.Frame) -> None:
        """Remove uma linha de enquete da interface e renumera as restantes."""
        self.file_paths.pop(key, None)
        self.enquete_rows = [(k, e, f) for k, e, f in self.enquete_rows if k != key]
        row_frame.destroy()

        old_rows = self.enquete_rows[:]
        self.enquete_rows = []
        for new_idx, (old_key, entry, frame) in enumerate(old_rows, start=1):
            new_key = f'enquete_{new_idx}'
            old_path = self.file_paths.pop(old_key, '')
            self.file_paths[new_key] = old_path
            self.enquete_rows.append((new_key, entry, frame))
            for widget in frame.winfo_children():
                if isinstance(widget, ttk.Label):
                    widget.config(text=f"Enquete {new_idx:02d}:")
                    break

        self.log(f"Enquete removida. Total: {len(self.enquete_rows)} enquete(s).")

    # -------------------------------------------------------------------------
    # Menu
    # -------------------------------------------------------------------------

    def create_menu(self) -> None:
        """Cria barra de menu com opções de histórico."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)

        self.recent_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Recentes", menu=self.recent_menu)
        self._update_recent_menu()

        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)

    def _update_recent_menu(self) -> None:
        """Atualiza menu de arquivos recentes."""
        self.recent_menu.delete(0, tk.END)
        recent_sets = self.file_history.get_recent(limit=5)

        if recent_sets:
            for i, item in enumerate(recent_sets):
                label = f"{item['name']}"
                timestamp = item['timestamp']
                self.recent_menu.add_command(
                    label=f"{i+1}. {label} ({timestamp})",
                    command=lambda item=item: self._load_recent_set(item)
                )
            self.recent_menu.add_separator()
            self.recent_menu.add_command(label="Limpar Histórico", command=self._clear_history)
        else:
            self.recent_menu.add_command(label="(Nenhum arquivo recente)", state='disabled')

    def _load_recent_set(self, item: dict) -> None:
        """Carrega conjunto de arquivos do histórico."""
        files = item['files']
        name = item['name']

        missing_files = []
        for file_type, path in files.items():
            if path and not os.path.exists(path):
                missing_files.append(f"{file_type}: {os.path.basename(path)}")

        if missing_files:
            messagebox.showerror(
                "Arquivos Não Encontrados",
                f"Alguns arquivos do conjunto '{name}' não existem mais:\n\n" +
                "\n".join(missing_files) + "\n\n" +
                "O conjunto será removido do histórico."
            )
            self.file_history._cleanup_invalid_sets()
            self._update_recent_menu()
            return

        self.file_paths = files.copy()

        if 'inscritos' in files:
            self.inscritos_entry.delete(0, tk.END)
            self.inscritos_entry.insert(0, files['inscritos'])

        if 'mensagens' in files:
            self.mensagens_entry.delete(0, tk.END)
            self.mensagens_entry.insert(0, files['mensagens'])

        if 'relatorio_acesso' in files:
            self.relatorio_entry.delete(0, tk.END)
            self.relatorio_entry.insert(0, files['relatorio_acesso'])

        if 'totalizado' in files:
            self.totalizado_entry.delete(0, tk.END)
            self.totalizado_entry.insert(0, files['totalizado'])

        if 'presenca_zoom' in files:
            self.zoom_entry.delete(0, tk.END)
            self.zoom_entry.insert(0, files['presenca_zoom'])

        for key, path in files.items():
            if key.startswith('enquete_') and path:
                self._add_enquete_row()
                if self.enquete_rows:
                    _, entry, _ = self.enquete_rows[-1]
                    entry.delete(0, tk.END)
                    entry.insert(0, path)
                    last_key = self.enquete_rows[-1][0]
                    self.file_paths[last_key] = path

        self.log(f"Conjunto '{name}' carregado do histórico")
        self.notebook.select(self.tab_evento)

    def _clear_history(self) -> None:
        """Limpa todo o histórico após confirmação."""
        result = messagebox.askyesno(
            "Limpar Histórico",
            "Tem certeza que deseja limpar todo o histórico de arquivos recentes?\n\n"
            "Esta ação não pode ser desfeita."
        )
        if result:
            self.file_history.clear()
            self._update_recent_menu()
            self.log("Histórico de arquivos limpo")

    # -------------------------------------------------------------------------
    # Log (aba Evento)
    # -------------------------------------------------------------------------

    def log(self, message: str) -> None:
        """Adicionar mensagem ao log com timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()

    # -------------------------------------------------------------------------
    # Carregar arquivo genérico (aba Evento)
    # -------------------------------------------------------------------------

    def load_file(self, file_type: str, entry_widget: ttk.Entry) -> None:
        """Abre diálogo para selecionar arquivo CSV."""
        file_path = filedialog.askopenfilename(
            title=f"Selecionar arquivo {file_type.replace('_', ' ').title()}",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.file_paths[file_type] = file_path
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, file_path)
            self.log(f"Arquivo {file_type} carregado: {os.path.basename(file_path)}")

    def clear_all(self) -> None:
        """Limpa todos os campos de entrada e cache de dados."""
        self.inscritos_entry.delete(0, tk.END)
        self.mensagens_entry.delete(0, tk.END)
        self.chat_entry.delete(0, tk.END)
        self.relatorio_entry.delete(0, tk.END)
        self.totalizado_entry.delete(0, tk.END)
        self.zoom_entry.delete(0, tk.END)
        self.inscritos_zoom_entry.delete(0, tk.END)

        for _, _, frame in self.enquete_rows:
            frame.destroy()
        self.enquete_rows = []

        self.file_paths = {
            'inscritos': '',
            'mensagens': '',
            'chat': '',
            'relatorio_acesso': '',
            'totalizado': '',
            'presenca_zoom': '',
            'inscritos_zoom': ''
        }
        self.controller.clear_cache()
        self.log("Todos os campos foram limpos.")

    def show_file_preview(self, file_type: str) -> None:
        """Mostra preview de arquivo CSV em janela modal."""
        file_path = self.file_paths.get(file_type, '')

        if not file_path:
            messagebox.showwarning(
                "Aviso",
                f"Nenhum arquivo {file_type.replace('_', ' ')} foi selecionado.\n"
                f"Use o botão 'Procurar' primeiro."
            )
            return

        if not os.path.exists(file_path):
            messagebox.showerror(
                "Erro",
                f"Arquivo não encontrado:\n{file_path}\n\n"
                f"O arquivo pode ter sido movido ou deletado."
            )
            return

        try:
            self.log(f"Carregando preview de {file_type}...")
            df = self.controller.loader.load_csv(file_path)
            title = file_type.replace('_', ' ').title()
            show_preview(self.root, df, title)
            self.log(f"Preview de {file_type} aberto: {len(df):,} linhas")
        except Exception as e:
            self.log(f"Erro ao carregar preview: {str(e)}")
            messagebox.showerror(
                "Erro ao Carregar Preview",
                f"Não foi possível carregar o arquivo:\n{str(e)}"
            )

    def validate_files(self) -> bool:
        """Valida se os arquivos obrigatórios foram selecionados."""
        optional_files = ['mensagens', 'chat', 'inscritos', 'presenca_zoom', 'inscritos_zoom']

        missing_files = []
        for file_type, path in self.file_paths.items():
            if file_type not in optional_files and not file_type.startswith('enquete_') and not path:
                missing_files.append(file_type.replace('_', ' ').title())

        if missing_files:
            messagebox.showerror("Erro", f"Faltam arquivos obrigatórios: {', '.join(missing_files)}")
            return False
        return True

    def process_and_generate(self) -> None:
        """Coordena o fluxo completo com threading para não bloquear a UI."""
        if not self.validate_files():
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile=f"Netpoint_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )

        if not output_path:
            self.log("Operação cancelada pelo usuário")
            return

        self.process_button.config(state='disabled')
        self.progress_bar.start(10)

        thread = threading.Thread(
            target=self._process_in_background,
            args=(output_path,),
            daemon=True
        )
        thread.start()

    def _process_in_background(self, output_path: str) -> None:
        """Executa processamento em background thread."""
        try:
            result_path, stats = self.controller.generate_report(
                file_paths=self.file_paths,
                output_path=output_path
            )
            self.root.after(0, self._on_success, result_path, stats)

        except PRSAException as e:
            self.root.after(0, self._on_error, "Erro", str(e))
        except Exception as e:
            self.root.after(0, self._on_error, "Erro inesperado", str(e))

    def _on_success(self, result_path: str, stats: dict) -> None:
        """Callback executado na thread principal quando processamento termina com sucesso."""
        self.progress_bar.stop()
        self.process_button.config(state='normal')

        try:
            name = self.file_history.generate_name(self.file_paths)
            self.file_history.add_set(name, self.file_paths)
            self._update_recent_menu()
            self.log(f"Conjunto salvo no histórico: {name}")
        except Exception as e:
            self.log(f"Erro ao salvar histórico: {str(e)}")

        StatsWindow(self.root, stats, result_path)
        self.clear_all()
        self.log("Campos limpos. Pronto para novo relatório.")

    def _on_error(self, title: str, message: str) -> None:
        """Callback executado na thread principal quando ocorre erro."""
        self.progress_bar.stop()
        self.process_button.config(state='normal')
        self.log(f"Erro: {message}")
        messagebox.showerror(title, message)


    # -------------------------------------------------------------------------
    # Auto-update
    # -------------------------------------------------------------------------

    def _check_for_updates(self) -> None:
        """Dispara verificação de atualização em background."""
        check_for_updates(
            current_version=settings.APP_VERSION,
            on_update_available=lambda v, url: self.root.after(
                0, self._on_update_available, v, url
            )
        )

    def _on_update_available(self, new_version: str, download_url: str) -> None:
        """Exibe diálogo de nova versão disponível."""
        answer = messagebox.askyesno(
            "Atualização Disponível",
            f"Uma nova versão está disponível!\n\n"
            f"Versão atual: {settings.APP_VERSION}\n"
            f"Nova versão:  {new_version}\n\n"
            f"Deseja atualizar agora?\n"
            f"O aplicativo será reiniciado automaticamente após a atualização.",
            icon='info'
        )
        if answer:
            self._start_update(download_url)

    def _start_update(self, download_url: str) -> None:
        """Abre janela de progresso e inicia o download da atualização."""
        win = tk.Toplevel(self.root)
        win.title("Atualizando...")
        win.geometry("380x120")
        win.resizable(False, False)
        win.grab_set()

        ttk.Label(win, text="Baixando atualização, aguarde...", font=('Arial', 10)).pack(pady=(18, 6))

        progress = ttk.Progressbar(win, length=320, mode='determinate', maximum=100)
        progress.pack(pady=4)

        status_var = tk.StringVar(value="Conectando...")
        ttk.Label(win, textvariable=status_var, font=('Arial', 8)).pack()

        def on_progress(pct: int) -> None:
            self.root.after(0, lambda: progress.configure(value=pct))
            self.root.after(0, lambda: status_var.set(f"{pct}% concluído"))

        def on_error(msg: str) -> None:
            win.destroy()
            messagebox.showerror(
                "Erro na Atualização",
                f"Não foi possível concluir a atualização:\n\n{msg}\n\n"
                f"Tente novamente mais tarde ou atualize manualmente."
            )

        download_and_apply(
            download_url=download_url,
            current_exe=get_current_exe(),
            on_progress=on_progress,
            on_error=on_error
        )


def main():
    root = tk.Tk()
    app = VideoConferenceReportGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
