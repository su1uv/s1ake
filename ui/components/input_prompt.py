from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Input

from ui.components.chat_history import ChatHistory


class InputPrompt(Horizontal):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="...", classes="input-field")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        user_prompt = event.value.strip()
        if not user_prompt:
            return
        self.app.query_one(ChatHistory).add_message(user_prompt, classes="user")
        self.query_one(Input).clear()
        self.query_one(Input).focus()
        self.app.process_prompt(user_prompt)
