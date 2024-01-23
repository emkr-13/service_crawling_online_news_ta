import json
import datetime as dt
from dataclasses import dataclass

@dataclass
class JSONTrait:
    def dict(self):
        return asdict(self)

    def json(self):
        return json.dumps(self.dict(), default=str)
       
@dataclass
class ListProgressOnlineNews(JSONTrait):
    id:str
    name:str
    since_time:dt.date
    progress_time:dt.date
    until_time:dt.date
    
@dataclass 
class OnlineNews(JSONTrait):
    title:str
    news_published_at:dt.datetime
    content:str 
    url:str
    asal_berita:str
