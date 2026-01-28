from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .models import ResumeAnalysis
from .schemas import AnalysisResponse
from .services.parser import extract_text_from_pdf
from .services.engine import analyze_resume_content

# Initialize Database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="DocuLens AI")

@app.get("/")
def home():
    return {"message": "DocuLens AI Resume Analyzer API"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    file: UploadFile = File(...),
    jd: str = Form(...),
    db: Session = Depends(get_db)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # 1. Extract text from PDF
    pdf_bytes = await file.read()
    resume_text = extract_text_from_pdf(pdf_bytes)

    # 2. Process with AI
    analysis_json, embedding = await analyze_resume_content(resume_text, jd)

    # 3. Save to Database
    new_analysis = ResumeAnalysis(
        filename=file.filename,
        match_score=analysis_json.get("match_score", 0),
        analysis_data=analysis_json,
        embedding=embedding
    )
    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)

    return new_analysis