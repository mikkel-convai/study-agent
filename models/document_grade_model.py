from pydantic import BaseModel, Field

class DocumentGrade(BaseModel):
    document_grade: str = Field(description="Grading of retrieved document, 'useful' or 'useless'")