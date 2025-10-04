import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

def load_docs(doc_paths):
    docs = []
    for path in doc_paths:
        ext = os.path.splitext(path)[-1].lower()
        if ext == ".txt":
            loader = TextLoader(path)
        elif ext == ".pdf":
            loader = PyPDFLoader(path)
        else:
            continue
        docs.extend(loader.load())
    return docs

def setup_chroma(doc_paths):
    docs = load_docs(doc_paths)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(chunks, embedding=embeddings, persist_directory="chroma_store")
    return vectorstore

def retrive(query, vectorstore, k=3):
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    return retriever.get_relevant_documents(query)
