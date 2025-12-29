from pydantic import BaseModel

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

class Filter(BaseModel):
    members  : list[str] = []    
    min_time : HourMinuteTime | None
    max_time : HourMinuteTime | None
    min_date : DayMonthYearDate | None
    max_date : DayMonthYearDate | None
    
class RoomInit(BaseModel):
    max_players: int
    filters : Filter | None
    
    