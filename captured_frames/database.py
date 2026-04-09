# database.py
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

# Define the base class for our ORM models
Base = declarative_base()

# Define the table schema
class ThreatLog(Base):
    __tablename__ = 'threat_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.now)
    threat_type = Column(String, default="unauthorized_device")
    is_threat = Column(Boolean, default=True)
    context_string = Column(String)
    image_path = Column(String, nullable=True)

# Create a local SQLite database engine
# echo=False keeps the console clean. Set to True to see the raw SQL queries.
engine = create_engine('sqlite:///edge_vision.db', echo=False)

# This physically creates the tables in the database file if they don't exist
Base.metadata.create_all(engine)

# Create a session factory
SessionLocal = sessionmaker(bind=engine)