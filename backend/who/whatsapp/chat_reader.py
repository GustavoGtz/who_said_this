import re
import string
from typing import Iterator, Sequence
from who.models import Message, Filter, HourMinuteTime, DayMonthYearDate

class WhatsappReader:
    def __init__(self, file: str):
        with open(file, encoding="utf-8") as f:
            self.chat = f.readlines()  # -> list[str]
        
        self.members: list[str] = []
        self.messages: list[Message] = []
        self.process_chat()

    def get_members(self) -> Sequence[str]:
        # TODO: Devolver la lista que contiene los nombres
        #       de los miembros del Chat.
        ...

    def get_messages_number(self, f: Filter) -> int:
        # TODO: Calcular el numero de mensajes en self.messages despues
        #       de aplicar los filtros f y devolver el entero.
        ...

    def get_messages(self, f: Filter) -> Iterator[Message]:
        # TODO: Devolver una Iterador de objetos tipo Message despues
        #       de aplicar los filtros f.
        #       Importante:
        #       1) NO MUTAR la lista original self.message, unicamente
        #          devolver una "copia".
        #       2) El valor de retorno debe ser un Iterator con elementos
        #          de tipo Message.
        ...
    
    def create_messages_data(self):
        msg_patterns = [r'(?P<date>[\d]{1,2}\/[\d]{1,2}\/[\d]{1,2})'
                        r', (?P<time>[\d]{1,2}:[\d]{1,2}.[AP]M)',
                        r' - (?P<member>[^:]+):',
                        r' (?P<text>.*)']
        msg_pattern = re.compile(''.join(msg_patterns))
        
        for msg in self.chat:
            m = msg_pattern.match(msg)
            
            if m:
                msg_date = m.group("date")
                msg_time = m.group("time").replace("\u202f", "-")
                msg_member = m.group("member")
                msg_text = m.group("text")
                
                if msg_member not in self.members: self.members.append(msg_member)
                
                # Cast the msg_time from str to HourMinuteTime format
                hhmm, suffix = msg_time.split('-')
                msg_hour, msg_minute = map(int, hhmm.split(':'))
                if suffix == "AM":
                    if msg_hour == 12:
                        msg_hour = 0 
                else: 
                    if msg_hour != 12:
                        msg_hour += 12
                
                # Cast the msg_date from str DayMonthYearDate format 
                msg_month, msg_day, msg_year = map(int, msg_date.split('/'))
                
                message = Message(
                    text = msg_text,
                    author = msg_member,
                    time = HourMinuteTime(
                        hour = msg_hour,
                        minute = msg_minute
                    ),
                    date = DayMonthYearDate(
                        day = msg_day,
                        month = msg_month,
                        year = msg_year
                    )
                )
                
                self.messages.append(message)

    def process_chat(self):
        """
        1. Remove trash messages.
        2. Merge multiline messages.
        3. Merge multi-messages.
        4. Apply several NLP techniques to improve the quality.
        """
        self.remove_invalid_messages()
        self.merge_multiline_messages()
        self.merge_multisent_messages()
        self.remove_low_quality_messages()
        self.create_messages_data()
    
    """
    Type of messages to be removed:
    11/7/25, 10:05 AM - 'name': <Media omitted>
    7/6/24, 11:30 AM - 'name' added 'name'
    11/8/25, 10:39 PM - 'name': This message was deleted
    10/1/24, 6:44 PM - 'name' left
    5/27/22, 12:24 PM - 'name' removed 'name'
    5/19/22, 7:36 PM - 'name':
    3/31/24, 10:36 PM - ERROR: can't send to this group, not a member
    """
    def remove_invalid_messages(self):
        def msg_filters(msg):
            begin = '^[\d]{1,2}\/[\d]{1,2}\/[\d]{1,2}, [\d]{1,2}:[\d]{1,2}.[AP]M - '
            
            if re.compile(begin + '.+: <Media omitted>$').match(msg) : return False
            if re.compile(begin + '.+: added .+$').match(msg) : return False
            if re.compile(begin + '.+: This message was deleted$').match(msg) : return False
            if re.compile(begin + '.+: left$').match(msg) : return False
            if re.compile(begin + '.+: removed .+$').match(msg) : return False
            if re.compile(begin + '.+: $').match(msg) : return False
            if re.compile(begin + "ERROR: can't send to this group, not a member$").match(msg) : return False

            return True
        
        self.chat = list(filter(msg_filters, self.chat))


    """
    Merge messages like:
    11/12/2025, 11:05 AM - Foo: This is amazing
                                 I mean, really amazing
    """
    def merge_multiline_messages(self):
        is_multiline = False
        msg_pattern = re.compile('^[\d]{1,2}\/[\d]{1,2}\/[\d]{1,2}, [\d]{1,2}:[\d]{1,2}.[AP]M - .+')
        multiline_buffer = None
        merged_msgs = []
        
        for msg in self.chat:
            if msg_pattern.match(msg):
                if is_multiline:
                    merged_msgs.append(''.join(multiline_buffer))
                    is_multiline = False
                else:
                    if multiline_buffer is not None: merged_msgs.append(multiline_buffer[0])
                multiline_buffer = [msg]
            
            else:
                multiline_buffer.append(msg)
                is_multiline = True
        
        self.chat = merged_msgs
        
    """
    Merge messages like:
    11/12/2025, 11:05 AM - Foo: This is amazing
    11/12/2025, 11:06 AM - Foo: no, really AMAZING!
    """
    def merge_multisent_messages(self):
        msg_patterns = [r'(?P<date>[\d]{1,2}\/[\d]{1,2}\/[\d]{1,2})'
                        r', (?P<time>[\d]{1,2}:[\d]{1,2}.[AP]M)',
                        r' - (?P<member>[^:]+):',
                        r' (?P<text>.*)']
        msg_pattern = re.compile(''.join(msg_patterns))
        multimessage_buffer = []
        prev_msg_member = None
        merged_msgs = []
        
        for msg in self.chat:
            m = msg_pattern.match(msg)
            
            if m:
                msg_member = m.group("member")
                msg_text = m.group("text")
                
                if prev_msg_member is not None and prev_msg_member == msg_member:
                    multimessage_buffer.append(msg_text)
                    continue
                elif len(multimessage_buffer) > 0:
                    merged_msgs.append(''.join(multimessage_buffer))
                
                multimessage_buffer = [msg]
                prev_msg_member = msg_member
            else:
                if len(multimessage_buffer) > 0: merged_msgs.append(''.join(multimessage_buffer))
                prev_msg_member = None
                merged_msgs.append(msg) 
        
        self.chat = merged_msgs
    
    """
    Remove messages like:
     * This process uses Spanish languge *
    11/12/2025, 11:05 AM - Foo: Okey
    11/12/2025, 11:06 AM - Foo: Haha
    """
    def remove_low_quality_messages(self):
        low_quality_words = ["a"]

        msg_patterns = [r'(?P<date>[\d]{1,2}\/[\d]{1,2}\/[\d]{1,2})'
                        r', (?P<time>[\d]{1,2}:[\d]{1,2}.[AP]M)',
                        r' - (?P<member>[^:]+):',
                        r' (?P<text>.*)']
        msg_pattern = re.compile(''.join(msg_patterns), re.DOTALL)

        def clean_text(text, stop_words):
            text = text.lower()
            text = text.translate(str.maketrans('', '', string.punctuation))
            words = text.split()
            return [w for w in words if w not in stop_words]
        
        def good_enough(msg):
            m = msg_pattern.match(msg)
            if m:
                msg_text = m.group("text")

                msg_words = clean_text(msg_text, low_quality_words)

                if len(msg_words) > 10:
                    return True
                else:
                    return False
            
        self.chat = list(filter(good_enough, self.chat))
        
    
