from __future__ import annotations

import subprocess
import threading
from dataclasses import dataclass
from typing import Callable

from .state import OperationResult


def ps_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


@dataclass
class CommandStep:
    label: str
    command: str


class PowerShellRunner:
    def __init__(self, on_complete: Callable[[OperationResult], None]) -> None:
        self._on_complete = on_complete

    def run_async(self, title: str, steps: list[CommandStep]) -> None:
        worker = threading.Thread(target=self._run_steps, args=(title, steps), daemon=True)
        worker.start()

    def _run_steps(self, title: str, steps: list[CommandStep]) -> None:
        stdout_chunks: list[str] = []
        stderr_chunks: list[str] = []
        returncode = 0

        for step in steps:
            completed = subprocess.run(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-NonInteractive",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-Command",
                    step.command,
                ],
                capture_output=True,
                text=True,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            if completed.stdout:
                stdout_chunks.append(f"[{step.label}]\n{completed.stdout.strip()}\n")
            if completed.stderr:
                stderr_chunks.append(f"[{step.label}]\n{completed.stderr.strip()}\n")
            if completed.returncode != 0:
                returncode = completed.returncode
                break

        result = OperationResult(
            title=title,
            stdout="\n".join(chunk for chunk in stdout_chunks if chunk).strip(),
            stderr="\n".join(chunk for chunk in stderr_chunks if chunk).strip(),
            returncode=returncode,
        )
        self._on_complete(result)
