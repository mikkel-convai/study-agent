import os
from langchain_chroma import Chroma
from utils.llm_utils import embeddings

current_dir = os.path.dirname(os.path.abspath("index.py"))
db_dir = os.path.join(current_dir, "database")
persistent_directory = os.path.join(db_dir, "student_uploads")

db = Chroma(
    persist_directory=persistent_directory,
    embedding_function=embeddings
)

retriever = db.as_retriever()