from nodes.teacher import answering_teacher
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from states.study_agent_state import StudyAgentState
from edges.edges import student_exist_route, update_student_route
from nodes.student_profile import load_student, extract_student_info, update_profile
from nodes.retrievers import dummy_retriever, retrieve_docs_chroma, retrieve_docs_inmemory, grade_docs

studyagent_workflow = StateGraph(StudyAgentState)

# Student profiling
studyagent_workflow.add_node('load_student', load_student)
studyagent_workflow.add_node('extract_student_info', extract_student_info)
studyagent_workflow.add_node('update_profile', update_profile)

# RAG
studyagent_workflow.add_node('retriever', dummy_retriever)
studyagent_workflow.add_node('chroma_retriever', retrieve_docs_chroma)
studyagent_workflow.add_node('inmemory_retriever', retrieve_docs_inmemory)
studyagent_workflow.add_node('grader', grade_docs)

# Answering
studyagent_workflow.add_node('teacher', answering_teacher)

# Edges
studyagent_workflow.add_conditional_edges(START, student_exist_route, ['load_student', 'extract_student_info'])
studyagent_workflow.add_edge('load_student', 'extract_student_info')
studyagent_workflow.add_conditional_edges('extract_student_info', update_student_route, ['update_profile', 'retriever'])

studyagent_workflow.add_edge('update_profile', 'retriever')
studyagent_workflow.add_edge('retriever', 'inmemory_retriever')
studyagent_workflow.add_edge('retriever', 'chroma_retriever')
studyagent_workflow.add_edge('inmemory_retriever', 'grader')
studyagent_workflow.add_edge('chroma_retriever', 'grader')
studyagent_workflow.add_edge('grader', 'teacher')
studyagent_workflow.add_edge('teacher', END)

memory = MemorySaver()
study_agent_graph = studyagent_workflow.compile(checkpointer=memory)