"""Janela de edição dos insights gerados pela IA antes de finalizar o relatório."""

import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional


class InsightsEditorWindow:
    """
    Abre uma janela modal com os insights gerados pelo Claude para revisão e edição.
    Ao confirmar, chama on_confirm(insights) com a lista editada.
    Ao cancelar, chama on_cancel().
    """

    def __init__(
        self,
        parent: tk.Tk,
        insights: List[Dict],
        on_confirm,
        on_cancel=None,
    ):
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        self._entries: List[Dict[str, tk.Widget]] = []

        self.win = tk.Toplevel(parent)
        self.win.title("Revisar Insights — Relatório Inteligente")
        self.win.geometry("680x680")
        self.win.resizable(True, True)
        self.win.grab_set()
        self.win.protocol("WM_DELETE_WINDOW", self._cancel)

        self._build(insights)
        self.win.update_idletasks()
        self.win.minsize(560, 500)

    def _build(self, insights: List[Dict]) -> None:
        # ── Cabeçalho ──
        header = tk.Frame(self.win, bg="#3db3f5", pady=12)
        header.pack(fill=tk.X)
        tk.Label(
            header, text="Revisar Insights gerados pela IA",
            bg="#3db3f5", fg="white",
            font=("Segoe UI", 13, "bold")
        ).pack(side=tk.LEFT, padx=16)
        tk.Label(
            header, text="Edite antes de finalizar o relatório",
            bg="#3db3f5", fg="white",
            font=("Segoe UI", 9)
        ).pack(side=tk.LEFT)

        # ── Área rolável ──
        outer = tk.Frame(self.win)
        outer.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        canvas = tk.Canvas(outer, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        self._scroll_frame = tk.Frame(canvas, padx=14, pady=8)

        self._scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self._scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scroll com roda do mouse
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        # ── Cards editáveis ──
        for i, ins in enumerate(insights):
            self._build_card(i, ins)

        # ── Botões ──
        btn_frame = tk.Frame(self.win, pady=10, padx=14)
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM)

        ttk.Button(
            btn_frame,
            text="Confirmar e gerar relatório",
            command=self._confirm,
            style="Accent.TButton"
        ).pack(side=tk.RIGHT, padx=(6, 0))

        ttk.Button(
            btn_frame,
            text="Cancelar",
            command=self._cancel
        ).pack(side=tk.RIGHT)

        ttk.Separator(self.win, orient="horizontal").pack(fill=tk.X, side=tk.BOTTOM)

    def _build_card(self, index: int, ins: Dict) -> None:
        frame = tk.LabelFrame(
            self._scroll_frame,
            text=f"  Insight {index + 1}  ",
            font=("Segoe UI", 9, "bold"),
            fg="#3d3d6e",
            padx=10, pady=8,
            relief=tk.GROOVE
        )
        frame.pack(fill=tk.X, pady=6)

        # Linha: ícone + título
        row_top = tk.Frame(frame)
        row_top.pack(fill=tk.X, pady=(0, 6))

        tk.Label(row_top, text="Ícone:", font=("Segoe UI", 9), width=6, anchor="w").pack(side=tk.LEFT)
        icon_var = tk.StringVar(value=ins.get("icon", "💡"))
        icon_entry = ttk.Entry(row_top, textvariable=icon_var, width=5, font=("Segoe UI", 12))
        icon_entry.pack(side=tk.LEFT, padx=(0, 16))

        tk.Label(row_top, text="Título:", font=("Segoe UI", 9), anchor="w").pack(side=tk.LEFT)
        title_var = tk.StringVar(value=ins.get("title", ""))
        title_entry = ttk.Entry(row_top, textvariable=title_var, width=38, font=("Segoe UI", 9))
        title_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Texto do insight
        tk.Label(frame, text="Texto:", font=("Segoe UI", 9), anchor="w").pack(anchor="w")
        body_text = tk.Text(frame, height=3, wrap=tk.WORD, font=("Segoe UI", 9),
                            relief=tk.FLAT, bg="#f5f5fb", bd=1,
                            highlightbackground="#c0c0d0", highlightthickness=1)
        body_text.insert("1.0", ins.get("body", ""))
        body_text.pack(fill=tk.X, expand=True, pady=(2, 0))

        self._entries.append({
            "icon": icon_var,
            "title": title_var,
            "body": body_text,
        })

    def _confirm(self) -> None:
        insights = []
        for entry in self._entries:
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
