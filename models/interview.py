# models/interview.py
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from models.job import JobPosting
from models.user import User

class InterviewRound(Base):
    __tablename__ = "interview_rounds"
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    round_number = Column(Integer)
    title = Column(String)
    description = Column(Text)
    interview_time = Column(String)  

    job = relationship("JobPosting", back_populates="interview_rounds")
    questions = relationship("InterviewQuestion", back_populates="round", cascade="all, delete-orphan")

class InterviewQuestion(Base):
    __tablename__ = "interview_questions"
    id = Column(Integer, primary_key=True)
    round_id = Column(Integer, ForeignKey("interview_rounds.id"))
    question_text = Column(Text)

    round = relationship("InterviewRound", back_populates="questions")

class CandidateInterviewProgress(Base):
    __tablename__ = "candidate_interview_progress"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    current_round = Column(Integer, default=0)


    user = relationship("User", back_populates="interview_progress", foreign_keys=[user_id])
    job = relationship("JobPosting", back_populates="interview_progresses")
