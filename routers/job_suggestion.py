from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.profile import CandidateProfile
from pydantic import BaseModel
from services.deps import get_current_user, get_db
import os
import google.generativeai as genai

router = APIRouter()


# Cấu hình Gemini
genai.configure(api_key="AIzaSyBNnPljQsx0sDanyEhXDbTy-UGd0jhkTS4")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

@router.get("/suggest-jobs")
def suggest_jobs(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user_id = current_user.id
    profile = db.query(CandidateProfile).filter_by(user_id=user_id).first()
    if not profile:
        return {"error": "Profile not found"}

    prompt = f"""
    Dựa trên hồ sơ ứng viên dưới đây, hãy gợi ý 5 công việc phù hợp dưới dạng JSON:
    Học vấn: {profile.education}
    Kinh nghiệm: {profile.experience}
    Kỹ năng: {profile.skills}
    """

    try:
        response = model.generate_content(prompt)
        return {"suggested_jobs": response.text}
    except Exception as e:
        return {"error": str(e)}
    

class ChatRequest(BaseModel):
    message: str

@router.post("/chatbot")
def chat_with_bot(request: ChatRequest):
    try:
        response = model.generate_content(request.message)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
