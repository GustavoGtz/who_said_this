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


# ########################################### #
#     COMPARISION FUNCTIONS (PROVISIONAL)     #
# ########################################### #

def isDateGreater(d1, d2):
    return (d1.year, d1.month, d1.day) > (d2.year, d2.month, d2.day)

def isTimeGreater(t1, t2):
    return (t1.hour, t1.minute) > (t2.hour, t2.minute)

