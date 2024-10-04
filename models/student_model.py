from typing import Optional
from pydantic import BaseModel, Field

class Student(BaseModel):
    ''' Class for agent to fill out, which fits with SQL table '''
    
    username: str = Field(description='The username for the student, which is a unique identifier')
    name: Optional[str] = Field(None, description='Name of student')
    summary: Optional[str] = Field(None, description='A summary of the students profile, based on available fields')
    @property
    def persona(self) -> str:
        return f"Username:\n {self.username}\n Name:\n {self.name}\nSummary\n {self.summary}"