from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import os
import time

engine = create_engine(
    os.environ['DATABASE_URL'],
    connect_args={ 'sslmode':'disable' },
    isolation_level='SERIALIZABLE' # monitor performance versus REPEATABLE READ
)

RETRIES = 5
RETRY_WAIT = 2
for n in range(RETRIES):
    try:
        with engine.connect():
            break
    except OperationalError:
        time.sleep(RETRY_WAIT)
else:
    raise Exception('Database not available...')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from akira.models.annotator import Annotator
from akira.models.assignment import Assignment
from akira.models.item import Item
from akira.models.decision import Decision