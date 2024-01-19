import json
import datetime as dt
from dataclasses import asdict, dataclass


@dataclass
class JSONTrait:
    def dict(self):
        return asdict(self)

    def json(self):
        return json.dumps(self.dict(), default=str)
    
class ListOnlineNews(JSONTrait):
    id:str
    name:str
    since_time:dt.date
    progress_time:dt.date
    until_time:dt.date
    
    def __init__(self, *args):
        (
            self.id,
            self.name,
            self.since_time,
            self.progress_time,
            self.until_time
        ) = args
        
    def __dir__(self):
        return [
            "id",
            "name",
            "since_time",
            "progress_time",
            "until_time"
        ]
    
    def __repr__(self):
        return dict(
            (x, y)
            for (x, y) in zip(
                dir(self),
                (self.__getattribute__(x) for x in dir(self)),
            )
        ).__str__()

class OnlineNews(JSONTrait):
    title:str
    news_published_at:dt.datetime
    content:str 
    url:str
    asal_berita:str
    
    def __init__(self, *args):
        (
            self.title,
            self.news_published_at,
            self.content,
            self.url,
            self.asal_berita
        ) = args
    
    def __dir__(self):
        return [
            "title"
            "news_published_at",
            "content",
            "url",
            "asal_beirta"
        ]
        
    def __repr__(self):
        return dict(
            (x, y)
            for (x, y) in zip(
                dir(self),
                (self.__getattribute__(x) for x in dir(self)),
            )
        ).__str__()