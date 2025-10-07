from typing import Optional, List

from pydantic import BaseModel


class Slip(BaseModel):
    id: int
    advice: str
    date: Optional[str] = None

class AdviceResponse(BaseModel):
    slip:Slip


class SearchResponse(BaseModel):
    total_results: str
    query: str
    slips: List[Slip]


class ErrorMessage(BaseModel):
    type: str
    text: str

class ErrorResponse(BaseModel):
    message: ErrorMessage

