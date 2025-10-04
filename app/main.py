from fastapi import FastAPI
from app.utils import generate_response
from app.graph_setup import graph
from app.rag_setup import setup_chroma

app = FastAPI()
vectorstore = None

@app.on_event("startup")
async def startup_event():
    global vectorstore
    vectorstore = setup_chroma(["data/sample.txt"])  # preload sample doc

@app.post("/chat")
async def chat(user_query: str):
    global vectorstore
    graph.transition("ask_question")
    response = generate_response(user_query, vectorstore)
    graph.transition("answer_question")
    return {"response": response}
