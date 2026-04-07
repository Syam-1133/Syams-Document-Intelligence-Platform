"""
Session state initialization and management
"""
import streamlit as st
import queue

def initialize_session_state():
    """Initialize all session state variables"""
    # Voice assistant states
    if "listening" not in st.session_state:
        st.session_state.listening = False
    if "audio_queue" not in st.session_state:
        st.session_state.audio_queue = queue.Queue()
    if "last_spoken_text" not in st.session_state:
        st.session_state.last_spoken_text = ""
    if "selected_voice" not in st.session_state:
        st.session_state.selected_voice = "Bella"
    if "tts_provider" not in st.session_state:
        st.session_state.tts_provider = "elevenlabs"
    
    # Chat and document states
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "document_source" not in st.session_state:
        st.session_state.document_source = "Not initialized"
    if "voice_query" not in st.session_state:
        st.session_state.voice_query = ""
    
    # Response states
    if "show_response" not in st.session_state:
        st.session_state.show_response = False
    if "current_response" not in st.session_state:
        st.session_state.current_response = ""
