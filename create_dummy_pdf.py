from reportlab.pdfgen import canvas

def create_dummy_pdf(filename):
    c = canvas.Canvas(filename)
    c.drawString(100, 750, "RAG PDF Summarization Test Document")
    c.drawString(100, 730, "This is a sample PDF created to test the RAG summarization capabilities.")
    c.drawString(100, 710, "Retrieval-Augmented Generation (RAG) is a technique for enhancing the accuracy and reliability of generative AI models with facts fetched from external sources.")
    c.drawString(100, 690, "In this example, we are using LangChain, ChromaDB, and Ollama.")
    c.drawString(100, 670, "LangChain provides the framework, ChromaDB acts as the vector store, and Ollama runs the local LLM.")
    c.drawString(100, 650, "The goal is to summarize this content effectively.")
    c.save()
    print(f"Created {filename}")

if __name__ == "__main__":
    create_dummy_pdf("sample.pdf")
