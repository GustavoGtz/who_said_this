from typing import Protocol, Iterator, Sequence

from who.models import Message, Filter

class ChatReader(Protocol):
    
    def get_members(self) -> Sequence[str]:
        ...
    
    def get_messages_count(self, f : Filter) -> int:
        ...
    
    def get_messages(self, f : Filter) -> Iterator[Message]:
        ...
