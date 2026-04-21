"""
Voice Assistant Tab UI Component
"""
import streamlit as st
from datetime import datetime
from services.llm_service import process_query, process_query_streaming
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

def voice_query_interface_streaming():
    """Voice query interface with streaming responses (real-time)"""
    with st.container():
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

        with col1:
            if st.button("🎤 Start Listening (Streaming)", use_container_width=True, type="primary"):
                if "vectors" not in st.session_state:
                    st.error("Please process documents first!")
                else:
                    # Transcription step
                    st.info("🎤 Listening for speech...")
                    spoken_text = speech_to_text()

                    if spoken_text and not spoken_text.startswith(("Timeout", "Could not", "Error")):
                        st.session_state.voice_query = spoken_text
                        st.success(f"✅ Heard: '{spoken_text}'")
                        st.info("🤖 Processing and streaming response...")

                        # Create placeholders for real-time updates
                        response_text_placeholder = st.empty()
                        response_indicator = st.empty()

                        accumulated_response = ""
                        context_docs = None

                        try:
                            # Stream the response token by token
                            token_count = 0
                            for token, full_response, docs in process_query_streaming(spoken_text):
                                if token is None:  # Stream complete
                                    context_docs = docs
                                    response_indicator.success("✅ Response complete")
                                    break

                                accumulated_response = full_response
                                token_count += 1

                                # Update display in real-time with animated cursor
                                with response_text_placeholder.container():
                                    st.markdown(f'<div class="response-box">{accumulated_response}▌</div>', unsafe_allow_html=True)

                            if not accumulated_response:
                                st.error("❌ Could not generate response. Please try again.")
                                return

                        except StopIteration:
                            st.warning("⚠️ Response streaming interrupted")
                            return
                        except Exception as e:
                            st.error(f"❌ Error in streaming: {str(e)}")
                            # Fallback to non-streaming
                            st.info("Attempting non-streaming response...")
                            response, response_time = process_query(spoken_text)
                            if response:
                                accumulated_response = response['answer']
                                context_docs = response['context']
                            else:
                                return

                        # Store complete response
                        if accumulated_response and context_docs is not None:
                            st.session_state.chat_history.append({
                                "question": spoken_text,
                                "answer": accumulated_response,
                                "timestamp": datetime.now(),
                                "response_time": 0,
                                "voice_query": True
                            })

                            st.session_state.last_spoken_text = accumulated_response
                            st.session_state.current_response = accumulated_response

                            # Play audio
                            st.markdown("### 🔊 AI AUDIO RESPONSE")
                            try:
                                audio_response = text_to_speech(
                                    accumulated_response,
                                    provider=st.session_state.tts_provider,
                                    voice_id=ELEVENLABS_VOICES[st.session_state.selected_voice]
                                )
                                if audio_response:
                                    st.markdown(audio_response, unsafe_allow_html=True)
                                else:
                                    st.warning("⚠️ Could not generate audio response")
                            except Exception as e:
                                st.error(f"❌ Audio generation error: {str(e)}")
                    else:
                        st.error(f"❌ Voice recognition failed: {spoken_text}")

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


def render_voice_tab():
    """Render the voice assistant tab"""
    st.markdown("### 🎙️ VOICE-ENABLED DOCUMENT ASSISTANT")

    if "vectors" not in st.session_state:
        st.warning("⚠️ Please process documents first to use the voice assistant!")
        if st.button("📁 Go to Document Processing", use_container_width=True):
            st.rerun()
    else:
        # Mode selection
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            mode = st.radio("Response Mode", ["⚡ Streaming (Real-time)", "📝 Standard"], horizontal=True)

        if mode == "⚡ Streaming (Real-time)":
            st.info("💡 Responses stream token-by-token in real-time!")
            voice_query_interface_streaming()
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
