import argparse
import os
import glob
from audio_processor import AudioProcessor
from embedding_model import LocalWav2Vec2Model, RemoteMockModel
from vector_db import AudioVectorDB

def get_model(model_type):
    if model_type == 'local':
        return LocalWav2Vec2Model()
    elif model_type == 'remote':
        return RemoteMockModel()
    else:
        raise ValueError("Invalid model type. Choose 'local' or 'remote'.")

def add_folder(folder_path, model_type):
    print(f"Adding audio files from {folder_path} using {model_type} model...")
    processor = AudioProcessor()
    model = get_model(model_type)
    db = AudioVectorDB()

    # Find all wav and mp3 files
    files = glob.glob(os.path.join(folder_path, "*.wav")) + glob.glob(os.path.join(folder_path, "*.mp3"))
    
    if not files:
        print("No audio files found in the specified folder.")
        return

    for file_path in files:
        print(f"Processing {file_path}...")
        waveform = processor.load_and_preprocess(file_path)
        if waveform is not None:
            embedding = model.get_embedding(waveform)
            db.add_audio(embedding, {"path": file_path, "filename": os.path.basename(file_path)})
            print(f"Added {file_path} to database.")

def search_file(file_path, model_type):
    print(f"Searching for similar files to {file_path} using {model_type} model...")
    processor = AudioProcessor()
    model = get_model(model_type)
    db = AudioVectorDB()

    waveform = processor.load_and_preprocess(file_path)
    if waveform is None:
        print("Failed to process input file.")
        return

    embedding = model.get_embedding(waveform)
    results = db.query_audio(embedding)

    print("\nSearch Results:")
    if results['metadatas'] and results['metadatas'][0]:
        for i, metadata in enumerate(results['metadatas'][0]):
            distance = results['distances'][0][i] if 'distances' in results else "N/A"
            print(f"{i+1}. {metadata['filename']} (Path: {metadata['path']}) - Distance: {distance}")
    else:
        print("No results found.")

def main():
    parser = argparse.ArgumentParser(description="Audio Similarity Search")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add audio files from a folder to the database")
    add_parser.add_argument("folder", help="Path to the folder containing audio files")
    add_parser.add_argument("--model", choices=['local', 'remote'], default='local', help="Model to use for embeddings")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for similar audio files")
    search_parser.add_argument("file", help="Path to the audio file to search for")
    search_parser.add_argument("--model", choices=['local', 'remote'], default='local', help="Model to use for embeddings")

    args = parser.parse_args()

    if args.command == "add":
        add_folder(args.folder, args.model)
    elif args.command == "search":
        search_file(args.file, args.model)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
