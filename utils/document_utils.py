# utils/document_utils.py
import tempfile
import streamlit as st
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader

# Text splitter for handling user-defined docs
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Number of characters per chunk
    chunk_overlap=100  # Overlap between chunks (helps retain context between chunks)
)

def process_uploaded_files(uploaded_files):
    documents = []
    # Check if files are uploaded
    for uploaded_file in uploaded_files:
        # Map the correct loader based on file type
        if uploaded_file.name.endswith(".pdf"):
            loader_class = PyMuPDFLoader
        elif uploaded_file.name.endswith(".txt"):
            loader_class = TextLoader
        else:
            st.error(f"Unsupported file type: {uploaded_file.name}")
            continue

        # Process the uploaded file and extract content
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())  # Write file content to a temporary file
            tmp_file_path = tmp_file.name  # Get the path to the temporary file
            loader = loader_class(tmp_file_path)  # Initialize the appropriate loader
            loaded_documents = loader.load()  # Load the document content

            # Split the document into smaller chunks
            for doc in loaded_documents:
                chunks = text_splitter.split_text(doc.page_content)  # Split text into smaller chunks
                # Wrap each chunk in a Document object
                for chunk in chunks:
                    documents.append(Document(page_content=chunk, metadata={"source": uploaded_file.name}))

    return documents
