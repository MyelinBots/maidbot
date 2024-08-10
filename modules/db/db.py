import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class DB():

    def __init__(self):
        postgresDSN = os.getenv('POSTGRES_DSN', 'postgresql+psycopg2://pigeon:mysecretpassword@localhost:5432/pigeon')
        self.db = create_engine(postgresDSN)
        self.db.connect()
        Base.metadata.create_all(self.db)
        self.session = None
        print('Database connected')

    def getSession(self):
        if self.db is None:
            raise Exception('Database not connected')
        if self.session is not None:
            return self.session
        # create a session
        self.session = Session(bind=self.db)

        return self.session


    def close(self):
        self.session.close()
        self.db.dispose()
        print('Database disconnected')

    def commit(self):
        self.session.commit()
        print('Database committed')

    def rollback(self):
        self.session.rollback()
        print('Database rolled back')

