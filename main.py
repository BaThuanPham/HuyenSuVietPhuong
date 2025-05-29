from fastapi import FastAPI
from routers import auth, profile, job_suggestion, job, interview


app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(profile.router, prefix="/candidate", tags=["Profile"])
app.include_router(job_suggestion.router, prefix="/suggestion", tags=["Job Suggestion"])
app.include_router(interview.router, prefix="/interview", tags=["Interview"])
app.include_router(job.router, prefix="/jobs", tags=["Jobs"])

#python -m venv venv #dung lan dau de khoi tao
#venv\Scripts\activate 
#uvicorn main:app --reload

#pip install -r requirements.txt
#http://localhost:8000/docs
