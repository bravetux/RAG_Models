# Design and Verification Process

This document outlines the architectural design choices and the verification steps undertaken to build the RAG-based PDF Summarizer.

## 1. Design

### 1.1 Architecture
The application follows a standard **Retrieval-Augmented Generation (RAG)** pipeline:

1.  **Document Loading**: The PDF is ingested into the system.
2.  **Splitting**: The text is broken down into manageable chunks to fit within the context window of the embedding model and LLM.
3.  **Embedding**: Text chunks are converted into vector representations.
4.  **Storage**: Vectors are stored in a vector database for efficient similarity search.
5.  **Retrieval**: The system searches for chunks relevant to the user's query (in this case, a summarization prompt).
6.  **Generation**: The LLM generates a summary based on the retrieved context.

### 1.2 Component Selection

| Component | Choice | Rationale |
| :--- | :--- | :--- |
| **Orchestration** | **LangChain** | Provides a robust framework for chaining LLM components and managing the RAG flow. |
| **LLM & Embeddings** | **Ollama** | Allows for local, private, and cost-effective inference. Selected model: `deepseek-r1:1.5b` (flexible). |
| **Vector Store** | **ChromaDB** | A lightweight, open-source vector database that runs locally and integrates well with LangChain. |
| **PDF Loader** | **PyPDF** | A reliable standard library for parsing PDF files in Python. |

### 1.3 Implementation Details
-   **Chunking Strategy**: Used `RecursiveCharacterTextSplitter` with a chunk size of 1000 and overlap of 200. This ensures context is preserved across chunk boundaries.
-   **Dependency Management**: Due to recent breaking changes in LangChain's ecosystem (splitting into `langchain-core`, `langchain-community`, etc.), we pinned the versions to a stable 0.1.x release set (`langchain==0.1.20`) to ensure compatibility with standard import paths.

## 2. Verification Process

The verification process involved unit testing the components and integration testing the full pipeline.

### 2.1 Test Data Generation
To ensure a controlled testing environment, we created a utility script `create_dummy_pdf.py`.
-   **Action**: Generated `sample.pdf` using `reportlab`.
-   **Content**: A simple paragraph explaining RAG, ensuring we knew exactly what the summary should contain.

### 2.2 Integration Testing & Debugging
We encountered and resolved several issues during the implementation phase:

1.  **Initial Attempt (Latest LangChain)**:
    -   *Issue*: `ModuleNotFoundError: No module named 'langchain.chains'` and other import errors.
    -   *Cause*: Recent major version updates in LangChain (0.2.x/0.3.x) have reorganized the package structure, causing compatibility issues with some community integrations and standard import patterns.
    -   *Action*: Attempted to upgrade/reinstall, but issues persisted due to package shadowing.

2.  **Resolution (Downgrade)**:
    -   *Action*: Downgraded to a known stable configuration:
        -   `langchain==0.1.20`
        -   `langchain-community==0.0.38`
    -   *Result*: Imports worked correctly.

3.  **Final Verification Run**:
    -   *Command*: `python summarize_pdf.py sample.pdf`
    -   *Observation*:
        -   PDF loaded successfully.
        -   Split into 1 chunk (correct for the small sample).
        -   ChromaDB initialized.
        -   Ollama (DeepSeek) generated a concise summary.
    -   *Output*: "The document explains that Retrieval-Augmented Generation (RAG) enhances generative AI..." (Matches expected content).

### 2.3 Conclusion
The system is verified to work with the specified dependencies and local Ollama setup. The `requirements.txt` file has been updated to reflect the specific versions required to reproduce this successful run.
