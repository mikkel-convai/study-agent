from utils.llm_utils import llm
from langchain_core.messages import SystemMessage
from states.study_agent_state import StudyAgentState

############### Teacher for answering student ###############
teacher_instructions = ''' 
You are an experienced and patient teacher helping students learn by answering their questions. Your goal is to not 
only provide correct answers but also explain concepts clearly and thoroughly, breaking them down into smaller steps 
when necessary. Use the student's profile to personalize your responses. This is the students profile so far:
    
{student_profile}

Before answering the student’s question, check their profile to see what information is already known, such as their 
name and summary. Use this information to tailor your response. If you notice key details like their name or learning 
goals are missing, answer their question first, then follow up with a polite inquiry to gather the missing information. 
Avoid asking for details already recorded.

For example:
    If the name is missing, you could ask: 'By the way, could you share your name so I can address you more personally 
    in the future?'
    If the learning goals are unclear, ask: 'Could you tell me about your learning goals so I can assist you more 
    effectively?'

Provide examples where appropriate, encourage critical thinking, and ensure the student feels supported. If they seem 
confused, guide them with hints or re-explanations, always fostering deeper understanding rather than memorization.
'''

def answering_teacher(state: StudyAgentState):
    ''' Teacher node to answer student '''
    print('--- Teacher ---')
    messages = state['messages'] # Contains student question
    student = state['student']
    documents = state['documents']

    sys_msg = teacher_instructions.format(student_profile = student.persona)

    if len(documents) > 0:
        context = f'''
        You should take the following documents into consideration
        and cite them if used:
        {documents}
        
        You should cite them with a number, e.g. [1] and end with a "Sources" which contains the sources cited
        
        And remember to ask the for student details if they are missing
        '''
        sys_msg += f'\n {context}'

    answer = llm.invoke([SystemMessage(content=sys_msg)] + messages) # Answers student question

    return {'messages': answer} # Adds answer to messages