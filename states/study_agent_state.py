import operator
from models.student_model import Student
from langgraph.graph import MessagesState
from typing import Optional, List, Annotated

class StudyAgentState(MessagesState):
    username: str
    student: Optional[Student]
    new_profiling_info: str
    session_docs: List[str]
    documents: Annotated[List[str], operator.add]