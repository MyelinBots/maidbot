from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Weather(Base):
    __tablename__ = 'weathers'

    # automate uuid generation
    id: Mapped[str] = mapped_column(String, primary_key=True)
    nick: Mapped[str] = mapped_column(String)
    server: Mapped[str] = mapped_column(String)
    channel: Mapped[str] = mapped_column(String)
    location: Mapped[str] = mapped_column(String)
    
    def __repr__(self) -> str:
        return f'<Weather(nick={self.nick}, server={self.server}, channel={self.channel}, location={self.location})>'
