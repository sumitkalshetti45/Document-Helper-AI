# AI Document Chatbot

## Project Overview

This project is an **AI-powered chatbot** that allows users to **upload PDF or TXT documents** and interact with them using **natural language queries**.  
It uses **Retrieval-Augmented Generation (RAG)** and a **language model** to answer questions based on document content.  

Users can also ask general questions like **“What is this file about?”** to get a summary of the uploaded documents. The chatbot **stores chat history**, supports **clearing data**, and allows **downloading the conversation**.  

This project is built with **Python**, **Streamlit**, and **LangChain**, making it a strong **resume-ready project** for AI and data enthusiasts.  

---

## Features

- Upload **PDF or TXT documents** for AI-based querying.  
- Automatic **document summary generation**.  
- **RAG-based question answering** for precise answers.  
- **Chat history** preserved during the session.  
- **Clear chat history and uploaded files** button for fresh start.  
- **Download chat history** as CSV.  
- User-friendly **Streamlit web interface** with loading spinners.  

---

## Folder Structure
ai_knowledge_assistant/
│
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app
│   ├── llm_setup.py     # LLM setup
│   ├── graph_setup.py   # LangGraph setup
│   ├── rag_setup.py     # Chroma embeddings + retrieval
│   └── utils.py         # Helper functions
│
├── data/                # Store your documents here
│   └── sample_doc.txt
├── .env                 # Environment variables
├── requirements.txt
└── README.md



## requiremnts
langchain
langgraph
tiktoken
chromadb
openai
pypdf
streamlit
python-dotenv
langchain_community
langchain_openai

## run app
uvicorn app.main:app --reload


## run frontend

streamlit run sapp.py