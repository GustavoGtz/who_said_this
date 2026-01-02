from pydantic import BaseModel

# ########################################### #
#              USEFUL MODELS                  #
# ########################################### #

class DayMonthYearDate(BaseModel):
    day   : int
    month : int
    year  : int

class HourMinuteTime(BaseModel):
    hour   : int
    minute : int

class Message(BaseModel):
    text   : str
    author : str
    time   : HourMinuteTime
    date   : DayMonthYearDate

class RoundMessage(BaseModel):
    text   : str
    time   : HourMinuteTime
    date   : DayMonthYearDate
    answer : str | None
    options : list[str]

class Filter(BaseModel):
    members  : list[str] = []    
    min_time : HourMinuteTime | None
    max_time : HourMinuteTime | None
    min_date : DayMonthYearDate | None
    max_date : DayMonthYearDate | None


# ########################################### #
#             PAYLOAD MODELS                  #
# ########################################### #

class RoomInitPayload(BaseModel):
    filter: Filter
    max_players: int

class RoomRandomizeMessagesPayload(BaseModel):
    number_of_messages : int

class RoomSetSecondsPerRound(BaseModel):
    seconds : int
    


    
    