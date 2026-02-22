"""
Sidebar UI Component
"""
import streamlit as st
from datetime import datetime
from services.llm_service import create_vector_embedding_from_files

def render_sidebar():
    """Render the sidebar with system status and controls"""
    with st.sidebar:
        st.markdown("### 🏢 SYSTEM DASHBOARD")
        
        # System Status
        st.markdown("#### 📈 SYSTEM STATUS")
        if "vectors" in st.session_state:
            st.markdown(
                f'<div class="success-box">'
                f'<span class="status-indicator status-online"></span>'
                f'<strong>VECTOR DATABASE: ONLINE</strong><br>'
                f'Source: {st.session_state.document_source}'
                f'</div>', 
                unsafe_allow_html=True
            )
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<div class="metric-card">📄 Document Chunks<br><h3>{len(st.session_state.final_documents)}</h3></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric-card">🤖 Model<br><h3>Llama-3.1-8B</h3></div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="warning-box">'
                f'<span class="status-indicator status-offline"></span>'
                f'<strong>VECTOR DATABASE: OFFLINE</strong><br>'
                f'Upload documents or use existing ones'
                f'</div>', 
                unsafe_allow_html=True
            )
        
        st.markdown("---")
        
        # Quick Actions
        st.markdown("#### ⚡ QUICK ACTIONS")
        
        # Document Upload Section
        st.markdown("#### 📤 UPLOAD DOCUMENTS")
        uploaded_files = st.file_uploader(
            "Choose files",
            type=['pdf', 'txt', 'doc', 'docx'],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
        
        if uploaded_files:
            if st.button("🚀 PROCESS UPLOADED FILES", use_container_width=True, type="primary"):
                if create_vector_embedding_from_files(uploaded_files):
                    st.success("Uploaded files processed successfully!")
                    st.rerun()
        
        # Use existing files button
        if st.button("USE EXISTING DOCUMENTS", use_container_width=True):
            if create_vector_embedding_from_files():
                st.success("Existing documents processed successfully!")
                st.rerun()
        
        if st.button("CLEAR CHAT HISTORY", use_container_width=True):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
            st.rerun()
        
        st.markdown("---")
        
        st.markdown("#### 💬 RECENT QUERIES")
        if st.session_state.chat_history:
            for i, chat in enumerate(st.session_state.chat_history[-5:]):
                with st.expander(f"Q: {chat['question'][:50]}..." if len(chat['question']) > 50 else f"Q: {chat['question']}", expanded=False):
                    voice_indicator = "🎙️ " if chat.get('voice_query') else ""
                    st.markdown(f'<div class="chat-bubble chat-question"><strong>Question:</strong> {voice_indicator}{chat["question"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="chat-bubble chat-answer"><strong>Answer:</strong> {chat["answer"][:150]}...</div>', unsafe_allow_html=True)
        else:
            st.info("No queries yet. Start a conversation!")
        
        st.markdown("---")
        st.markdown("**Built with:**")
        st.markdown("• Streamlit")
        st.markdown("• LangChain ")
        st.markdown("• Groq  LLM")
        st.markdown("• ElevenLabs ")
        st.markdown(f"*Session: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
