from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base

class JobPosting(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    recruiter_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(Text)
    employment_type = Column(String)
    locations = Column(String)
    category = Column(String)
    salary = Column(String)
    company_name = Column(String)
    
    interview_rounds = relationship("InterviewRound", back_populates="job", cascade="all, delete-orphan")
    interview_progresses = relationship("CandidateInterviewProgress", back_populates="job")


class JobApplication(Base):
    __tablename__ = "job_applications"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))

    __table_args__ = (UniqueConstraint('user_id', 'job_id', name='_user_job_uc'),)