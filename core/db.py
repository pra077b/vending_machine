from contextlib import contextmanager

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dataclasses import dataclass, fields


POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DATABASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
DbSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Model(Base):
    __abstract__ = True

    def as_dict(self):
        return {
            k: getattr(self, k)
            for k in self.__table__.columns.keys()
        }

    def to_dc(self, dc: dataclass):
        return dc(**{
            f.name: getattr(self, f.name)
            for f in fields(dc)
        })


@contextmanager
def db_context():
    """
    A context manager for providing the db session
    @rtype: object
    """
    db = DbSession()
    try:
        yield db
    except BaseException:
        db.rollback()
        raise
    finally:
        db.close()
