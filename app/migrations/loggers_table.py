from sqlalchemy import Column, String, Integer
from app.db import Base

class Logger(Base):
    __tablename__ = "loggers"

    id = Column(Integer, primary_key=True, index=True)
    log_message = Column(String)
    log_level = Column(String)
