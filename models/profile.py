from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class CandidateProfile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    full_name = Column(String)
    phone = Column(String)
    email = Column(String)
    education = Column(String)
    experience = Column(String)
    skills = Column(String)
    cv_url = Column(String)

    user = relationship("User", back_populates="profile", foreign_keys=[user_id])

