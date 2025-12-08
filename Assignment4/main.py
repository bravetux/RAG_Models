import argparse
import os
import sys
from dotenv import load_dotenv
from database import MongoDBHandler
from llm_chain import LLMChainHandler

# Load env variables from .env file
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Toolchain: Upload to MongoDB & Query with LLM")
    parser.add_argument("--upload", type=str, help="Text content to upload to MongoDB")
    parser.add_argument("--query", type=str, help="Question to ask the LLM")
    parser.add_argument("--list", action="store_true", help="List recent documents from DB")
    
    args = parser.parse_args()

    # Initialize Database
    try:
        db = MongoDBHandler()
    except Exception as e:
        print(f"CRITICAL: Could not connect to MongoDB. Ensure it is running.\nDetails: {e}")
        sys.exit(1)

    # Handle Upload
    if args.upload:
        print(f"Uploading content: '{args.upload}'...")
        doc_id = db.insert_document(args.upload)
        print(f"Successfully uploaded. Document ID: {doc_id}")
        return

    # Handle List
    if args.list:
        docs = db.retrieve_documents(limit=5)
        print("\n--- Recent Documents ---")
        for doc in docs:
            print(f"ID: {doc.get('_id')} | {doc.get('timestamp')}")
            print(f"Content: {doc.get('content')}")
            print("-" * 20)
        return

    # Handle Query
    if args.query:
        print(f"Querying LLM: '{args.query}'...")
        
        # 1. Retrieve Context
        # (For this assignment, we fetch recent documents as context. 
        # In a full RAG, we would use embeddings search.)
        context_docs = db.retrieve_documents(limit=5) 
        
        if not context_docs:
            print("Warning: No documents found in database to provide as context.")
        
        # 2. Initialize LLM Chain
        try:
            chain = LLMChainHandler()
        except Exception as e:
            print(f"Error initializing LLM Chain: {e}")
            sys.exit(1)
            
        # 3. Get Answer
        answer = chain.query(args.query, context_docs)
        
        print("\n=== LLM Response ===")
        print(answer)
        print("====================")
        return

    # If no arguments
    parser.print_help()

if __name__ == "__main__":
    main()
