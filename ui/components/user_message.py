from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Label


class UserMessage(Horizontal):
    def __init__(self, text: str, classes: str = "") -> None:
        super().__init__(classes=classes)
        self.text = text

    def compose(self) -> ComposeResult:
        yield Label(self.text, classes="user-content")
