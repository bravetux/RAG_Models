import chromadb
import uuid

class AudioVectorDB:
    def __init__(self, collection_name="audio_embeddings", persist_directory="./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_audio(self, embedding, metadata):
        """
        Adds an audio embedding to the database.
        metadata should include 'filename', 'path', etc.
        """
        audio_id = str(uuid.uuid4())
        self.collection.add(
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[audio_id]
        )
        return audio_id

    def query_audio(self, embedding, n_results=5):
        """
        Queries the database for similar audio files.
        """
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=n_results
        )
        return results
