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
from config import settings


class VideoConferenceReportGenerator:
    """
    Interface gráfica para geração de relatórios de videoconferência.

    Classe focada apenas em UI, delegando lógica de negócio ao ReportController.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"{settings.APP_NAME} v{settings.APP_VERSION}")
        self.root.geometry("800x600")

        # Configurar ícone da aplicação
        self._set_app_icon()

        # Variáveis para armazenar caminhos dos arquivos
        # Nota: 'mensagens', 'chat' e 'enquete_N' são opcionais
        self.file_paths: Dict[str, str] = {
            'inscritos': '',
            'mensagens': '',
            'chat': '',
            'relatorio_acesso': '',
            'totalizado': '',
            'presenca_zoom': ''
        }

        # Lista de enquetes dinâmicas: cada item é (enquete_key, entry_widget, row_frame)
        self.enquete_rows = []

        # Controller (Dependency Injection)
        self.controller = ReportController(progress_callback=self.log)

        # Histórico de arquivos
        self.file_history = FileHistory()

        self.create_widgets()
        self.create_menu()

    def _set_app_icon(self) -> None:
        """Configura o ícone da aplicação."""
        try:
            # Tentar carregar ícone .ico (Windows)
            icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
            else:
                # Tentar carregar ícone .png (alternativa)
                icon_png = os.path.join(os.path.dirname(__file__), 'assets', 'icon.png')
                if os.path.exists(icon_png):
                    icon = tk.PhotoImage(file=icon_png)
                    self.root.iconphoto(True, icon)
        except Exception:
            # Silenciosamente ignorar erros de ícone
            pass
        
    def create_widgets(self):
        """Criar interface gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text=settings.APP_NAME,
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Seção de carregamento de arquivos
        files_frame = ttk.LabelFrame(main_frame, text="Carregar Arquivos CSV", padding="10")
        files_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        files_frame.columnconfigure(1, weight=1)
        
        # Inscritos (opcional)
        ttk.Label(files_frame, text="Arquivo Inscritos (opcional):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.inscritos_entry = ttk.Entry(files_frame, width=50)
        self.inscritos_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(files_frame, text="Procurar",
                  command=lambda: self.load_file('inscritos', self.inscritos_entry)).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(files_frame, text="Preview",
                  command=lambda: self.show_file_preview('inscritos')).grid(row=0, column=3, padx=5, pady=5)
        
        # Mensagens (opcional)
        ttk.Label(files_frame, text="Arquivo Mensagens (opcional):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.mensagens_entry = ttk.Entry(files_frame, width=50)
        self.mensagens_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(files_frame, text="Procurar",
                  command=lambda: self.load_file('mensagens', self.mensagens_entry)).grid(row=1, column=2, padx=5, pady=5)
        ttk.Button(files_frame, text="Preview",
                  command=lambda: self.show_file_preview('mensagens')).grid(row=1, column=3, padx=5, pady=5)

        # Chat (opcional)
        ttk.Label(files_frame, text="Arquivo Chat (opcional):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.chat_entry = ttk.Entry(files_frame, width=50)
        self.chat_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(files_frame, text="Procurar",
                  command=lambda: self.load_file('chat', self.chat_entry)).grid(row=2, column=2, padx=5, pady=5)
        ttk.Button(files_frame, text="Preview",
                  command=lambda: self.show_file_preview('chat')).grid(row=2, column=3, padx=5, pady=5)

        # Relatório de Acesso
        ttk.Label(files_frame, text="Relatório de Acesso:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.relatorio_entry = ttk.Entry(files_frame, width=50)
        self.relatorio_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(files_frame, text="Procurar",
                  command=lambda: self.load_file('relatorio_acesso', self.relatorio_entry)).grid(row=3, column=2, padx=5, pady=5)
        ttk.Button(files_frame, text="Preview",
                  command=lambda: self.show_file_preview('relatorio_acesso')).grid(row=3, column=3, padx=5, pady=5)

        # Totalizado
        ttk.Label(files_frame, text="Arquivo Totalizado:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.totalizado_entry = ttk.Entry(files_frame, width=50)
        self.totalizado_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(files_frame, text="Procurar",
                  command=lambda: self.load_file('totalizado', self.totalizado_entry)).grid(row=4, column=2, padx=5, pady=5)
        ttk.Button(files_frame, text="Preview",
                  command=lambda: self.show_file_preview('totalizado')).grid(row=4, column=3, padx=5, pady=5)

        # Presença no Zoom (opcional)
        ttk.Label(files_frame, text="Presença no Zoom (opcional):").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.zoom_entry = ttk.Entry(files_frame, width=50)
        self.zoom_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(files_frame, text="Procurar",
                  command=lambda: self.load_file('presenca_zoom', self.zoom_entry)).grid(row=5, column=2, padx=5, pady=5)
        ttk.Button(files_frame, text="Preview",
                  command=lambda: self.show_file_preview('presenca_zoom')).grid(row=5, column=3, padx=5, pady=5)

        # Separador e seção de Enquetes
        ttk.Separator(files_frame, orient='horizontal').grid(
            row=6, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=8
        )

        # Cabeçalho da seção de enquetes com botão "+"
        enquetes_header = ttk.Frame(files_frame)
        enquetes_header.grid(row=7, column=0, columnspan=4, sticky=(tk.W, tk.E), padx=5, pady=2)
        ttk.Label(enquetes_header, text="Enquetes (opcional):", font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
        ttk.Button(enquetes_header, text="+ Adicionar Enquete",
                   command=self._add_enquete_row).pack(side=tk.LEFT, padx=10)

        # Frame container para as linhas de enquete (crescimento dinâmico)
        self.enquetes_container = ttk.Frame(files_frame)
        self.enquetes_container.grid(row=8, column=0, columnspan=4, sticky=(tk.W, tk.E))
        self.enquetes_container.columnconfigure(1, weight=1)

        # Status/Log
        log_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        log_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Text widget para log
        self.log_text = tk.Text(log_frame, height=8, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Scrollbar para o log
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=scrollbar.set)

        # Barra de progresso
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=3, column=0, columnspan=3, pady=10)
        progress_frame.columnconfigure(0, weight=1)

        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            length=600
        )
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5)

        # Botões de ação
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=4, column=0, columnspan=3, pady=10)

        self.process_button = ttk.Button(
            action_frame,
            text="Processar e Gerar Relatório",
            command=self.process_and_generate,
            style='Accent.TButton'
        )
        self.process_button.pack(side=tk.LEFT, padx=5)

        ttk.Button(action_frame, text="Limpar",
                  command=self.clear_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Sair",
                  command=self.root.quit).pack(side=tk.LEFT, padx=5)

        # Mensagem inicial
        self.log("Sistema pronto. Carregue os arquivos CSV para começar.")

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
                   command=lambda k=key, f=row_frame: self._remove_enquete_row(k, f)).grid(row=0, column=4, padx=2)

        self.enquete_rows.append((key, entry, row_frame))
        self.file_paths[key] = ''

        self.log(f"Enquete {idx:02d} adicionada. Selecione o arquivo CSV.")

    def _remove_enquete_row(self, key: str, row_frame: ttk.Frame) -> None:
        """Remove uma linha de enquete da interface e renumera as restantes."""
        # Remover do dicionário de caminhos
        self.file_paths.pop(key, None)

        # Remover da lista de rows
        self.enquete_rows = [(k, e, f) for k, e, f in self.enquete_rows if k != key]

        # Destruir o frame
        row_frame.destroy()

        # Renumerar enquetes restantes (chaves e labels)
        old_rows = self.enquete_rows[:]
        self.enquete_rows = []
        for new_idx, (old_key, entry, frame) in enumerate(old_rows, start=1):
            new_key = f'enquete_{new_idx}'
            # Atualizar path no dicionário
            old_path = self.file_paths.pop(old_key, '')
            self.file_paths[new_key] = old_path
            self.enquete_rows.append((new_key, entry, frame))
            # Atualizar label dentro do frame
            for widget in frame.winfo_children():
                if isinstance(widget, ttk.Label):
                    widget.config(text=f"Enquete {new_idx:02d}:")
                    break

        self.log(f"Enquete removida. Total: {len(self.enquete_rows)} enquete(s).")

    def create_menu(self) -> None:
        """Cria barra de menu com opções de histórico."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)

        # Submenu Recentes
        self.recent_menu = tk.Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Recentes", menu=self.recent_menu)
        self._update_recent_menu()

        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)

    def _update_recent_menu(self) -> None:
        """Atualiza menu de arquivos recentes."""
        # Limpar menu atual
        self.recent_menu.delete(0, tk.END)

        # Obter conjuntos recentes
        recent_sets = self.file_history.get_recent(limit=5)

        if recent_sets:
            for i, item in enumerate(recent_sets):
                # Criar label com nome e timestamp
                label = f"{item['name']}"
                timestamp = item['timestamp']

                # Adicionar comando
                self.recent_menu.add_command(
                    label=f"{i+1}. {label} ({timestamp})",
                    command=lambda item=item: self._load_recent_set(item)
                )

            # Separador
            self.recent_menu.add_separator()
            self.recent_menu.add_command(
                label="Limpar Histórico",
                command=self._clear_history
            )
        else:
            # Sem histórico
            self.recent_menu.add_command(
                label="(Nenhum arquivo recente)",
                state='disabled'
            )

    def _load_recent_set(self, item: dict) -> None:
        """
        Carrega conjunto de arquivos do histórico.

        Args:
            item: Dicionário com informações do conjunto
        """
        files = item['files']
        name = item['name']

        # Verificar se todos os arquivos ainda existem
        missing_files = []
        for file_type, path in files.items():
            if not os.path.exists(path):
                missing_files.append(f"{file_type}: {os.path.basename(path)}")

        if missing_files:
            messagebox.showerror(
                "Arquivos Não Encontrados",
                f"Alguns arquivos do conjunto '{name}' não existem mais:\n\n" +
                "\n".join(missing_files) + "\n\n" +
                "O conjunto será removido do histórico."
            )
            # Limpar histórico de conjuntos inválidos
            self.file_history._cleanup_invalid_sets()
            self._update_recent_menu()
            return

        # Carregar arquivos nos campos
        self.file_paths = files.copy()

        # Atualizar campos de entrada
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

        # Restaurar enquetes do histórico
        for key, path in files.items():
            if key.startswith('enquete_') and path:
                self._add_enquete_row()
                if self.enquete_rows:
                    _, entry, _ = self.enquete_rows[-1]
                    entry.delete(0, tk.END)
                    entry.insert(0, path)
                    last_key = self.enquete_rows[-1][0]
                    self.file_paths[last_key] = path

        self.log(f"✓ Conjunto '{name}' carregado do histórico")

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

    def log(self, message: str) -> None:
        """
        Adicionar mensagem ao log com timestamp.

        Args:
            message: Mensagem a ser exibida no log
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def load_file(self, file_type: str, entry_widget: ttk.Entry) -> None:
        """
        Abre diálogo para selecionar arquivo CSV.

        Args:
            file_type: Tipo do arquivo ('inscritos', 'mensagens', etc)
            entry_widget: Campo de entrada onde exibir o caminho
        """
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

        # Remover todas as linhas de enquete da UI
        for _, _, frame in self.enquete_rows:
            frame.destroy()
        self.enquete_rows = []

        self.file_paths = {
            'inscritos': '',
            'mensagens': '',
            'chat': '',
            'relatorio_acesso': '',
            'totalizado': '',
            'presenca_zoom': ''
        }
        self.controller.clear_cache()
        self.log("Todos os campos foram limpos.")

    def show_file_preview(self, file_type: str) -> None:
        """
        Mostra preview de arquivo CSV em janela modal.

        Args:
            file_type: Tipo do arquivo ('inscritos', 'mensagens', etc)
        """
        # Verificar se arquivo foi selecionado
        file_path = self.file_paths.get(file_type, '')

        if not file_path:
            messagebox.showwarning(
                "Aviso",
                f"Nenhum arquivo {file_type.replace('_', ' ')} foi selecionado.\n"
                f"Use o botão 'Procurar' primeiro."
            )
            return

        # Verificar se arquivo existe
        if not os.path.exists(file_path):
            messagebox.showerror(
                "Erro",
                f"Arquivo não encontrado:\n{file_path}\n\n"
                f"O arquivo pode ter sido movido ou deletado."
            )
            return

        try:
            # Carregar CSV (usando o loader do controller para consistência)
            self.log(f"Carregando preview de {file_type}...")
            df = self.controller.loader.load_csv(file_path)

            # Mostrar janela de preview
            title = file_type.replace('_', ' ').title()
            show_preview(self.root, df, title)

            self.log(f"Preview de {file_type} aberto: {len(df):,} linhas")

        except Exception as e:
            self.log(f"Erro ao carregar preview: {str(e)}")
            messagebox.showerror(
                "Erro ao Carregar Preview",
                f"Não foi possível carregar o arquivo:\n{str(e)}\n\n"
                f"Verifique se o arquivo está no formato CSV correto."
            )
        
    def validate_files(self) -> bool:
        """
        Valida se os arquivos obrigatórios foram selecionados.

        Arquivos opcionais: mensagens, chat
        Arquivos obrigatórios: inscritos, relatorio_acesso, totalizado

        Returns:
            True se arquivos obrigatórios foram carregados, False caso contrário
        """
        # Arquivos opcionais não são validados
        optional_files = ['mensagens', 'chat', 'inscritos', 'presenca_zoom']

        missing_files = []
        for file_type, path in self.file_paths.items():
            if file_type not in optional_files and not path:
                missing_files.append(file_type.replace('_', ' ').title())

        if missing_files:
            messagebox.showerror("Erro", f"Faltam arquivos obrigatórios: {', '.join(missing_files)}")
            return False
        return True
        
    def process_and_generate(self) -> None:
        """
        Coordena o fluxo completo com threading para não bloquear a UI.

        Valida arquivos, solicita caminho de saída e inicia thread
        para processamento assíncrono.
        """
        # Validar arquivos selecionados
        if not self.validate_files():
            return

        # Solicitar caminho de saída ANTES de iniciar thread
        output_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile=f"Netpoint_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )

        if not output_path:
            self.log("Operação cancelada pelo usuário")
            return

        # Desabilitar botão durante processamento
        self.process_button.config(state='disabled')
        self.progress_bar.start(10)  # Inicia animação (10ms de intervalo)

        # Executar em thread separada para não travar UI
        thread = threading.Thread(
            target=self._process_in_background,
            args=(output_path,),
            daemon=True
        )
        thread.start()

    def _process_in_background(self, output_path: str) -> None:
        """
        Executa processamento em background thread.

        Args:
            output_path: Caminho onde salvar o arquivo Excel

        Note:
            Este método roda em thread separada. Usa root.after()
            para atualizar UI com segurança.
        """
        try:
            # Delegar ao controller (ele faz: load -> process -> generate)
            # Agora retorna tupla (result_path, stats)
            result_path, stats = self.controller.generate_report(
                file_paths=self.file_paths,
                output_path=output_path
            )

            # Sucesso - agendar atualização da UI na thread principal
            self.root.after(0, self._on_success, result_path, stats)

        except PRSAException as e:
            # Erros específicos do domínio
            self.root.after(0, self._on_error, "Erro", str(e))
        except Exception as e:
            # Erros inesperados
            self.root.after(0, self._on_error, "Erro inesperado", str(e))

    def _on_success(self, result_path: str, stats: dict) -> None:
        """
        Callback executado na thread principal quando processamento termina com sucesso.

        Args:
            result_path: Caminho do arquivo gerado
            stats: Dicionário com estatísticas do processamento
        """
        # Parar barra de progresso
        self.progress_bar.stop()

        # Reabilitar botão
        self.process_button.config(state='normal')

        # Adicionar ao histórico
        try:
            # Gerar nome automático baseado na pasta
            name = self.file_history.generate_name(self.file_paths)
            self.file_history.add_set(name, self.file_paths)
            self._update_recent_menu()
            self.log(f"✓ Conjunto salvo no histórico: {name}")
        except Exception as e:
            # Não bloquear por erro no histórico
            self.log(f"⚠ Erro ao salvar histórico: {str(e)}")

        # Mostrar janela de estatísticas customizada
        StatsWindow(self.root, stats, result_path)

        # Limpar campos para permitir novo relatório
        self.clear_all()
        self.log("Campos limpos. Pronto para novo relatório.")

    def _on_error(self, title: str, message: str) -> None:
        """
        Callback executado na thread principal quando ocorre erro.

        Args:
            title: Título da mensagem de erro
            message: Mensagem de erro detalhada
        """
        # Parar barra de progresso
        self.progress_bar.stop()

        # Reabilitar botão
        self.process_button.config(state='normal')

        # Logar erro
        self.log(f"Erro: {message}")

        # Mostrar mensagem de erro
        messagebox.showerror(title, message)


def main():
    root = tk.Tk()
    app = VideoConferenceReportGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
