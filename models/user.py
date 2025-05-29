from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    full_name = Column(String)
    hashed_password = Column(String)
    role = Column(String)
    current_token = Column(String, nullable=True)

  # Nếu có nhiều mối liên hệ đến User, cần chỉ rõ foreign_keys
    profile = relationship("CandidateProfile", back_populates="user", uselist=False)
    interview_progress = relationship("CandidateInterviewProgress", back_populates="user", foreign_keys='CandidateInterviewProgress.user_id')



