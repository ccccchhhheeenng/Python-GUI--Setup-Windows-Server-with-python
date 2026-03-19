from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class OperationResult:
    title: str
    stdout: str = ""
    stderr: str = ""
    returncode: int = 0


@dataclass
class AppState:
    route: list[str] = field(default_factory=list)
    busy: bool = False
    issues: list[str] = field(default_factory=list)
    last_result: OperationResult | None = None

    def push(self, segment: str) -> None:
        self.route.append(segment)

    def pop(self) -> None:
        if self.route:
            self.route.pop()

    def breadcrumb(self) -> str:
        if not self.route:
            return "Main Window"
        return "Main Window > " + " > ".join(self.route)

    def set_issues(self, *messages: str) -> None:
        self.issues = [message for message in messages if message]

    def clear_issues(self) -> None:
        self.issues.clear()
