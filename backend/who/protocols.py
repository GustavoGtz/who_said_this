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
        """
        Return a collection of message samples.
        Each sample contains `sample_size` messages, and there are `sample_count` samples.
        """
        ...

    def generate_question(self, options_number: int,) -> Sequence[Message, list[str]]:
        """
        Generate a question consisting of:
        - A reference message (the question)
        - A list of possible answer options (one of them being the correct one)
        """
        ...

    def set_messages(self, new_messages: Sequence[Message]) -> None:
        """
        Replace the current messages with a new sequence of messages.
        """
        ...
    
