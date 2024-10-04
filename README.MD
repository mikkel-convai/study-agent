# Study Agent

The **Study Agent** is an AI-powered tool designed to help students learn more efficiently by providing personalized guidance and relevant study materials. By integrating **Retrieval-Augmented Generation (RAG)** capabilities and **student profiling**, the agent tailors responses and recommendations based on each student's learning needs and preferences.

## Get started
1. python -m venv .venv
2. Setup .env
3. pip install -r requirements
4. run sqlite3 students.db -init student_schema.sql

## Main Ideas
- **RAG Capabilities:** The agent uses document retrieval techniques to fetch relevant study materials and integrate them into responses, enhancing the learning experience with up-to-date and contextual information.
  
- **Student Profiling:** The agent dynamically builds and updates a personalized profile for each student, capturing details such as name, learning goals, and academic background. This profile helps the agent offer personalized feedback and suggestions.

- **SQL Database Integration:** Student profiles are stored in an SQLite database, allowing the agent to retain information across sessions. The database is regularly updated with new insights as students interact with the agent, ensuring the advice remains personalized and relevant.

## How It Works
- The agent begins by retrieving or creating a profile for each student based on their interactions.
- It then uses its RAG capabilities to retrieve documents or other resources relevant to the student's query.
- The student's profile is updated with new information, and the agent continuously adapts to the student's evolving needs.
- Finally, the agent answers questions, offering detailed explanations and personalized support.

## TODO
- Add in-memory rag capabilities back in
- Fine tune prompts
- Flesh out student profile
- Add evaluation
- Add Ollama option
- Add summarizer and handle message history

## Future features
- Calendar integration for study planning and time blocking
- Quiz/Flashcard maker
- Study planner, using curriculum