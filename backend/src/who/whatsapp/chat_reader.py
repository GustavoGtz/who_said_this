from typing import Iterator, Sequence
from who.models import Message, Filter, HourMinuteTime, DayMonthYearDate

class WhatsappReader:
    def __init__(self, file: str):
        with open(file, encoding="utf-8") as f:
            self.chat = f.readlines()  # -> list[str]

        self.members: list[str] = []
        self.messages: dict = {}

        self.process_chat()

    def get_members(self) -> Sequence[str]:
        ...

    def get_messages_number(self, f: Filter) -> int:
        ...

    def get_messages(self, f: Filter) -> Iterator[Message]:
        ...

    def process_chat(self):
        """
        1. Remove trash messages.
        2. Merge multiline messages.
        3. Merge multi-messages.
        4. Apply several NLP techniques to improve the quality.
        """
        self.members = []
        self.messages = {}
