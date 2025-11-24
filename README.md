# RAG PDF Summarizer

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
