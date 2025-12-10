from typing import Protocol, Iterator, Sequence

from who.models import Message, Filter

class ChatReader(Protocol):
    
    def get_members(self) -> Sequence[str]:
        ...
    
    def get_messages_number(self, f : Filter) -> int:
        ...
    
    def get_messages(self, f : Filter) -> Iterator[Message]:
        ...
        
class MessagesManager(Protocol):

    def get_samples(self,sample_size: int, sample_count: int) -> Sequence[Sequence[Message]]:
        ...

    def generate_question(self, options_number: int,) -> Sequence[Message, list[str]]:
        ...

    def set_messages(self, new_messages: Sequence[Message]) -> None:
        ...
    
