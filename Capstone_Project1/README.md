# RAG Agent with Multi-Channel Notifications

A Retrieval Augmented Generation (RAG) system that answers queries based on uploaded documents and distributes summaries via Email, SMS, WhatsApp, and Twitter.

## Features
- **RAG Architecture**: Uses `LangChain`, `ChromaDB`, and `SentenceTransformers`.
- **LLM Support**: Supports **Ollama** (default) and **LM Studio**.
- **Storage**: Archives all summaries in SQLite.
- **Notifications**: Modular integration for:
    - Email (SMTP)
    - SMS & WhatsApp (Twilio)
    - Twitter/X (Tweepy)

## Setup

1.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configuration**
    Copy `.env.example` to `.env` and configure your keys.
    ```bash
    cp .env.example .env
    ```
    - For **Ollama**, make sure `ollama serve` is running.
    - For **LM Studio**, start the server on port 1234.

## Usage

### 1. Ingest Data
Load text into the vector database.
```bash
python main.py --ingest sample.txt
```

### 2. Query & Notify
Ask a question and send the summary to specific channels.
```bash
python main.py --query "What is LangChain?" --notify email,sms --email ic19939@gmail.com --phone +919444530846
```
*Note: Without valid API keys in `.env`, the system will MOCK the notification (print success to console).*

### 3. Check Database
Summaries are stored in `summary_store.db`.

## Project Structure
- `main.py`: Entry point.
- `rag_engine.py`: RAG logic.
- `notifications.py`: Notification services.
- `db_manager.py`: Database operations.
- `design.md`: Architecture details.
