from textual.widgets import Input

from ui.components.chat_history import ChatHistory


class InputPrompt(Input):
    def __init__(self) -> None:
        super().__init__(placeholder="...")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        user_prompt = event.value.strip()
        if not user_prompt:
            return
        self.app.query_one(ChatHistory).add_message(user_prompt, classes="user")
        self.clear()
        self.focus()
        self.app.process_prompt(user_prompt)
