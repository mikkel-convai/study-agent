import sqlite3
from utils.llm_utils import llm
from models.student_model import Student
from states.study_agent_state import StudyAgentState
from langchain_core.messages import SystemMessage, HumanMessage

student_db_path = "database/students/students.db"

################ Loading student from DB ################
def fetch_student_profile(username: str) -> Student:
    ''' Retrieve student profile if existing '''
    
    # Connect to the SQLite database (adjust the path to your database file)
    connection = sqlite3.connect(student_db_path)
    cursor = connection.cursor()

    # Execute the query to search for the student by username
    cursor.execute('SELECT * FROM students WHERE username = ?', (username,))

    # Fetch the result
    student_data = cursor.fetchone()

    # Close the connection
    cursor.close()
    connection.close()

    # If a student is found, return a Student object, otherwise return None
    if student_data:
        _, username, name, summary = student_data
        return Student(username=username, name=name, summary=summary)
    else:
        return Student(username=username)
    
def load_student(state: StudyAgentState) -> StudyAgentState:
    ''' Loading user from SQL based on username, if it exists '''
    print('--- Loading Student ---')
    username = state['username']
    student = fetch_student_profile(username)
    
    return {'student': student}

################ Extract student info ################
profiling_prompt = '''
You are an intelligent student profiling assistant responsible for analyzing student queries to determine if new 
information is available for updating the student profile. Your task is not to respond directly to the user 
but to route the query based on whether new student data is present.

Information you should look for includes:

    Name
    Topic or subject being studied
    Academic profile (e.g., courses, level of study)
    Learning goals (e.g., objectives or future targets)
    Preferences (e.g., study methods, preferred learning materials)

If the query provides new student data, return: <student_profiling>[extracted information]</student_profiling>

If there is no new data to update, return: No new user data

This node does not interact with the user directly but ensures that any new student information is properly 
flagged for future updates.

Here is what we know about the student so far:
{student_persona}
'''

# TODO: Make better, see comments below
# This node sets the new_profiling_info state
# It could be changed into a route, if it didn't have to set stage
def extract_student_info(state: StudyAgentState):
    ''' Node/Route for whether to update student profile or not '''
    print('--- Extract student info ---')
    student = state['student']
    latest_message = state['messages'][-1]

    formatted_prompt = profiling_prompt.format(student_persona = student.persona)
    route = llm.invoke([SystemMessage(content=formatted_prompt)] + [latest_message])

    if '<student_profiling>' in route.content:
        print('Updated new profiling info in state')
        return {'new_profiling_info': route.content}
    else:
        print('No further profiling data')

################ Update student profile ################
# Update profile
def update_db(student: Student) -> None:
    ''' Update student profile if existing '''
    print('--- Updating DB ---')
    # Connect to the SQLite database (adjust the path to your database file)
    connection = sqlite3.connect(student_db_path)
    cursor = connection.cursor()

    # Execute the query to upsert the student
    cursor.execute(
        '''
        INSERT INTO students (username, name, summary)
        VALUES (:username, :name, :summary)
        ON CONFLICT(username) 
        DO UPDATE SET 
            name = excluded.name,
            summary = excluded.summary;
        ''', 
        {
            'username': student.username,
            'name': student.name,
            'summary': student.summary
        }
    )

    # Commit the transaction to save the changes
    connection.commit()

    # Close the connection
    cursor.close()
    connection.close()

    print('DB updated')

update_student_prompt = ''' 
You are tasked with updating the profile of the following student. The student's current profile will be provided below. Review the profile and update any missing or incomplete fields, including the student's name and summary.

- If the student's name is missing or incorrect, suggest an appropriate name or confirm the correct name if possible.
- If the summary is incomplete, add relevant details to provide a more complete profile of the student's academic background or learning habits.
- Do not modify the username, as it is a unique identifier.

Here is the student's current profile:
Username: {student_username}
Name: {student_name}
Summary: {student_summary}

Here is what was extracted from the agent:
{extracted_info}

Please provide the updated profile with all relevant fields filled in. If a field is already complete, leave it unchanged.
'''

def update_profile(state: StudyAgentState):
    """ Node for updating the student profile """
    print('--- Updating student ---')
    student = state['student']
    messages = state['messages']
    extracted_info = state['new_profiling_info']

    formatted_prompt = update_student_prompt.format(
        student_username=student.username,
        student_name=student.name if student.name else "Not Provided",
        student_summary=student.summary if student.summary else "Not Provided",
        extracted_info=extracted_info
    )

    structured_llm = llm.with_structured_output(Student)
    updated_student = structured_llm.invoke(
        [SystemMessage(content=formatted_prompt)] + 
        [HumanMessage(content=f'Student to update: \n {student.persona}')] +
        messages
    )

    print(f'Student before: \n {student}')
    print(f'Updated student: \n {updated_student}')
    
    update_db(updated_student)

    return {'student': updated_student, 'new_profiling_info': ''}