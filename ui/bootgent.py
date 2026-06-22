from google.genai import Client, types
from textual import work
from textual.app import App, ComposeResult
from textual.containers import VerticalGroup, VerticalScroll
from textual.widgets import Footer, Header, Input, Label, Static

from workers.send_prompt import send_prompt


class ChatMessage(Label):
    pass


class TokenInfo(Static):
    def update_display(self, metadata: dict[str, int]) -> None:
        self.update(
            f"Input: {metadata['prompt_token_count']}\n"
            f"Output: {metadata['candidates_token_count']}"
        )


class ChatHistory(VerticalScroll):
    def add_message(self, text: str, classes: str = "") -> ChatMessage:
        msg = ChatMessage(text, classes=classes)
        self.mount(msg)
        self.scroll_end(animate=False)
        return msg


class InputPrompt(Input):
    def __init__(self) -> None:
        super().__init__(placeholder="...")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        user_prompt = event.value.strip()
        if not user_prompt:
            return
        self.app.query_one(ChatHistory).add_message(
            f"You: {user_prompt}", classes="user"
        )
        self.clear()
        self.focus()
        self.app.process_prompt(user_prompt)


class Bootgent(App):
    CSS_PATH = "styles.tcss"

    def __init__(
        self, messages: list[types.Content], client: Client, metadata: dict[str, int]
    ):
        super().__init__()
        self.messages = messages
        self.client = client
        self.metadata = metadata

    @work(exclusive=True)
    async def process_prompt(self, prompt: str) -> None:
        chat = self.query_one(ChatHistory)
        thinking = chat.add_message("Thinking...", classes="thinking")
        try:
            r = await send_prompt(prompt, self.messages, self.client, self.metadata)
            chat.add_message(f"Bot: {r}", classes="bot")
        finally:
            thinking.remove()
        self.query_one("#token-info", TokenInfo).update_display(self.metadata)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield TokenInfo(classes="left-bar", id="token-info")
        yield VerticalGroup(ChatHistory(), InputPrompt(), classes="body")
