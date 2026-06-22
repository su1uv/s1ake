from textual.containers import VerticalScroll
from textual.widget import Widget

from ui.components.bot_message import BotMessage
from ui.components.chat_message import ChatMessage
from ui.components.user_message import UserMessage


class ChatHistory(VerticalScroll):
    def add_message(self, text: str, classes: str = "") -> Widget:
        if classes == "user":
            msg: Widget = UserMessage(text, classes=classes)
        elif classes == "bot":
            msg = BotMessage(text, classes=classes)
        else:
            msg = ChatMessage(text, classes=classes)
        self.mount(msg)
        self.scroll_end(animate=False)
        return msg
