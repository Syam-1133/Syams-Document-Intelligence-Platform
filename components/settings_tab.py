"""
Settings Tab UI Component
"""
import streamlit as st

def render_settings_tab():
    """Render the settings tab with configuration options"""
    st.markdown("### ⚙️ SYSTEM CONFIGURATION")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🤖 MODEL SETTINGS")
        model_option = st.selectbox("LLM Model", ["llama-3.1-8b-instant", "llama-3.1-70b-versatile", "mixtral-8x7b"], index=0)
        temperature = st.slider("Temperature", 0.0, 1.0, 0.1, 0.1)
        max_tokens = st.number_input("Max Tokens", 100, 4000, 1000)
        
        st.markdown("#### 🔍 RETRIEVAL SETTINGS")
        chunk_count = st.slider("Number of Chunks to Retrieve", 1, 10, 4)
        search_type = st.selectbox("Search Type", ["similarity", "mmr", "similarity_score_threshold"])
    
    with col2:
        st.markdown("#### 📄 DOCUMENT PROCESSING")
        chunk_size = st.number_input("Chunk Size", 500, 2000, 1000)
        chunk_overlap = st.number_input("Chunk Overlap", 0, 500, 200)
        text_splitter = st.selectbox("Text Splitter", ["RecursiveCharacterTextSplitter", "CharacterTextSplitter"])
        
        st.markdown("#### 🎙️ VOICE SETTINGS")
        tts_engine_choice = st.selectbox("TTS Engine", ["ElevenLabs (Premium)", "gTTS (Online)", "pyttsx3 (Offline)"])
        speech_rate = st.slider("Speech Rate", 50, 300, 150)
        auto_play_voice = st.checkbox("Auto-play voice responses", value=True)
