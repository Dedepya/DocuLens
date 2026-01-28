from pydantic import BaseModel, ConfigDict
from typing import List, Dict

class AnalysisDetail(BaseModel):
    match_score: int
    technical_skills_gap: List[str]
    soft_skills_gap: List[str]
    section_feedback: Dict[str, str]
    rewrite_suggestions: List[str]

class AnalysisResponse(BaseModel):
    id: int
    filename: str
    match_score: int
    analysis_data: AnalysisDetail

    model_config = ConfigDict(from_attributes=True)