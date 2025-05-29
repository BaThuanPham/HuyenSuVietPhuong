from fastapi import APIRouter, Depends, UploadFile, File, Form,HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.profile import CandidateProfile
from services.deps import get_current_user,get_db, require_role
from schemas.profile import ProfileUpdate
from services.deps import get_db, require_role
from models.interview import InterviewRound, InterviewQuestion, CandidateInterviewProgress
from models.job import JobPosting, JobApplication
import os, shutil

router = APIRouter()
UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/create")
def create_profile(
    phone = Form(...),
    education: str = Form(...),
    experience: str = Form(...),
    skills: str = Form(...),
    cv: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    filename = f"{current_user.id}_{cv.filename}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(cv.file, buffer)

    profile = CandidateProfile(
        user_id=current_user.id,
        full_name=current_user.full_name,
        phone=phone,
        email=current_user.email,
        education=education,
        experience=experience,
        skills=skills,
        cv_url=path 
    )
    db.add(profile)
    db.commit()
    return {"msg": "Profile created", "cv_path": path}

@router.get("/view")
def view_profile(
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["candidate"]))
):
    profile = db.query(CandidateProfile).filter_by(user_id=current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")

    return {
        "full_name": profile.full_name,
        "email": profile.email,
        "phone": profile.phone,
        "education": profile.education,
        "experience": profile.experience,
        "skills": profile.skills,
        "cv_url": profile.cv_url
    }


@router.put("/update")
def update_profile(
    data: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["candidate"]))
):
    profile = db.query(CandidateProfile).filter_by(user_id=current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found. Please create one first.")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)

    return {"msg": "Profile updated successfully", "profile": profile.__dict__}


@router.delete("/delete")
def delete_profile(
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["candidate"]))
):
    profile = db.query(CandidateProfile).filter_by(user_id=current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")

    db.delete(profile)
    db.commit()

    return {"msg": "Profile deleted successfully."}

@router.get("/candidate-detail/{candidate_id}")
def get_candidate_detail_for_hr(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["hr"]))
):
    # Lấy tất cả job của HR hiện tại
    hr_jobs = db.query(JobPosting).filter_by(recruiter_id=current_user.id).all()
    job_ids = [job.id for job in hr_jobs]

    if not job_ids:
        raise HTTPException(status_code=404, detail="You have not posted any jobs.")

    # Kiểm tra ứng viên có apply vào job nào của HR không
    application = db.query(JobApplication).filter(
        JobApplication.user_id == candidate_id,
        JobApplication.job_id.in_(job_ids)
    ).first()

    if not application:
        raise HTTPException(status_code=403, detail="Candidate has not applied to your jobs.")

    job_id = application.job_id  # Lấy job_id đầu tiên mà ứng viên đã apply

    # Lấy profile ứng viên
    profile = db.query(CandidateProfile).filter_by(user_id=candidate_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Candidate profile not found.")

    # Lấy tiến độ phỏng vấn nếu có
    progress = db.query(CandidateInterviewProgress).filter_by(user_id=candidate_id, job_id=job_id).first()
    interview_rounds = db.query(InterviewRound).filter_by(job_id=job_id).all()

    current_round_info = None
    if progress:
        round_match = next((r for r in interview_rounds if r.round_number == progress.current_round), None)
        if round_match:
            current_round_info = {
                "current_round_number": progress.current_round,
                "current_round_title": round_match.title,
                "interview_time": round_match.interview_time
            }

    return {
        "user_id": candidate_id,
        "full_name": profile.full_name,
        "experience": profile.experience,
        "skills": profile.skills,
        "education": profile.education,
        "cv_url": profile.cv_url,
        "interview_progress": current_round_info
    }
