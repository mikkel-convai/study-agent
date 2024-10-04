from typing import Literal
from states.study_agent_state import StudyAgentState

def retriever_route(state: StudyAgentState):
    ''' Deciding which retriever to use based on session documents '''

    session_docs = state.get('session_docs', [])

    if len(session_docs) == 0:
        return 'chroma_retriever'
    else:
        return 'inmemory_retriever'

def got_docs(state: StudyAgentState):
    ''' Check if there are relevant documents for the teachers answer '''
    # TODO: Add a max_turns to state and/or a web search or other deafult

    relevant_docs = state.get('documents', [])

    if len(relevant_docs) == 0:
        return 'chroma_retriever'
    else:
        return 'teacher'

# Check student state
def student_exist_route(state: StudyAgentState) -> Literal['load_student', 'extract_student_info']:
    ''' Router to load user if profile not in state '''
    print('--- Student exist route ---')
    student = state.get('student', None)

    # If the student doesn't exist, a node for loading or creating student is used
    if student is None:
        return 'load_student'
    
    return 'extract_student_info'

# Routing to updating student
def update_student_route(state: StudyAgentState):
    ''' Route for deciding whether to update student profile or just answer questions '''
    print('--- New student info route ---')
    new_profiling_info = state.get('new_profiling_info', '')

    if new_profiling_info:
        print(new_profiling_info)
        return 'update_profile'
    else:
        print('No new info')
        return 'retriever'
