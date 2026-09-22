# RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot project.

## Overview
This project aims to build an AI chatbot that grounds its responses in custom data using RAG techniques.

## Tech Stack
- **Language:** Python
- **Vector Database:** FAISS
- **Framework:** LangChain
- **LLMs:** Google Gemini (Primary) and Groq (Fallback)
- **Frontend:** Streamlit

## Setup
1. Create a virtual environment: `python -m venv venv`
2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up your `.env` file with necessary API keys:
   ```env
   GOOGLE_API_KEY="your_google_api_key_here"
   GROQ_API_KEY="your_groq_api_key_here"
   ```

## Usage
1. Ingest data: `python vector_store.py`
2. Start the web interface: `streamlit run app.py`
