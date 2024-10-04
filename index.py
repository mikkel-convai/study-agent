import tempfile
import streamlit as st
from utils.logging import get_logger
from langchain_core.messages import HumanMessage
from graphs.study_agent_graph import study_agent_graph
from utils.document_utils import process_uploaded_files

logger = get_logger()

# Messages
if "messages" not in st.session_state:
    st.session_state.messages = []

if "username" not in st.session_state:
    st.session_state.username = ""

if "documents" not in st.session_state:
    st.session_state.documents = []

# Sidebar for username input and file upload
with st.sidebar:
    st.session_state.username = st.text_input('Username (Required)', st.session_state.username)

    if not st.session_state.username:
        st.warning("Please enter your username to start the conversation.")
    else:
        uploaded_files = st.file_uploader("Upload your documents", type=["pdf", "txt"], accept_multiple_files=True)

        # Check if files are uploaded
        if uploaded_files:
            st.session_state.documents.extend(process_uploaded_files(uploaded_files))  # Use the utility function

            # Show a success message after processing each file
            st.success(f"Successfully uploaded and processed {len(uploaded_files)} file(s).")

# Ensure the user has provided a username
if not st.session_state.username:
    st.stop()

# Use the username as the thread_id for tracking
thread = {'configurable': {'thread_id': st.session_state.username}}
study_agent = study_agent_graph
documents = st.session_state.documents

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input for the chat
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Run the agent and display the assistant's response
    with st.chat_message("assistant"):
        response = study_agent.invoke(
            input={'username': st.session_state.username, 'messages': HumanMessage(content=prompt), 'session_docs': documents}, 
            config=thread
        )
        st.write(response["messages"][-1].content)
        
    st.session_state.messages.append({"role": "assistant", "content": response["messages"][-1].content})
