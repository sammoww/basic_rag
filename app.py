import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from vector_store import get_vector_store
import langchain

# Load environment variables
load_dotenv()

# Turn off verbose debug mode for a cleaner terminal
langchain.debug = False

# --- Page Config ---
st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 RAG Chatbot")
st.write("Ask me questions about the documents I have ingested!")

# --- Setup Core Components ---
@st.cache_resource
def get_core_components():
    """Initializes and caches the heavy components (retriever and LLMs)."""
    try:
        vector_store = get_vector_store()
        retriever = vector_store.as_retriever(search_kwargs={"k": 2})
        
        gemini_llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0.3, max_retries=1)
        groq_llm = ChatGroq(model_name="llama3-8b-8192", temperature=0.3, max_retries=1)
        llm_with_fallback = gemini_llm.with_fallbacks([groq_llm])
        
        return retriever, llm_with_fallback
    except Exception as e:
        st.error(f"Error initializing database: {e}\nDid you run `python vector_store.py` first?")
        return None, None

retriever, llm = get_core_components()

# --- Sidebar Toggle ---
with st.sidebar:
    st.header("⚙️ Settings")
    strict_rag_mode = st.toggle(
        "Strict RAG Mode", 
        value=True, 
        help="If ON, the AI only answers based on documents. If OFF, it will use general knowledge when documents don't have the answer."
    )

# --- Build Chain Dynamically ---
if retriever and llm:
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
        
    if strict_rag_mode:
        # The strict system prompt we used before
        template = """Answer the question based ONLY on the following context.
If you cannot answer the question with the context, please state that you don't know.

Context:
{context}

Question: {question}
"""
    else:
        # A relaxed system prompt
        template = """You are a helpful AI assistant. Use the following context to help answer the question. 
If the context doesn't contain the answer, use your own general knowledge to answer it.

Context:
{context}

Question: {question}
"""
    
    prompt = ChatPromptTemplate.from_template(template)
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
else:
    rag_chain = None

# --- Chat UI ---
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a question about RAG..."):
    # Log the user's question to the backend terminal
    print(f"\n[BACKEND LOG] User asked: {prompt}")
    
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate assistant response
    if rag_chain:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = rag_chain.invoke(prompt)
                    
                    # Log the AI's response to the backend terminal
                    print(f"[BACKEND LOG] AI replied: {response}\n{'-'*40}")
                    
                    st.markdown(response)
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    print(f"[BACKEND LOG] Error: {e}")
                    st.error(f"Failed to generate response: {e}")
