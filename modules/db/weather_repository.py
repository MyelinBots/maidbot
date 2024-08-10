import uuid
from sqlalchemy import select
from modules.db.weather import Weather


class WeatherRepository:
    def __init__(self, db):
        self.db = db

    def get(self, nick, server, channel) -> Weather:
        session = self.db.getSession()
        stmt = select(Weather).where(Weather.nick == nick).where(Weather.server == server).where(Weather.channel == channel.lower())
        result = session.execute(stmt).first()
        weather = result[0] if result else None
        return weather

    def upsert(self, nick, server, channel, location):
        weather = self.get(nick, server, channel)
        session = self.db.getSession()
        if weather is None:
            userid = str(uuid.uuid4())
            weather = Weather(id=userid, nick=nick)
            weather.server = server
            # channel to lowercase
            weather.channel = channel.lower()
            weather.location = location
            session.add(weather)
            session.commit()
        else:
            weather.location = location
            session.commit()
        return

    def delete(self, nick, server, channel):
        session = self.db.getSession()
        # get player by nick
        weather = self.get(nick, server, channel.lower())
        # delete player
        session.delete(weather)
        session.commit()

    def getAll(self) -> list[Weather]:
        session = self.db.getSession()
        # sort by highest score
        stmt = select(Weather).order_by(Weather.nick.desc())
        result = session.execute(stmt).scalars().all()
        return result

