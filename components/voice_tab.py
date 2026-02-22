"""
Voice Assistant Tab UI Component
"""
import streamlit as st
from datetime import datetime
from services.llm_service import process_query
from services.voice_service import speech_to_text, text_to_speech
from config.settings import ELEVENLABS_VOICES

def voice_query_interface():
    """Voice query interface component"""
    with st.container():
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            if st.button("🎤 Start Listening", use_container_width=True, type="primary"):
                if "vectors" not in st.session_state:
                    st.error("Please process documents first!")
                else:
                    spoken_text = speech_to_text()
                    if spoken_text and not spoken_text.startswith(("Timeout", "Could not", "Error")):
                        st.session_state.voice_query = spoken_text
                        st.success(f"🎤 Heard: '{spoken_text}'")
                        
                        # Process the voice query
                        response, response_time = process_query(spoken_text)
                        if response:
                            # Store in chat history
                            st.session_state.chat_history.append({
                                "question": spoken_text,
                                "answer": response['answer'],
                                "timestamp": datetime.now(),
                                "response_time": response_time,
                                "voice_query": True
                            })
                            
                            # Store for voice replay
                            st.session_state.last_spoken_text = response['answer']
                            st.session_state.show_response = True
                            st.session_state.current_response = response['answer']
                    else:
                        st.error(f"Voice recognition failed: {spoken_text}")
        
        with col2:
            if st.session_state.get('last_spoken_text'):
                if st.button("🔊 Repeat Answer", use_container_width=True):
                    audio_response = text_to_speech(
                        st.session_state.last_spoken_text,
                        provider=st.session_state.tts_provider,
                        voice_id=ELEVENLABS_VOICES[st.session_state.selected_voice]
                    )
                    if audio_response:
                        st.markdown(audio_response, unsafe_allow_html=True)
        
        with col3:
            # Voice preview
            if st.button("🎵 Preview Voice", use_container_width=True):
                preview_text = "Hello! I'm your Shyam AI voice assistant. How can I help you today?"
                audio_response = text_to_speech(
                    preview_text,
                    provider=st.session_state.tts_provider,
                    voice_id=ELEVENLABS_VOICES[st.session_state.selected_voice]
                )
                if audio_response:
                    st.markdown(audio_response, unsafe_allow_html=True)
        
        with col4:
            if st.button("⏹️ Stop Audio", use_container_width=True):
                st.info("Refresh page to stop audio playback")
    
    # Display response outside columns for full width
    if st.session_state.get('show_response') and st.session_state.get('current_response'):
        st.markdown("### 📋 AI RESPONSE")
        st.markdown(f'<div class="response-box">{st.session_state.current_response}</div>', unsafe_allow_html=True)
        
        # Text-to-speech for the response
        st.markdown("### 🔊 AI AUDIO RESPONSE")
        audio_response = text_to_speech(
            st.session_state.current_response, 
            provider=st.session_state.tts_provider,
            voice_id=ELEVENLABS_VOICES[st.session_state.selected_voice]
        )
        if audio_response:
            st.markdown(audio_response, unsafe_allow_html=True)
        
        # Reset the flag after displaying
        st.session_state.show_response = False

def render_voice_tab():
    """Render the voice assistant tab"""
    st.markdown("### 🎙️ VOICE-ENABLED DOCUMENT ASSISTANT")
    
    if "vectors" not in st.session_state:
        st.warning("⚠️ Please process documents first to use the voice assistant!")
        if st.button("📁 Go to Document Processing", use_container_width=True):
            st.rerun()
    else:
        voice_query_interface()
        
        # Voice chat history
        if any(chat.get('voice_query') for chat in st.session_state.chat_history):
            st.markdown("### 🎙️ VOICE QUERY HISTORY")
            voice_chats = [chat for chat in st.session_state.chat_history if chat.get('voice_query')]
            for chat in voice_chats[-5:]:
                with st.expander(f"🎙️ {chat['question'][:60]}...", expanded=False):
                    st.markdown(f'<div class="chat-bubble chat-question"><strong>Voice Question:</strong> {chat["question"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="chat-bubble chat-answer"><strong>AI Response:</strong> {chat["answer"]}</div>', unsafe_allow_html=True)
                    
                    if st.button(f"🔊 Play Response", key=f"play_{chat['timestamp']}"):
                        audio_response = text_to_speech(
                            chat['answer'],
                            provider=st.session_state.tts_provider,
                            voice_id=ELEVENLABS_VOICES[st.session_state.selected_voice]
                        )
                        if audio_response:
                            st.markdown(audio_response, unsafe_allow_html=True)
