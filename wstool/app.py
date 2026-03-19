from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

from .powershell import CommandStep, PowerShellRunner
from .state import AppState, OperationResult
from .views import dhcp, dns, iscsi, main_menu


class WindowsServerToolApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Windows Server Tool")
        self.root.minsize(420, 220)

        self.style = ttk.Style()
        self.style.configure("Custom.TButton", padding=6)
        self.style.configure("Red.TButton", padding=6)
        self.style.configure("Green.TButton", padding=6)

        self.state = AppState()
        self.runner = PowerShellRunner(self._finish_background_operation)
        self.dynamic_labels: list[tk.Widget] = []

        self.content = ttk.Frame(self.root, padding=12)
        self.content.pack(fill=tk.BOTH, expand=True)

        self.footer = ttk.Frame(self.root, padding=(12, 0, 12, 12))
        self.footer.pack(fill=tk.X)
        self.issue_label = ttk.Label(self.footer, text="0 problem found", anchor=tk.W)
        self.issue_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.busy_label = ttk.Label(self.footer, text="Button Lock=False", anchor=tk.E)
        self.busy_label.pack(side=tk.RIGHT)

        self.render()

    def run(self) -> None:
        self.root.mainloop()

    def set_window_size(self, width: int, height: int) -> None:
        self.root.geometry(f"{width}x{height}")

    def clear_content(self) -> None:
        self.dynamic_labels = []
        for widget in self.content.winfo_children():
            widget.destroy()
        self.content.grid_columnconfigure(0, weight=0)
        self.content.grid_columnconfigure(1, weight=1)
        self.content.grid_columnconfigure(2, weight=0)

    def render(self) -> None:
        self.clear_content()
        route = self.state.route
        if not route:
            main_menu.build(self)
        elif route[0] == "DHCP":
            dhcp.build_setup(self)
        elif route[0] == "RemoveDHCP":
            dhcp.build_remove_scope(self)
        elif route[0] == "DNS":
            dns.build(self)
        elif route[0] == "iSCSI":
            iscsi.build(self)
        else:
            self.state.set_issues("Unknown route.")
        self.refresh_status()

    def render_header(self) -> None:
        ttk.Label(self.content, text=self.state.breadcrumb(), anchor=tk.CENTER).grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 8))

    def refresh_status(self) -> None:
        issue_count = len(self.state.issues)
        if issue_count:
            self.issue_label.config(text=" | ".join(self.state.issues))
        else:
            self.issue_label.config(text="0 problem found")
        self.busy_label.config(text=f"Button Lock={'True' if self.state.busy else 'False'}")

    def navigate(self, segment: str) -> None:
        self.state.push(segment)
        self.state.clear_issues()
        self.render()

    def back(self) -> None:
        if self.state.busy:
            return
        self.state.pop()
        self.state.clear_issues()
        self.render()

    def add_back_button(self):
        return ttk.Button(self.content, text="Back", command=self.guard(self.back), style="Red.TButton")

    def add_labeled_entry(self, label: str, row: int, width: int = 28, show: str | None = None) -> tk.Entry:
        lbl = ttk.Label(self.content, text=label)
        lbl.grid(row=row, column=0, sticky="w", pady=6)
        entry = ttk.Entry(self.content, width=width, show=show or "")
        entry.grid(row=row, column=1, sticky="ew", pady=6)
        self.dynamic_labels.append(lbl)
        return entry

    def add_combobox(self, label: str, values: tuple[str, ...], row: int) -> ttk.Combobox:
        lbl = ttk.Label(self.content, text=label)
        lbl.grid(row=row, column=0, sticky="w", pady=6)
        combo = ttk.Combobox(self.content, values=values, state="readonly")
        combo.grid(row=row, column=1, sticky="ew", pady=6)
        self.dynamic_labels.append(lbl)
        return combo

    def add_form_actions(self, row: int, submit_text: str, submit) -> None:
        self.add_back_button().grid(row=row, column=0, sticky="ew", pady=(10, 0))
        ttk.Button(self.content, text=submit_text, command=self.guard(submit), style="Green.TButton").grid(row=row, column=1, sticky="ew", pady=(10, 0))

    def guard(self, callback):
        def wrapped():
            if self.state.busy:
                return
            self.state.clear_issues()
            try:
                callback()
            except ValueError as error:
                self.state.set_issues(str(error))
                self.refresh_status()
            except Exception as error:  # pragma: no cover - defensive UI fallback
                self.state.set_issues(f"Unexpected error: {error}")
                self.refresh_status()
                messagebox.showerror("Windows Server Tool", str(error))

        return wrapped

    def run_steps(self, title: str, steps: list[CommandStep]) -> None:
        if not steps:
            return
        self.state.busy = True
        self.state.clear_issues()
        self.refresh_status()
        self.runner.run_async(title, steps)

    def _finish_background_operation(self, result: OperationResult) -> None:
        self.root.after(0, lambda: self._handle_result(result))

    def _handle_result(self, result: OperationResult) -> None:
        self.state.busy = False
        self.state.last_result = result
        if result.returncode != 0:
            self.state.set_issues("Operation failed. Review the result window for details.")
        else:
            self.state.clear_issues()
        self.refresh_status()
        self.show_result_window(result)

    def show_result_window(self, result: OperationResult) -> None:
        top = tk.Toplevel(self.root)
        top.title(result.title)
        top.geometry("900x500")

        ttk.Label(top, text=result.title, anchor=tk.CENTER).pack(fill=tk.X, padx=12, pady=(12, 8))

        output = scrolledtext.ScrolledText(top, wrap=tk.WORD, height=18)
        output.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        stdout = result.stdout or "No Output"
        stderr = result.stderr or "No Error"
        status = "Success" if result.returncode == 0 else f"Failed (exit code {result.returncode})"
        output.insert("end", f"Status:\n{status}\n\nOutput:\n{stdout}\n\nError:\n{stderr}")
        output.configure(state="disabled")

        ttk.Button(top, text="Close", command=top.destroy, style="Red.TButton").pack(pady=(0, 12))
