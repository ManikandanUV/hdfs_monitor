from sqlalchemy import create_engine, Column, BigInteger, DateTime, String, Boolean, func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Monitors(Base):
    __tablename__ = 'active_monitors'

    id = Column(BigInteger, primary_key=True)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = Column(DateTime, default=func.current_timestamp(),
                           onupdate=func.current_timestamp())
    dir_path = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)

    def __init__(self, dir_path, is_active=True):
        """
        :string dir_path: Directory path to be monitored
        :boolean is_active: Is the directory active for monitoring
        """
        self.dir_path = dir_path
        self.is_active = is_active


class Messages(Base):
    __tablename__ = 'message_log'

    id = Column(BigInteger, primary_key=True)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = Column(DateTime, default=func.current_timestamp(),
                           onupdate=func.current_timestamp())
    dir_id = Column(BigInteger, nullable=False)
    filename = Column(String, nullable=False)
    message = Column(String, nullable=False)
