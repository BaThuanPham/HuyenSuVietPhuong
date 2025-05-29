from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models.job import JobPosting, JobApplication
from models.profile import CandidateProfile
from schemas.job import JobCreate
from services.deps import get_current_user, require_role, get_db
from models.interview import InterviewRound, InterviewQuestion, CandidateInterviewProgress
import json

router = APIRouter()

@router.post("/create")
def create_job(job: JobCreate, db: Session = Depends(get_db), current_user=Depends(require_role(["hr", "admin"]))):
    job_entry = JobPosting(
        title=job.title,
        description=job.description,
        employment_type=job.employment_type,
        locations=json.dumps(job.locations),
        category=job.category,
        salary=job.salary,
        company_name=job.company_name,
        recruiter_id=current_user.id
    )
    db.add(job_entry)
    db.commit()
    return {"msg": "Job posted successfully"}

#ứng viên ứng tuyển job
@router.post("/apply/{job_id}")
def apply_to_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["candidate"]))
):
    # Kiểm tra hồ sơ ứng viên đã tồn tại
    profile = db.query(CandidateProfile).filter_by(user_id=current_user.id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="Candidate profile not found.")

    # Kiểm tra job có tồn tại không
    job = db.query(JobPosting).filter_by(id=job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    # Kiểm tra đã ứng tuyển chưa
    existing = db.query(JobApplication).filter_by(user_id=current_user.id, job_id=job_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already applied to this job.")

    # Thêm mới ứng tuyển
    application = JobApplication(user_id=current_user.id, job_id=job_id)
    db.add(application)
    db.commit()
    return {"msg": "Application submitted successfully."}

#lấy thông tin các job đã tồn tại và lọc dùng cho hiển thị bên ứng viênviên
@router.get("/all")
def get_all_jobs(
    location: str = Query(None),
    category: str = Query(None),
    employment_type: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(JobPosting)

    if category:
        query = query.filter(JobPosting.category.ilike(f"%{category}%"))
    
    if employment_type:
        query = query.filter(JobPosting.employment_type == employment_type)
    
    jobs = query.all()

    result = []

    for job in jobs:
        locations = json.loads(job.locations)
        if location and location.lower() not in [loc.lower() for loc in locations]:
            continue  # Bỏ qua job không khớp location

        result.append({
            "job_id": job.id,
            "title": job.title,
            "description": job.description,
            "employment_type": job.employment_type,
            "locations": locations,
            "category": job.category,
            "salary": job.salary,
            "company name": job.company_name,
            "recruiter_id": job.recruiter_id
        })

    return result


#lấy thông tin các job hr đã đăng và các ứng viên đã ứng tuyển của từng job - hiển thị bên hr
@router.get("/applied-candidates")
def get_applied_candidates_by_job(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["hr"]))
):
    jobs = db.query(JobPosting).filter_by(recruiter_id=current_user.id).all()
    if not jobs:
        return {"msg": "No jobs posted yet."}

    result = []

    for job in jobs:
        applications = db.query(JobApplication).filter_by(job_id=job.id).all()

        # Lấy danh sách các vòng phỏng vấn của job
        interview_rounds = db.query(InterviewRound).filter_by(job_id=job.id).all()
        rounds_info = [
            {"round_number": r.round_number, "title": r.title, "description": r.description}
            for r in sorted(interview_rounds, key=lambda x: x.round_number)
        ]

        candidates = []
        for app in applications:
            profile = db.query(CandidateProfile).filter_by(user_id=app.user_id).first()
            progress = db.query(CandidateInterviewProgress).filter_by(user_id=app.user_id, job_id=job.id).first()

            current_round_info = None
            if progress:
                round_match = next((r for r in interview_rounds if r.round_number == progress.current_round), None)
                if round_match:
                    current_round_info = {
                        "current_round_number": progress.current_round,
                        "current_round_title": round_match.title,
                        "interview_time": round_match.interview_time
                    }

            if profile:
                candidates.append({
                    "user_id": app.user_id,
                    "full_name": profile.full_name,
                    "experience": profile.experience,
                    "skills": profile.skills,
                    "education": profile.education,
                    "cv_url": profile.cv_url,
                    "interview_progress": current_round_info
                })

        result.append({
            "job_id": job.id,
            "job_title": job.title,
            "interview_rounds": rounds_info,
            "candidates": candidates
        })

    return result



@router.get("/jobdetail/{job_id}")
def get_job_detail(
    job_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)  # Cho phép cả ứng viên và HR xem
):
    job = db.query(JobPosting).filter_by(id=job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    candidates = []
    if current_user.role in ["hr", "admin"] and job.recruiter_id == current_user.id:
        applications = db.query(JobApplication).filter_by(job_id=job_id).all()
        
        # Lấy danh sách các vòng phỏng vấn của job để tra cứu tiêu đề
        interview_rounds = db.query(InterviewRound).filter_by(job_id=job_id).all()

        for app in applications:
            profile = db.query(CandidateProfile).filter_by(user_id=app.user_id).first()
            progress = db.query(CandidateInterviewProgress).filter_by(user_id=app.user_id, job_id=job_id).first()

            current_round_info = None
            if progress:
                matched_round = next((r for r in interview_rounds if r.round_number == progress.current_round), None)
                if matched_round:
                    current_round_info = {
                        "current_round_number": progress.current_round,
                        "current_round_title": matched_round.title,
                        "interview_time": matched_round.interview_time
                    }

            if profile:
                candidates.append({
                    "user_id": app.user_id,
                    "full_name": profile.full_name,
                    "experience": profile.experience,
                    "skills": profile.skills,
                    "education": profile.education,
                    "cv_url": profile.cv_url,
                    "interview_progress": current_round_info
                })

    return {
        "title": job.title,
        "description": job.description,
        "employment_type": job.employment_type,
        "locations": json.loads(job.locations),
        "category": job.category,
        "salary": job.salary,
        "company_name": job.company_name,
        "candidates": candidates if candidates else "Restricted or no applications yet"
    }

