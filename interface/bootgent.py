from textual.app import App, ComposeResult
from textual.containers import VerticalGroup, VerticalScroll
from textual.widgets import Input, Label, Static


class InputPrompt(Input):
    pass


class Prompt(Label):
    pass


class PromptHistory(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield VerticalGroup(
            Prompt("Prompt 1"), Prompt("Prompt 2"), classes="prompt-history"
        )


class Bootgent(App):
    CSS_PATH = "styles.tcss"

    def compose(self) -> ComposeResult:
        yield Static("One", classes="left-bar")
        yield VerticalGroup(PromptHistory(), InputPrompt(), classes="body")


if __name__ == "__main__":
    app = Bootgent()
    app.run()
