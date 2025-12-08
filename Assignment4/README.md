# Toolchain Walkthrough: MongoDB + LangChain + LLM

This toolchain allows you to upload text to MongoDB and query it using a local or remote LLM.

## Prerequisites
1. **MongoDB**: Ensure MongoDB is running locally on port 27017.
2. **LLM Provider**:
    - **Ollama**: Ensure `ollama serve` is running.
    - **LM Studio / OpenAI**: Configure `.env`.

## Setup
1. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2. **Environment**:
    Copy `.env.example` to `.env` and adjust if needed (e.g., if using LM Studio).
    ```bash
    cp .env.example .env
    ```

## Usage

### 1. Upload Data
Store information (text) into the database.
```bash
python main.py --upload "Ollama is a tool for running LLMs locally."
```

### 2. Query Data
Ask a question. The system will retrieve recent context from MongoDB and answer.
```bash
python main.py --query "What is Ollama?"
```

### 3. List Data
See what's in the database.
```bash
python main.py --list
```

## Architecture
- **`database.py`**: Handles MongoDB connection and insertion/retrieval.
- **`llm_chain.py`**: Sets up the LangChain pipeline with the chosen provider.
- **`main.py`**: CLI entry point.
