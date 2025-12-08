# Audio Similarity Search

This project implements an improved audio similarity search tool using Python. It allows you to store audio embeddings in a vector database and search for similar audio files based on their content.

## Features

- **Audio Embedding:** Uses a pre-trained `Wav2Vec2` model (local) to generate embeddings for audio files.
- **Vector Database:** Utilizes `ChromaDB` for efficient storage and retrieval of high-dimensional audio embeddings.
- **Similarity Search:** Finds the most similar audio files to a given query audio file.
- **CLI Interface:** Provides a simple command-line interface for adding folders and searching files.
- **Flexible Models:** Supports switching between a local Wav2Vec2 model and a mock remote model (extensible for real APIs).

## Prerequisites

- Python 3.8+
- [FFmpeg](https://ffmpeg.org/) (required by `torchaudio` for loading audio files)

## Installation

1.  **Clone the repository** (if applicable) or navigate to the project directory:
    ```bash
    cd C:\Users\vigne\Downloads\Projects\antigravity_google\Assignment2
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The application is run via `main.py`.

### 1. Add Audio Files to Database

To index audio files, provide the path to a folder containing `.wav` or `.mp3` files.

```bash
python main.py add <path_to_audio_folder> --model local
```

*   `folder`: Path to the directory containing your audio files.
*   `--model`: Optional. `local` (default) or `remote`.

### 2. Search for Similar Audio

To find similar audio files, provide the path to a query audio file.

```bash
python main.py search <path_to_query_file> --model local
```

*   `file`: Path to the audio file you want to find matches for.
*   `--model`: Optional. `local` (default) or `remote`.

## Project Structure

*   `main.py`: The entry point for the CLI application. Handles argument parsing and orchestrates the flow.
*   `audio_processor.py`: Handles loading and preprocessing of audio files (resampling, normalization).
*   `embedding_model.py`: Contains classes for generating embeddings (`LocalWav2Vec2Model`, `RemoteMockModel`).
*   `vector_db.py`: Manages the ChromaDB connection, and adding/querying audio embeddings.
*   `test_similarity.py`: A script for testing the similarity functionality.
*   `requirements.txt`: List of Python dependencies.

## Key Technologies

*   **TorchAudio:** For audio loading and manipulation.
*   **Transformers (Hugging Face):** For the pre-trained Wav2Vec2 model.
*   **ChromaDB:** As the vector database for embedding storage.
*   **NumPy/SciPy:** For numerical operations.
