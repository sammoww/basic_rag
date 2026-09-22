import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from vector_store import get_vector_store

# Load environment variables
load_dotenv()

def format_docs(docs):
    """Formats retrieved documents into a single string context."""
    return "\n\n".join(doc.page_content for doc in docs)

def main():
    print("Welcome to the RAG Chatbot!")
    
    # 1. Initialize Vector Store and Retriever
    # Note: Make sure to run `python vector_store.py` first to ingest data!
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    
    # 2. Define the LLMs with Fallback
    gemini_llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash", 
        temperature=0.3,
        max_retries=1
    )
    
    groq_llm = ChatGroq(
        model_name="llama3-8b-8192", 
        temperature=0.3,
        max_retries=1
    )
    
    llm_with_fallback = gemini_llm.with_fallbacks([groq_llm])
    
    # 3. Create the RAG Prompt
    template = """Answer the question based ONLY on the following context.
If you cannot answer the question with the context, please state that you don't know.

Context:
{context}

Question: {question}
"""
    prompt = ChatPromptTemplate.from_template(template)
    
    # 4. Build the RAG Chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm_with_fallback
        | StrOutputParser()
    )
    
    # 5. Test the RAG Chain
    print("\n--- Testing RAG Pipeline ---")
    question = "What is RAG and how does it reduce hallucinations?"
    print(f"Question: {question}")
    
    try:
        print("Retrieving context and generating answer...")
        response = rag_chain.invoke(question)
        print(f"\nAnswer:\n{response}")
    except Exception as e:
        print(f"\n[Error] Pipeline failed. Error details:\n{e}")
        print("\nHint: Did you forget to set your API keys or run `python vector_store.py` to ingest the sample data?")

if __name__ == "__main__":
    main()
