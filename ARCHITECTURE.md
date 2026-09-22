# RAG Architecture & API Usage

The APIs you provided (Google Gemini and Groq) are the "brains" of this operation. They are used in two completely different places in our project.

Here is a diagram showing exactly how data flows and where the APIs are called:

```text
Phase 1: Data Ingestion (vector_store.py)
-----------------------------------------
[ data/sample.txt ]
       |
       v (1. Read File)
[ Text Splitter ]
       |
       v (2. Sends Text Chunks)
(( Google Gemini API - Embeddings Model ))  <-- API CALL
       |
       v (3. Returns Vectors)
[ FAISS Vector Database ]


Phase 2: Chatting (app.py)
--------------------------
[ User Question ]
       |
       v
[ Streamlit UI ]
       |
       v (1. Keyword/Vector Search)
[ FAISS Vector Database ]
       |
       v (2. Returns Relevant Context)
[ Prompt Template ]  <-- Merges Question + Context
       |
       v (3. Sends Question + Context)
(( Google Gemini API - Chat Model ))  <-- API CALL
       |
       v (If Gemini fails, fallback to Groq API)
[ Streamlit UI displays Final Answer ]
```

### Where exactly are the APIs used?

The pink boxes in the diagram show where your API keys are actively making network requests:

1. **When you run `vector_store.py` (The Embeddings API)**
   FAISS and Python don't understand English. To search through text, they need the text converted into math (vectors). 
   We send the raw text from `sample.txt` to Google's **Embedding API**. Google reads the text, turns it into a mathematical representation of the concepts, and sends that math back to us to store in FAISS.

2. **When you chat in `app.py` (The Chat API)**
   When you ask a question, our local code searches FAISS for matching text. Then, it takes your question AND the text it found, and bundles them into one massive prompt.
   It sends that massive prompt across the internet to Google's **Chat API** (Gemini 3.5 Flash). Gemini reads the context, figures out the answer, and sends the text response back to your Streamlit screen.
   *(And if Google's servers crash, LangChain automatically reroutes that exact same prompt to your Groq API key instead!)*
