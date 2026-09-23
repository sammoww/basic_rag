# Project Worklog

## 2026-09-17
### What was done
- Initialized project scaffolding (AGENTS.md, CLAUDE.md stub, README.md, .gitignore, and worklog.md) based on user's `/conductor: setup` request.

### What worked
- Basic empty structure established.

### What failed
- N/A yet.

## 2026-09-18
### What was done
- Decided on tech stack: Python, Chroma, and LangChain.
- Decided to use both Google Gemini and Groq with LangChain's Fallback mechanism to ensure high availability.
- Created `requirements.txt` and installed dependencies.
- Added `vector_store.py` for initializing FAISS DB and chunking/ingesting documents.
- Created `data/sample.txt` for testing ingestion.
- Updated `main.py` to run a full RAG chain (Retrieval-Augmented Generation) using the local FAISS store and the fallback LLMs.
- Created a `streamlit` web interface in `app.py` for a ChatGPT-like experience.
- Updated `README.md` and `.env.example` with setup instructions.

### What worked
- Initial scaffolding successfully built.

### What failed
- ChromaDB Rust backend threw access violation on Windows; resolved by migrating to FAISS.
- Deprecated Gemini 1.5 model name; resolved by migrating to Gemini 3.5 Flash.

## 2026-09-19
### What was done
- Added Strict RAG Mode vs General Knowledge toggle in `app.py` sidebar.
- Documented system prompt templates and how context injection works.
- Authored initial architecture diagrams (`ARCHITECTURE.md`).

### What worked
- Dynamic prompt switching in Streamlit.

## 2026-09-20
### What was done
- Created `architecture_diagram.html`: clean, responsive HTML visual breakdown with tabs.
- Created `pipeline_nodes.html`: comprehensive deep-dive mapping every file, function, class, and data input/output across the LangChain LCEL pipeline and text-splitting steps.
- Linked the two visual guides together.

### What worked
- High-clarity visual node cards for LangChain orchestration without brittle diagram dependencies.

## 2026-09-21
### What was done
- Authored `things_you_did_not_know_about_python.md` documenting:
  - Python module import mechanics and top-level execution side-effects.
  - The purpose of `if __name__ == "__main__":` in multi-use scripts.
  - FAISS architecture (in-memory embedded C++ library vs daemon DBs).
  - The dual-file indexing model (`index.faiss` vector matrix + `index.pkl` docstore map) and pickle security considerations.
  - Black-box ID lookup ("coat-check") mental model for vector-to-text resolution.

### What worked
- Detailed reference guide created for internal architectural clarity.

## 2026-09-22
### What was done
- Updated `.gitignore` to ensure `faiss_db/`, `chroma_db/`, and `*.log` are properly ignored alongside `.env` and `venv/`.
- Initialized local Git repository on `main` branch.
- Created initial Git commit for project files.
- Linked remote `origin` (`https://github.com/sammoww/basic_rag.git`) and pushed `main` branch with upstream tracking.
- Added Section 6 to `things_you_did_not_know_about_python.md` documenting Eager vs. Lazy Loading (`load()` vs. `lazy_load()`), Python generator lifecycle, Garbage Collection mechanics, and buffer/batch size controls.

### What worked
- Git initialized cleanly with all sensitive environment variables, virtual environments, and binary vector indices ignored.
- Initial code pushed successfully to GitHub repository.
- Expanded reference documentation with clear breakdowns of memory management in RAG ingestion pipelines.

## 2026-09-23
### What was done
- Added Section 7 to `things_you_did_not_know_about_python.md`: Detailed solutions for ingesting massive "pageless" `.txt` files (line/paragraph streaming, disk pre-splitting, memory mapping).
- Added Section 8 to `things_you_did_not_know_about_python.md`: Demystified Python OOP fundamentals (`class`, `__init__`, `self`, `yield` generator mechanics, and LangChain `BaseLoader` inheritance) with a mental model table and sequence diagram.

### What worked
- Reference guide extended with clean, separated topics for future review.
