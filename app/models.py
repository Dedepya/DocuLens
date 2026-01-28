from sqlalchemy import Column, Integer, String, JSON, Text
from pgvector.sqlalchemy import Vector
from .database import Base

class ResumeAnalysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    match_score = Column(Integer)
    # Stores the full AI feedback (skills gap, suggestions, etc)
    analysis_data = Column(JSON) 
    # Store embedding for future semantic search (similarity)
    embedding = Column(Vector(1536))