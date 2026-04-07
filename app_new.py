"""
Document Intelligence Platform - Main Application
A modular AI-powered document analysis system with voice assistant capabilities
"""
import streamlit as st

# Configure page FIRST before any other imports
st.set_page_config(
    page_title="Document Intelligence Platform",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import configuration
from config.settings import GROQ_API_KEY, OPENAI_API_KEY
from config.styling import DARK_THEME_CSS

# Import utilities
from utils.session_state import initialize_session_state

# Import components
from components.sidebar import render_sidebar
from components.query_tab import render_query_tab
from components.voice_tab import render_voice_tab
from components.analytics_tab import render_analytics_tab
from components.settings_tab import render_settings_tab

# Validate API keys
if not GROQ_API_KEY:
    st.error("🔑 GROQ API key not found! Please check your .env file.")
    st.stop()

if not OPENAI_API_KEY:
    st.error("🔑 OpenAI API key not found! Please check your .env file.")
    st.stop()

# Apply dark theme styling
st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)

# Initialize session state
initialize_session_state()

# Main UI - Professional Header
st.markdown('<div class="main-header"> AI-Powered Document Analyzer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">'
    '🚀 AI-Powered Document Analysis & Knowledge Extraction System<br>'
    '<small style="color: #88d3ce; font-size: 1.1rem; font-weight: 300;">'
    'Upload documents • Ask questions • Get answers • Voice Assistant Bot'
    '</small>'
    '</div>', 
    unsafe_allow_html=True
)

# Render sidebar
render_sidebar()

# Main content area with tabs
tab1, tab2, tab3, tab4 = st.tabs(["🔍 QUERY DOCUMENTS", "🎙️ VOICE ASSISTANT", "📊 ANALYTICS", "⚙️ SETTINGS"])

with tab1:
    render_query_tab()

with tab2:
    render_voice_tab()

with tab3:
    render_analytics_tab()

with tab4:
    render_settings_tab()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #66fcf1; font-size: 0.9rem;'>"
    "🔍 Document Intelligence Platform • Built with Streamlit, LangChain, and Groq • "
    "ElevenLabs Voice Assistant • Enterprise Ready AI Solution"
    "</div>", 
    unsafe_allow_html=True
)
