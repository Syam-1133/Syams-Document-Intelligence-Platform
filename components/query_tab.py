"""
Query Tab UI Component
"""
import streamlit as st
from datetime import datetime
from services.llm_service import process_query
from services.voice_service import text_to_speech
from config.settings import ELEVENLABS_VOICES

def render_query_tab():
    """Render the main query interface tab"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💬 DOCUMENT QUERY INTERFACE")
        
        # System initialization status
        if "vectors" not in st.session_state:
            st.markdown(
                '<div class="upload-section">'
                '<h3>📁 Upload Documents to Get Started</h3>'
                '<p>Upload PDF, TXT, or DOCX files to analyze their content</p>'
                '<p><small>Or use the "Use Existing Documents" button if you have files in the research_papers directory</small></p>'
                '</div>', 
                unsafe_allow_html=True
            )
        else:
            # Query interface
            st.markdown("#### 📝 ASK A QUESTION")
            user_prompt = st.text_area(
                "Enter your question about the documents:",
                placeholder="e.g., What are the main findings in these documents? Explain the key concepts...",
                height=120,
                label_visibility="collapsed"
            )
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                ask_button = st.button("🔍 ANALYZE DOCUMENTS", type="primary", use_container_width=True)
            with col2:
                speak_button = st.button("🔊 SPEAK ANSWER", use_container_width=True)
            
            if ask_button and user_prompt:
                response, response_time = process_query(user_prompt)
                
                if response:
                    # Store in chat history
                    st.session_state.chat_history.append({
                        "question": user_prompt,
                        "answer": response['answer'],
                        "timestamp": datetime.now(),
                        "response_time": response_time
                    })
                    
                    # Display response in full-width container
                    with st.container():
                        st.markdown("### 📋 ANALYSIS RESULTS")
                        st.markdown(f'<div class="response-box">{response["answer"]}</div>', unsafe_allow_html=True)
                    
                    # Response metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f'<div class="metric-card">⏱️ Response Time<br><h3>{response_time:.2f}s</h3></div>', unsafe_allow_html=True)
                    with col2:
                        st.markdown(f'<div class="metric-card">📚 Sources Retrieved<br><h3>{len(response["context"])}</h3></div>', unsafe_allow_html=True)
                    with col3:
                        st.markdown(f'<div class="metric-card">🤖 Model Used<br><h3>Llama-3.1-8B</h3></div>', unsafe_allow_html=True)
                    
                    # Store for voice
                    st.session_state.last_spoken_text = response['answer']
                    
                    # Source documents
                    with st.expander("📚 VIEW SOURCE DOCUMENTS (4 most relevant)", expanded=False):
                        for i, doc in enumerate(response['context']):
                            st.markdown(f"**Document {i+1}**")
                            st.markdown(f'<div class="source-box">{doc.page_content}</div>', unsafe_allow_html=True)
                            st.markdown("---")
            
            if speak_button and user_prompt and "last_spoken_text" in st.session_state:
                audio_response = text_to_speech(
                    st.session_state.last_spoken_text,
                    provider=st.session_state.tts_provider,
                    voice_id=ELEVENLABS_VOICES[st.session_state.selected_voice]
                )
                if audio_response:
                    st.markdown(audio_response, unsafe_allow_html=True)
