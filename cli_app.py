import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from vector_store import get_vector_store

# Load API keys
load_dotenv()

def main():
    print("\n" + "="*40)
    print("🤖 Welcome to the RAG CLI Chatbot!")
    print("="*40)
    print("Initializing database...\n")
    
    try:
        vector_store = get_vector_store()
        retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    except Exception as e:
        print(f"Error loading FAISS database: {e}")
        print("Did you run `python vector_store.py` to ingest data first?")
        return
        
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
        
    # Setup LLMs
    gemini_llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0.3, max_retries=1)
    groq_llm = ChatGroq(model_name="llama3-8b-8192", temperature=0.3, max_retries=1)
    llm_with_fallback = gemini_llm.with_fallbacks([groq_llm])
    
    # Prompt template
    template = """Answer the question based ONLY on the following context.
If you cannot answer the question with the context, please state that you don't know.

Context:
{context}

Question: {question}
"""
    prompt = ChatPromptTemplate.from_template(template)
    
    # Build chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm_with_fallback
        | StrOutputParser()
    )
    
    print("✅ Ready! You can start asking questions.")
    print("Type 'exit' or 'quit' to stop.\n")
    
    # Interactive chat loop
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
            
        if not user_input.strip():
            continue
            
        print("🤖 Bot is thinking...")
        try:
            response = rag_chain.invoke(user_input)
            print(f"🤖 Bot: {response}\n")
        except Exception as e:
            print(f"🤖 Bot [Error]: {e}\n")

if __name__ == "__main__":
    main()
