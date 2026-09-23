#!/usr/bin/env python3
"""Tkinter GUI for the external-template project scaffolder."""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from project_scaffold import SUPPORTED_LANGUAGES, SUPPORTED_STRUCTURES, generate_project


class ScaffoldApp(ttk.Frame):
    """Small platform-neutral GUI that delegates generation to the CLI API."""

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=16)
        self.master = master
        self.destination = tk.StringVar()
        self.project_name = tk.StringVar()
        self.language = tk.StringVar(value="cpp")
        self.structure = tk.StringVar(value="minimal")
        self.force = tk.BooleanVar(value=False)
        self.status = tk.StringVar(value="Ready")
        self._build_form()

    def _build_form(self) -> None:
        self.columnconfigure(1, weight=1)
        fields = (
            ("Destination", self.destination),
            ("Project name", self.project_name),
        )
        for row, (label, variable) in enumerate(fields):
            ttk.Label(self, text=label).grid(row=row, column=0, sticky="w", padx=(0, 8), pady=6)
            ttk.Entry(self, textvariable=variable, width=48).grid(
                row=row, column=1, sticky="ew", pady=6
            )
        ttk.Button(self, text="Browse", command=self._browse).grid(row=0, column=2, padx=(8, 0))

        ttk.Label(self, text="Language").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=6)
        ttk.Combobox(self, textvariable=self.language, values=SUPPORTED_LANGUAGES, state="readonly").grid(
            row=2, column=1, sticky="ew", pady=6
        )
        ttk.Label(self, text="Structure").grid(row=3, column=0, sticky="w", padx=(0, 8), pady=6)
        ttk.Combobox(self, textvariable=self.structure, values=SUPPORTED_STRUCTURES, state="readonly").grid(
            row=3, column=1, sticky="ew", pady=6
        )
        ttk.Checkbutton(self, text="Overwrite existing files", variable=self.force).grid(
            row=4, column=1, sticky="w", pady=6
        )
        ttk.Button(self, text="Generate project", command=self._generate).grid(
            row=5, column=1, sticky="e", pady=(12, 6)
        )
        ttk.Label(self, textvariable=self.status).grid(row=6, column=0, columnspan=3, sticky="w", pady=6)

    def _browse(self) -> None:
        selected = filedialog.askdirectory(title="Choose project destination")
        if selected:
            self.destination.set(selected)

    def _generate(self) -> None:
        if not self.destination.get().strip() or not self.project_name.get().strip():
            messagebox.showerror("Missing information", "Destination and project name are required.")
            return
        try:
            created, skipped = generate_project(
                Path(self.destination.get()),
                self.project_name.get(),
                self.language.get(),
                self.force.get(),
                self.structure.get(),
            )
        except (OSError, RuntimeError, ValueError) as error:
            messagebox.showerror("Generation failed", str(error))
            self.status.set("Generation failed")
            return
        self.status.set(f"Created {len(created)} file(s); skipped {len(skipped)}.")
        messagebox.showinfo("Project generated", self.status.get())


def main() -> None:
    root = tk.Tk()
    root.title("Project Scaffolder")
    root.minsize(600, 300)
    ScaffoldApp(root).pack(fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()