import streamlit as st
import os
import sys
from PyPDF2 import PdfReader
import pandas as pd

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) # Adjust the path as necessary

from app.rag_setup import setup_chroma
from app.utils import generate_response, set_summary

# Page config
st.set_page_config(page_title="Document Helper AI", page_icon="🤖", layout="wide")
st.title("🤖 Your AI Document Assistant")

# Initialize session state
if "chat_history" not in st.session_state: # Initialize chat history
    st.session_state.chat_history = []
if "doc_summary" not in st.session_state: # Initialize document summary
    st.session_state.doc_summary = None

# Sidebar: Upload Documents
st.sidebar.header("Upload Documents")
uploaded_files = st.sidebar.file_uploader(
    "Upload TXT or PDF files", accept_multiple_files=True, type=["txt", "pdf"]
)  # Allow multiple file uploads

# Sidebar: Clear chat history
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.chat_history = []
    st.sidebar.success("Chat history cleared!")
    
# Sidebar: Download chat history
if st.sidebar.button("💾 Download Chat"):
    if st.session_state.chat_history:
        df = pd.DataFrame(st.session_state.chat_history, columns=["Sender", "Message"])
        df.to_csv("chat_history.csv", index=False)
        st.sidebar.success("Chat history saved as chat_history.csv")
    else:
        st.sidebar.warning("No chat history to save!")

vectorstore = None # Initialize vectorstore

if uploaded_files:
    doc_paths = []
    all_text = ""
    os.makedirs("data", exist_ok=True) # Ensure data directory exists

    for uploaded_file in uploaded_files: # Process each uploaded file
        # Save uploaded file to data directory
        file_path = os.path.join("data", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer()) # getbuffer() for binary write 
        doc_paths.append(file_path)

        # Extract text for summary
        if uploaded_file.type == "text/plain":
            all_text += uploaded_file.getvalue().decode("utf-8") + "\n"  # Decode bytes to string
        elif uploaded_file.type == "application/pdf": # PDF file
            reader = PdfReader(file_path) # Read from saved file
            for page in reader.pages:
                all_text += page.extract_text() + "\n"  # Extract text from each page

    # Setup vectorstore (RAG)
    vectorstore = setup_chroma(doc_paths) # Create or update vectorstore with new documents

    # Generate & store summary in session state
    if all_text.strip():
        st.session_state.doc_summary = set_summary(all_text)

    st.sidebar.success("✅ Documents uploaded, processed & summarized!")
else:
    st.sidebar.info("Upload documents to start chatting.")

# Display chat history
for sender, message in st.session_state.chat_history:
    with st.chat_message("user" if sender == "You" else "assistant"):
        st.write(message)

# Chat input (always at the bottom)
if vectorstore:
    user_input = st.chat_input("Ask me anything about your uploaded documents...")

    if user_input:
        # Add user message
        st.session_state.chat_history.append(("You", user_input))
        with st.chat_message("user"):
            st.write(user_input)

        # Bot response with loading spinner
        with st.chat_message("assistant"):
            with st.spinner("Thinking... 🤔"):
                response = generate_response(
                    user_input,
                    vectorstore,
                    st.session_state.doc_summary
                )
            st.session_state.chat_history.append(("Bot", response))
            st.write(response)
else:
    st.info("👆 Upload documents first to start chatting.")
