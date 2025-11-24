import sys
import os
print("Python executable:", sys.executable)
print("Current working directory:", os.getcwd())
print("Path:", sys.path)

try:
    import langchain
    print("LangChain version:", langchain.__version__)
    print("LangChain file:", langchain.__file__)
    import langchain.chains
    print("LangChain chains imported successfully")
except ImportError as e:
    print("ImportError:", e)
except Exception as e:
    print("Error:", e)
