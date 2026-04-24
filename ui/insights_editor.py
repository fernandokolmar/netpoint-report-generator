"""Janela de edição dos insights gerados pela IA antes de finalizar o relatório."""

import threading
import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, List, Optional


class InsightsEditorWindow:
    """
    Abre uma janela modal com os insights gerados pelo Claude para revisão e edição.
    Cada card tem campo de instrução + botão "Regerar" para regenerar só aquele insight.
    Ao confirmar, chama on_confirm(insights) com a lista editada.
    """

    def __init__(
        self,
        parent: tk.Tk,
        insights: List[Dict],
        metrics: Dict[str, Any],
        api_key: str,
        on_confirm,
        on_cancel=None,
    ):
        self.parent = parent
        self.metrics = metrics
        self.api_key = api_key
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        self._entries: List[Dict[str, tk.Widget]] = []

        self.win = tk.Toplevel(parent)
        self.win.title("Revisar Insights — Relatório Inteligente")
        self.win.geometry("760x720")
        self.win.resizable(True, True)
        self.win.grab_set()
        self.win.protocol("WM_DELETE_WINDOW", self._cancel)

        self._build(insights)
        self.win.update_idletasks()
        self.win.minsize(600, 520)

    # ─────────────────────────────────────────────
    # Construção da janela
    # ─────────────────────────────────────────────

    def _build(self, insights: List[Dict]) -> None:
        # Cabeçalho
        header = tk.Frame(self.win, bg="#3db3f5", pady=12)
        header.pack(fill=tk.X)
        tk.Label(
            header, text="Revisar Insights gerados pela IA",
            bg="#3db3f5", fg="white", font=("Segoe UI", 13, "bold")
        ).pack(side=tk.LEFT, padx=16)
        tk.Label(
            header, text="Edite ou regenere cada card antes de finalizar",
            bg="#3db3f5", fg="white", font=("Segoe UI", 9)
        ).pack(side=tk.LEFT)

        # Área rolável
        outer = tk.Frame(self.win)
        outer.pack(fill=tk.BOTH, expand=True)

        self._canvas = tk.Canvas(outer, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=self._canvas.yview)
        self._scroll_frame = tk.Frame(self._canvas, padx=14, pady=8)

        self._scroll_frame.bind(
            "<Configure>",
            lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all"))
        )
        self._canvas.create_window((0, 0), window=self._scroll_frame, anchor="nw")
        self._canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._canvas.bind_all(
            "<MouseWheel>",
            lambda e: self._canvas.yview_scroll(-1 * (e.delta // 120), "units")
        )

        # Cards
        for i, ins in enumerate(insights):
            self._build_card(i, ins)

        # Botões inferiores
        ttk.Separator(self.win, orient="horizontal").pack(fill=tk.X, side=tk.BOTTOM)
        btn_frame = tk.Frame(self.win, pady=10, padx=14)
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM)

        ttk.Button(
            btn_frame, text="Confirmar e gerar relatório",
            command=self._confirm, style="Accent.TButton"
        ).pack(side=tk.RIGHT, padx=(6, 0))

        ttk.Button(
            btn_frame, text="Cancelar", command=self._cancel
        ).pack(side=tk.RIGHT)

    def _build_card(self, index: int, ins: Dict) -> None:
        frame = tk.LabelFrame(
            self._scroll_frame,
            text=f"  Insight {index + 1}  ",
            font=("Segoe UI", 9, "bold"),
            fg="#3d3d6e", padx=10, pady=8, relief=tk.GROOVE
        )
        frame.pack(fill=tk.X, pady=6)

        # Linha: ícone + título
        row_top = tk.Frame(frame)
        row_top.pack(fill=tk.X, pady=(0, 6))

        tk.Label(row_top, text="Ícone:", font=("Segoe UI", 9), width=6, anchor="w").pack(side=tk.LEFT)
        icon_var = tk.StringVar(value=ins.get("icon", "💡"))
        ttk.Entry(row_top, textvariable=icon_var, width=5, font=("Segoe UI", 12)).pack(side=tk.LEFT, padx=(0, 12))

        tk.Label(row_top, text="Título:", font=("Segoe UI", 9), anchor="w").pack(side=tk.LEFT)
        title_var = tk.StringVar(value=ins.get("title", ""))
        ttk.Entry(row_top, textvariable=title_var, font=("Segoe UI", 9)).pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Texto do insight
        tk.Label(frame, text="Texto:", font=("Segoe UI", 9), anchor="w").pack(anchor="w")
        body_text = tk.Text(
            frame, height=3, wrap=tk.WORD, font=("Segoe UI", 9),
            relief=tk.FLAT, bg="#f5f5fb", bd=1,
            highlightbackground="#c0c0d0", highlightthickness=1
        )
        body_text.insert("1.0", ins.get("body", ""))
        body_text.pack(fill=tk.X, expand=True, pady=(2, 8))

        # Separador visual
        ttk.Separator(frame, orient="horizontal").pack(fill=tk.X, pady=(0, 8))

        # Linha de regeneração
        regen_frame = tk.Frame(frame, bg="#f0f4ff", bd=0)
        regen_frame.pack(fill=tk.X)

        tk.Label(
            regen_frame, text="Orientação:", font=("Segoe UI", 8),
            fg="#555", bg="#f0f4ff", anchor="w"
        ).pack(side=tk.LEFT, padx=(0, 6))

        instrucao_var = tk.StringVar()
        instrucao_entry = ttk.Entry(
            regen_frame, textvariable=instrucao_var,
            font=("Segoe UI", 9), width=38
        )
        instrucao_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        instrucao_entry.insert(0, "Ex: este dado está errado, foque em...")

        # Placeholder: limpa ao focar, restaura se vazio
        def _clear_placeholder(e, var=instrucao_var):
            if var.get() == instrucao_entry.cget("foreground") or True:
                if var.get().startswith("Ex:"):
                    instrucao_entry.delete(0, tk.END)
                    instrucao_entry.config(foreground="black")

        def _restore_placeholder(e, var=instrucao_var, entry=instrucao_entry):
            if not var.get().strip():
                entry.delete(0, tk.END)
                entry.insert(0, "Ex: este dado está errado, foque em...")
                entry.config(foreground="#aaa")

        instrucao_entry.config(foreground="#aaa")
        instrucao_entry.bind("<FocusIn>", _clear_placeholder)
        instrucao_entry.bind("<FocusOut>", _restore_placeholder)

        # Status label (mostra "Gerando..." ou resultado)
        status_var = tk.StringVar(value="")
        status_label = tk.Label(
            frame, textvariable=status_var,
            font=("Segoe UI", 8, "italic"), fg="#777", anchor="w"
        )
        status_label.pack(anchor="w", pady=(4, 0))

        # Botão Regerar
        regen_btn = ttk.Button(
            regen_frame,
            text="↺ Regerar",
            command=lambda i=index, iv=instrucao_var, ie=instrucao_entry,
                           sv=status_var, icon=icon_var, title=title_var, body=body_text: (
                self._regerar_card(i, iv, ie, sv, icon, title, body)
            )
        )
        regen_btn.pack(side=tk.LEFT, padx=(0, 6))

        # Botão Remover
        remove_btn = ttk.Button(
            regen_frame,
            text="✕ Remover",
            command=lambda i=index, f=frame: self._remover_card(i, f)
        )
        remove_btn.pack(side=tk.LEFT)

        entry = {
            "icon": icon_var,
            "title": title_var,
            "body": body_text,
            "regen_btn": regen_btn,
            "status_var": status_var,
            "removed": False,
            "frame": frame,
        }
        self._entries.append(entry)

    # ─────────────────────────────────────────────
    # Regeneração de card individual
    # ─────────────────────────────────────────────

    def _regerar_card(
        self,
        index: int,
        instrucao_var: tk.StringVar,
        instrucao_entry: ttk.Entry,
        status_var: tk.StringVar,
        icon_var: tk.StringVar,
        title_var: tk.StringVar,
        body_text: tk.Text,
    ) -> None:
        instrucao = instrucao_var.get().strip()
        if not instrucao or instrucao.startswith("Ex:"):
            instrucao = "Gere um insight diferente e relevante sobre o evento."

        entry = self._entries[index]
        entry["regen_btn"].config(state="disabled", text="Gerando...")
        status_var.set("Consultando Claude...")

        insight_atual = {
            "icon": icon_var.get().strip(),
            "title": title_var.get().strip(),
            "body": body_text.get("1.0", tk.END).strip(),
        }

        def _run():
            try:
                from core.ai_insights import regerar_insight
                novo = regerar_insight(
                    metrics=self.metrics,
                    api_key=self.api_key,
                    insight_atual=insight_atual,
                    instrucao=instrucao,
                )
                self.win.after(0, lambda: self._apply_regen(index, novo, status_var))
            except Exception as e:
                self.win.after(0, lambda: self._regen_error(index, str(e), status_var))

        threading.Thread(target=_run, daemon=True).start()

    def _remover_card(self, index: int, frame: tk.LabelFrame) -> None:
        self._entries[index]["removed"] = True
        frame.destroy()
        # Renumera os títulos dos cards restantes
        pos = 1
        for entry in self._entries:
            if not entry.get("removed") and entry["frame"].winfo_exists():
                entry["frame"].config(text=f"  Insight {pos}  ")
                pos += 1

    def _apply_regen(self, index: int, novo: Dict, status_var: tk.StringVar) -> None:
        entry = self._entries[index]
        entry["icon"].set(novo.get("icon", "💡"))
        entry["title"].set(novo.get("title", ""))
        entry["body"].delete("1.0", tk.END)
        entry["body"].insert("1.0", novo.get("body", ""))
        entry["regen_btn"].config(state="normal", text="↺ Regerar")
        status_var.set("✓ Insight atualizado — revise e edite se necessário.")

    def _regen_error(self, index: int, error: str, status_var: tk.StringVar) -> None:
        entry = self._entries[index]
        entry["regen_btn"].config(state="normal", text="↺ Regerar")
        status_var.set(f"Erro: {error[:80]}")

    # ─────────────────────────────────────────────
    # Confirmar / Cancelar
    # ─────────────────────────────────────────────

    def _confirm(self) -> None:
        insights = []
        for entry in self._entries:
            if entry.get("removed"):
                continue
            insights.append({
                "icon": entry["icon"].get().strip(),
                "title": entry["title"].get().strip(),
                "body": entry["body"].get("1.0", tk.END).strip(),
            })
        self.win.grab_release()
        self.win.destroy()
        self.on_confirm(insights)

    def _cancel(self) -> None:
        self.win.grab_release()
        self.win.destroy()
        if self.on_cancel:
            self.on_cancel()
