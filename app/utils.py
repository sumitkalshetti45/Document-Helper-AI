from app.llm_setup import llm
from app.memory import memory
from app.rag_setup import retrive
from langchain.prompts import ChatPromptTemplate

# ----------------------
# Function to generate summary
# ----------------------
def set_summary(text: str) -> str:
    """
    Generate a concise summary of the uploaded document text.
    """
    prompt = ChatPromptTemplate.from_template("""
    Summarize the following document in 3–5 sentences. 
    Focus on the key topic, purpose, and important details.

    Document:
    {document}
    Summary:
    """)
    
    formatted_prompt = prompt.format_messages(document=text[:4000])
    summary = llm(formatted_prompt).content
    return summary.strip()


# ----------------------
# Function to generate response
# ----------------------
def generate_response(query, vectorstore, doc_summary=None):
    """
    Generate a response for the user query.
    Uses document summary for general 'file about' questions, otherwise RAG retrieval.
    """
    # Check if the query is about the whole document
    if any(phrase in query.lower() for phrase in [
        "what is this file about",
        "what is this document about",
        "summary of this file",
        "tell me about this file"
    ]):
        if doc_summary:
            return f"This document is about: {doc_summary}"
        else:
            return "I don’t know what this file is about yet."

    # Normal RAG flow
    context_docs = retrive(query, vectorstore)
    context = "\n".join([doc.page_content for doc in context_docs])

    prompt = ChatPromptTemplate.from_template("""
    You are an AI assistant. Use the provided context and chat history to answer the user's question.
    If the answer is not in the context, say "I couldn't find this in documents".

    Chat History:
    {chat_history}
    Context:
    {context}
    Question:
    {question}
    Answer:
    """)

    formatted_prompt = prompt.format_messages(
        chat_history=memory.load_memory_variables({})["chat_history"],
        context=context,
        question=query
    )

    response = llm(formatted_prompt).content
    memory.save_context({"input": query}, {"output": response})
    return response
