from google.genai import Client, types
from textual import work
from textual.app import App, ComposeResult
from textual.containers import VerticalGroup
from textual.widgets import Footer, Header

from ui.components.chat_history import ChatHistory
from ui.components.input_prompt import InputPrompt
from ui.components.token_info import TokenInfo
from workers.send_prompt import send_prompt


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
            chat.add_message(r, classes="bot")
        finally:
            thinking.remove()
        self.query_one("#token-info", TokenInfo).update_display(self.metadata)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield TokenInfo(classes="left-bar", id="token-info")
        yield VerticalGroup(ChatHistory(), InputPrompt(), classes="body")
