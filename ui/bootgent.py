from google.genai import Client, types
from textual import work
from textual.app import App, ComposeResult
from textual.containers import VerticalGroup, VerticalScroll
from textual.widgets import Footer, Header, Input, Label, Static

from workers.send_prompt import send_prompt


class ChatMessage(Label):
    pass


class ChatHistory(VerticalScroll):
    def add_message(self, text: str, classes: str = "") -> None:
        self.mount(ChatMessage(text, classes=classes))
        self.scroll_end(animate=False)


class InputPrompt(Input):
    def __init__(self) -> None:
        super().__init__(placeholder="...")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        user_prompt = event.value.strip()
        if not user_prompt:
            return
        self.app.query_one(ChatHistory).add_message(f"You: {user_prompt}", classes="user")
        self.clear()
        self.focus()
        self.app.process_prompt(user_prompt)


class Bootgent(App):
    CSS_PATH = "styles.tcss"

    def __init__(self, messages: list[types.Content], client: Client):
        super().__init__()
        self.messages = messages
        self.client = client

    @work(exclusive=True)
    async def process_prompt(self, prompt: str) -> None:
        r = await send_prompt(prompt, self.messages, self.client)
        self.query_one(ChatHistory).add_message(f"Bot: {r}", classes="bot")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Static("One", classes="left-bar")
        yield VerticalGroup(ChatHistory(), InputPrompt(), classes="body")
