from textual.app import App, ComposeResult, RenderResult
from textual.widgets import Input, Static, TextArea
from textual.containers import VerticalGroup, VerticalScroll


class InsertPrompt(Input):
    pass


class Prompt(TextArea):
    pass
    

class PromptHistory(VerticalGroup):
    
    def compose(self) -> ComposeResult:
        yield VerticalScroll(Prompt("Prompt 1"), Prompt("Prompt 2"))
        yield InsertPrompt()
    

class Bootgent(App):
    CSS_PATH = "styles.tcss"

    def compose(self) -> ComposeResult:
        yield Static("One", classes="left-bar")
        yield VerticalGroup(PromptHistory(), classes="body")


if __name__ == "__main__":
    app = Bootgent()
    app.run()



