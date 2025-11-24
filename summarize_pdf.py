import argparse
import os
import sys
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

# Configuration
MODEL_NAME = "deepseek-r1:1.5b" # Using available model
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def load_and_split_pdf(file_path):
    """Loads a PDF and splits it into chunks."""
    print(f"Loading PDF: {file_path}...")
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        sys.exit(1)
        
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    print(f"Splitting document...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, 
        chunk_overlap=CHUNK_OVERLAP
    )
    splits = text_splitter.split_documents(docs)
    print(f"Created {len(splits)} chunks.")
    return splits

def setup_vectorstore(splits):
    """Sets up the Chroma vector store with Ollama embeddings."""
    print("Initializing Vector Store (ChromaDB) with Ollama Embeddings...")
    embeddings = OllamaEmbeddings(model=MODEL_NAME)
    
    # Create a temporary vector store in memory for this run
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings
    )
    return vectorstore

def summarize_doc(vectorstore):
    """Runs the summarization chain."""
    print(f"Initializing RAG chain with model: {MODEL_NAME}...")
    llm = ChatOllama(model=MODEL_NAME)
    
    # Define the prompt for summarization
    prompt = ChatPromptTemplate.from_template("""
    Answer the following question based only on the provided context:

    <context>
    {context}
    </context>

    Question: {input}
    """)

    # Create the chain
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vectorstore.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    print("Generating summary...")
    response = retrieval_chain.invoke({"input": "Summarize the main points of this document in a concise paragraph."})
    
    return response["answer"]

def main():
    parser = argparse.ArgumentParser(description="Summarize a PDF using RAG with Ollama and ChromaDB.")
    parser.add_argument("file_path", help="Path to the PDF file to summarize")
    args = parser.parse_args()

    splits = load_and_split_pdf(args.file_path)
    vectorstore = setup_vectorstore(splits)
    summary = summarize_doc(vectorstore)
    
    print("\n--- SUMMARY ---\n")
    print(summary)
    print("\n---------------")

if __name__ == "__main__":
    main()
