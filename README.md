# RAG_Models
Rag Models
Assignment 1: 
Use any other open source model in place of openai and do the summarization of a pdf document using langchain and the concept of RAG. use chromadb vector database for this
 
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
