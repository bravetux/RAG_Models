# RAG_Models
Rag Models

# Assignment 1: RAG PDF Summarizer

A Python application that summarizes PDF documents using Retrieval-Augmented Generation (RAG). It leverages **LangChain** for orchestration, **ChromaDB** for vector storage, and **Ollama** for local LLM inference.

## Prerequisites

1.  **Python 3.12+** installed.
2.  **Ollama** installed and running.
    *   Download from [ollama.com](https://ollama.com/).
    *   Pull the model used in the script (default is `deepseek-r1:1.5b`):
        ```bash
        ollama pull deepseek-r1:1.5b
        ```
    *   *Note: You can change the model in `summarize_pdf.py` by modifying the `MODEL_NAME` variable.*

## Installation

1.  Clone the repository (or navigate to the project directory).
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### 1. Generate a Dummy PDF (Optional)
If you don't have a PDF to test with, you can generate a sample one:
```bash
python create_dummy_pdf.py
```
This will create `sample.pdf` in your current directory.

### 2. Run the Summarizer
Run the script providing the path to your PDF file:
```bash
python summarize_pdf.py path/to/your/document.pdf
```

**Example:**
```bash
python summarize_pdf.py sample.pdf
```

## How It Works

1.  **Load**: The PDF is loaded using `PyPDFLoader`.
2.  **Split**: The text is split into chunks using `RecursiveCharacterTextSplitter`.
3.  **Embed**: Chunks are embedded using `OllamaEmbeddings` and stored in a temporary `Chroma` vector store.
4.  **Retrieve**: The system retrieves relevant chunks based on the query "Summarize the main points of this document...".
5.  **Generate**: The retrieved context is passed to the Ollama LLM to generate the final summary.

## Troubleshooting

-   **Import Errors**: If you see `ModuleNotFoundError: No module named 'langchain.chains'`, ensure you have installed the specific versions listed in `requirements.txt`. This project uses LangChain 0.1.x syntax.
-   **Ollama Connection**: Ensure Ollama is running (`ollama serve`) and the specified model is pulled.

# Other Assignments

Assignment 2:
write a python program to find similar audio files to the one you upload. Store many audio files and compare the one you upload with the stored ones. Using torchaudio framework or any other appropriate framework
 
Assignment 3:
create a translator app which takes your voice/speech as an input 
(in the language you have selected, give 5 language choices) convert it to speech in the language you selected as output (in the output also give 5 language choices)
 
Assignment 4:
create a toolchain with LLM, langchain and nosql database such as mongodb or redis and upload your information on to the nosql database and query it through an LLM

--
 
Consider doing any one of the below two as a capstone project
 
capstone project 1:
==================
problem statement:

Construct a RAG agent using python programming, any open source LLM, sentence transformer for embeddings and an open source vector db. The upload the embeddings on to the vector db.
 
1. Connect to SQLite for storing the summary from LLM
2. Take the summary and send it as a message to your WhatsApp
3. Take the summary and send it as a text message to your phone
4. Take the summary and send it to your email 
5. Take the summary and shorten the summary to 280 characters 
   and post it on your on your twitter handle
 
 
capstone project 2:
==================
problem statement:
 
Download Ollama or LM Studio or GPT4all and install on your desktop. Take any private document you have (a pdf or text) and convert it to embeddings (using sentence transformers or any other way) and store the embeddings on to the local vector db, consider chromadb.
 
Then, using python program, build a RAG agent that connects to the desktop LLM, vector db and langchain and a prompt from the user. 
Then user queries specific information from the document, and the RAG agent returns the answer
