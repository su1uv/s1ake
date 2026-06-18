from textual.app import App, ComposeResult
from textual.containers import VerticalGroup, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Footer, Header, Input, Label, Static


class Bootgent(App):
    messages_list: reactive[list[str]] = reactive(list, recompose=True)
    CSS_PATH = "styles.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Static("One", classes="left-bar")
        yield VerticalGroup(ChatHistory(), InputPrompt(), classes="body")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        user_prompt = event.value.strip()
        if not user_prompt:
            return
        self.messages_list.append(user_prompt)
        self.mutate_reactive(Bootgent.messages_list)
        event.input.clear()


class Message(Label):
    pass


class ChatHistory(VerticalScroll):
    def on_mount(self) -> None:
        self.classes = "chat-hist"
        self.id = "chatHist"

        assert isinstance(self.app, Bootgent)
        for m in self.app.messages_list:
            self.mount(Message(m))


class InputPrompt(Input):
    def on_mount(self) -> None:
        self.classes = "input-prompt"
        self.placeholder = "How can I help you?"


if __name__ == "__main__":
    app = Bootgent()
    app.run()
