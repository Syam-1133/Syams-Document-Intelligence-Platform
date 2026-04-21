"""
LLM and Document Processing Service
"""
import time
import streamlit as st
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS

from config.settings import GROQ_API_KEY, LLM_MODEL, LLM_TEMPERATURE, CHUNK_SIZE, CHUNK_OVERLAP, BATCH_SIZE, SEPARATORS, RETRIEVAL_K
from config.prompts import DOCUMENT_ANALYSIS_PROMPT
from utils.document_loader import load_uploaded_documents, load_documents_from_directory

@st.cache_resource
def get_llm():
    """Initialize and cache LLM"""
    try:
        return ChatGroq(groq_api_key=GROQ_API_KEY, model=LLM_MODEL, temperature=LLM_TEMPERATURE)
    except Exception as e:
        st.error(f"Error initializing Groq LLM: {str(e)}")
        return None

def create_vector_embedding_from_files(uploaded_files=None):
    """Create vector embeddings from uploaded files or existing documents"""
    try:
        # Create progress containers
        progress_container = st.container()
        status_container = st.container()
        metrics_container = st.container()
        
        with progress_container:
            st.markdown("### 📊 Document Processing Progress")
            progress_bar = st.progress(0)
            status_text = st.empty()
            time_elapsed = st.empty()
            
        start_time = time.time()
        
        # Step 1: Load documents
        status_text.text("📄 Loading documents...")
        progress_bar.progress(10)
        
        if uploaded_files:
            # Use uploaded files
            docs = load_uploaded_documents(uploaded_files)
            source_type = "uploaded files"
        else:
            # Use existing research_papers directory
            docs = load_documents_from_directory()
            source_type = "research_papers directory"
        
        if not docs:
            st.error("❌ No documents found or could be loaded!")
            return False
        
        st.info(f"📑 Loaded {len(docs)} documents from {source_type}")
        
        # Step 2: Initialize embeddings
        status_text.text("🔧 Initializing OpenAI embeddings...")
        progress_bar.progress(30)
        
        embeddings = OpenAIEmbeddings(
            chunk_size=1000,
            max_retries=3
        )
        
        # Step 3: Split documents
        status_text.text("✂️ Processing and splitting documents into chunks...")
        progress_bar.progress(50)
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=SEPARATORS
        )
        
        final_documents = text_splitter.split_documents(docs)
        
        if not final_documents:
            st.error("❌ No text could be extracted from the documents!")
            return False
        
        st.info(f"📑 Created {len(final_documents)} text chunks")
        
        # Step 4: Create vector store
        status_text.text("🔍 Creating vector database (this may take a moment)...")
        progress_bar.progress(70)
        
        # Process in batches
        vectors = None
        
        for i in range(0, len(final_documents), BATCH_SIZE):
            batch = final_documents[i:i+BATCH_SIZE]
            if vectors is None:
                vectors = FAISS.from_documents(batch, embeddings)
            else:
                batch_vectors = FAISS.from_documents(batch, embeddings)
                vectors.merge_from(batch_vectors)
            
            progress = 70 + (25 * (i + BATCH_SIZE) / len(final_documents))
            progress_bar.progress(min(95, int(progress)))
            
            # Update time
            elapsed = time.time() - start_time
            time_elapsed.text(f"⏱️ Time elapsed: {elapsed:.1f} seconds")
        
        st.session_state.vectors = vectors
        st.session_state.final_documents = final_documents
        st.session_state.document_source = source_type
        
        progress_bar.progress(100)
        status_text.text("✅ Vector database created successfully!")
        
        total_time = time.time() - start_time
        
        # Display metrics
        with metrics_container:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Documents Processed", len(docs))
            with col2:
                st.metric("Text Chunks Created", len(final_documents))
            with col3:
                st.metric("Processing Time", f"{total_time:.1f}s")
        
        return True
        
    except Exception as e:
        st.error(f"❌ Error creating vector embeddings: {str(e)}")
        return False

def process_query(user_prompt):
    """Process user query and return response"""
    try:
        with st.spinner("🔍 Searching through documents and generating response..."):
            llm = get_llm()
            if llm is None:
                return None, 0
            
            # Create retriever
            retriever = st.session_state.vectors.as_retriever(
                search_type="similarity",
                search_kwargs={"k": RETRIEVAL_K}
            )
            
            # Get relevant documents
            docs = retriever.invoke(user_prompt)
            
            # Format context
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Create chain with LCEL
            chain = (
                {"context": lambda x: context, "input": RunnablePassthrough()}
                | DOCUMENT_ANALYSIS_PROMPT
                | llm
                | StrOutputParser()
            )
            
            # Process query
            start_time = time.time()
            answer = chain.invoke(user_prompt)
            end_time = time.time()
            
            # Return in expected format
            response = {
                "answer": answer,
                "context": docs
            }
            
            return response, end_time - start_time
            
    except Exception as e:
        st.error(f"❌ Error processing query: {str(e)}")
        return None, 0

def process_query_streaming(user_prompt):
    """Stream LLM response token by token (real-time responses)"""
    try:
        llm = get_llm()
        if llm is None:
            st.error("❌ LLM not initialized")
            return

        # Check if vector store exists
        if "vectors" not in st.session_state:
            st.error("❌ No documents loaded. Please process documents first.")
            return

        # Create retriever
        retriever = st.session_state.vectors.as_retriever(
            search_type="similarity",
            search_kwargs={"k": RETRIEVAL_K}
        )

        # Get relevant documents
        try:
            docs = retriever.invoke(user_prompt)
        except Exception as e:
            st.error(f"❌ Error retrieving documents: {str(e)}")
            return

        if not docs:
            st.warning("⚠️ No relevant documents found for this query.")
            return

        # Format context
        context = "\n\n".join([doc.page_content for doc in docs])

        # Create chain with LCEL
        chain = (
            {"context": lambda x: context, "input": RunnablePassthrough()}
            | DOCUMENT_ANALYSIS_PROMPT
            | llm
            | StrOutputParser()
        )

        # Stream the response token by token
        accumulated_response = ""
        token_count = 0

        try:
            for token in chain.stream(user_prompt):
                if token:  # Only yield non-empty tokens
                    accumulated_response += token
                    token_count += 1
                    yield token, accumulated_response, docs

            # Yield final response with timing
            yield None, accumulated_response, docs  # None indicates stream complete

        except Exception as e:
            st.error(f"❌ Error during streaming: {str(e)}")
            yield None, accumulated_response, docs  # Return what we have so far

    except Exception as e:
        st.error(f"❌ Error in streaming query: {str(e)}")
        return
