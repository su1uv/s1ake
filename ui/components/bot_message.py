from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Label, Static


class BotMessage(Horizontal):
    HEART_COLOR = "#CDB4DB"

    def __init__(self, text: str, classes: str = "") -> None:
        super().__init__(classes=classes)
        self.text = text

    @staticmethod
    def _heart() -> Text:
        return Text("♥", style=BotMessage.HEART_COLOR)

    def compose(self) -> ComposeResult:
        yield Static(self._heart(), classes="bot-icon")
        yield Label(self.text, classes="bot-content")
