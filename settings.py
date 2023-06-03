import sqlalchemy as sa
from sqlalchemy.orm import Session, sessionmaker

import models
from fill_db import fill_db

SQLALCHEMY_DATABASE_URL = "sqlite:///database.db"

engine = sa.create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

ins = sa.inspect(engine)
print(len(ins.get_table_names()))
if len(ins.get_table_names()) == 0:
    models.Base.metadata.create_all(bind=engine)
    fill_db(Session(engine))
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
