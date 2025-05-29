# routers/interview.py
from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session, joinedload
from services.deps import get_db, require_role
from models.interview import InterviewRound, InterviewQuestion, CandidateInterviewProgress
from models.job import JobPosting

router = APIRouter()

@router.post("/jobs/{job_id}/interview-rounds")
def create_interview_round(
    job_id: int,
    round_number: int = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    interview_time: str = Form(...),  # thêm dòng này
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["hr", "admin"]))
):
    job = db.query(JobPosting).filter_by(id=job_id, recruiter_id=current_user.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found or unauthorized")

    interview_round = InterviewRound(
        job_id=job_id,
        round_number=round_number,
        title=title,
        description=description,
        interview_time=interview_time  # thêm dòng này
    )
    db.add(interview_round)
    db.commit()
    db.refresh(interview_round)
    return {"msg": "Interview round created", "interview_round": {
        "id": interview_round.id,
        "round_number": interview_round.round_number,
        "title": interview_round.title,
        "description": interview_round.description,
        "interview_time": interview_round.interview_time
    }}



@router.post("/interview-rounds/{round_id}/questions")
def add_question(round_id: int, question_text: str = Form(...), db: Session = Depends(get_db), current_user=Depends(require_role(["hr", "admin"]))):
    interview_round = db.query(InterviewRound).join(JobPosting).filter(InterviewRound.id == round_id, JobPosting.recruiter_id == current_user.id).first()
    if not interview_round:
        raise HTTPException(status_code=404, detail="Interview round not found or unauthorized")

    question = InterviewQuestion(round_id=round_id, question_text=question_text)
    db.add(question)
    db.commit()
    db.refresh(question)
    return {"msg": "Question added", "question": question}


@router.post("/jobs/{job_id}/candidates/{user_id}/advance")
def advance_candidate(job_id: int, user_id: int, db: Session = Depends(get_db), current_user=Depends(require_role(["hr", "admin"]))):
    job = db.query(JobPosting).filter_by(id=job_id, recruiter_id=current_user.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found or unauthorized")

    progress = db.query(CandidateInterviewProgress).filter_by(job_id=job_id, user_id=user_id).first()
    if not progress:
        progress = CandidateInterviewProgress(job_id=job_id, user_id=user_id, current_round=1)
        db.add(progress)
    else:
        progress.current_round += 1
    db.commit()
    return {"msg": "Candidate advanced to next round", "current_round": progress.current_round}

    ...

@router.get("/candidate/interview-progress")
def get_interview_progress(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["candidate"]))
):
    progresses = (
        db.query(CandidateInterviewProgress)
        .options(joinedload(CandidateInterviewProgress.job))
        .filter(CandidateInterviewProgress.user_id == current_user.id)
        .all()
    )

    result = []
    for progress in progresses:
        job = progress.job

        # Truy vấn round hiện tại
        round_detail = db.query(InterviewRound).filter_by(
            job_id=job.id,
            round_number=progress.current_round
        ).first()

        result.append({
            "job": {
                "id": job.id,
                "title": job.title,
                "description": job.description,
                "employment type": job.employment_type,
                "locations": job.locations,
                "category": job.category,
                "salary": job.salary,
                "company name": job.company_name
            },
            "interview_progress": {
                "current round": progress.current_round,
                "title": round_detail.title if round_detail else None,
                "description": round_detail.description if round_detail else None,
                "interview_time": round_detail.interview_time if round_detail else None
            }
        })

    return result
