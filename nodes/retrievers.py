from utils.db_utils import retriever
from utils.llm_utils import embeddings, llm
from states.study_agent_state import StudyAgentState
from langchain_core.prompts import ChatPromptTemplate
from models.document_grade_model import DocumentGrade
from langchain_community.vectorstores import DocArrayInMemorySearch

################ Dummy for entering retrievers ################
def dummy_retriever(state: StudyAgentState):
    ''' Node before deciding which retriever to use'''
    pass

################ Chroma retriever ################
def retrieve_docs_chroma(state: StudyAgentState):
    ''' Retriever for getting context and docs '''
    print('--- Chroma Retriever ---')
    query = state["messages"][-1].content
    
    # embeddings = AzureOpenAIEmbeddings(model=os.getenv("AZURE_OPENAI_EMB_DEPLOYMENT_NAME"))
    # current_dir = os.path.dirname(os.path.abspath("full_development.ipynb"))
    # db_dir = os.path.join(current_dir, "db")
    # persistent_directory = os.path.join(db_dir, "test_material")
    # db = Chroma(
    #     persist_directory=persistent_directory,
    #     embedding_function=embeddings
    # )
    # retriever = db.as_retriever()
    docs = retriever.invoke(query)

    return {'documents': docs}

################ In memory retriever ################
def retrieve_docs_inmemory(state: StudyAgentState):
    ''' Retriever for getting context and docs '''
    print('--- InMemory Retriever ---')
    query = state["messages"][-1].content
    documents = state.get('session_docs', [])

    if len(documents) > 0:
        # embeddings = AzureOpenAIEmbeddings(model=os.getenv("AZURE_OPENAI_EMB_DEPLOYMENT_NAME"))
        retriever = DocArrayInMemorySearch.from_documents(documents, embeddings)

        docs = retriever.similarity_search(query, k=3)

        return {'documents': docs}
    
################ Grader ################
# Retrieval grading
grader_instruction = """
You are tasked with determining whether a document is relevant to a student's inquiry.
Evaluate the document based on its ability to directly address or provide useful information regarding the question or topic posed by the student.
If the document is relevant and contains valuable information, respond with 'useful'.
If the document is unrelated or does not contribute meaningfully to the inquiry, respond with 'useless'.
Be objective and concise in your evaluation.
"""
grader_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", grader_instruction),
        ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
    ]
)

# LLM with class as output, string of either useful or useless
grader_llm = llm.with_structured_output(DocumentGrade)

# Grader chain
doc_grader = grader_prompt | grader_llm

def grade_docs(state: StudyAgentState):
    ''' Grader to filter retrieved documents by relevance '''
    print('--- Doc Grader ---')
    question = state['messages'][-1].content
    documents = state.get('documents', [])
    filtered_docs = []
    
    if len(documents) > 0:
        for doc in documents:
            usefulness = doc_grader.invoke({'document': doc, 'question': question})
            if usefulness.document_grade == 'useful':
                filtered_docs.append(doc)
            elif usefulness.document_grade == 'useless':
                continue

    print(f'Filtered docs for now: {filtered_docs}')
    return {'documents': filtered_docs}