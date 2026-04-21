"""
Voice Assistant Service - Text-to-Speech and Speech-to-Text
"""
import streamlit as st
import pyttsx3
import speech_recognition as sr
import io
import base64
import requests
import threading
import time
from config.settings import ELEVENLABS_API_KEY, ELEVENLABS_VOICES, SPEECH_RATE, SPEECH_VOLUME, SPEECH_TIMEOUT, SPEECH_PHRASE_TIME_LIMIT

@st.cache_resource
def init_voice_engine():
    """Initialize text-to-speech engine"""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[1].id)  # Female voice if available
        engine.setProperty('rate', SPEECH_RATE)
        engine.setProperty('volume', SPEECH_VOLUME)
        return engine
    except Exception as e:
        st.warning(f"Text-to-speech engine initialization failed: {str(e)}")
        return None

@st.cache_resource
def init_speech_recognizer():
    """Initialize speech recognition"""
    return sr.Recognizer()

def is_microphone_available():
    """Check if microphone is available"""
    try:
        with sr.Microphone() as source:
            return True
    except Exception as e:
        return False

def text_to_speech_elevenlabs(text, voice_id, stability=0.5, similarity_boost=0.5):
    """Convert text to speech using ElevenLabs API"""
    try:
        if not ELEVENLABS_API_KEY:
            return "❌ ElevenLabs API key not configured"
        
        # ElevenLabs API endpoint
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        
        data = {
            "text": text,
            "model_id": "eleven_turbo_v2_5",
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            audio_buffer = io.BytesIO(response.content)
            audio_buffer.seek(0)
            
            # Encode audio for HTML audio element
            audio_base64 = base64.b64encode(audio_buffer.read()).decode()
            audio_html = f'''
                <audio autoplay controls style="width: 100%; margin: 10px 0;">
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                    Your browser does not support the audio element.
                </audio>
                <div style="text-align: center; color: #ff6b6b; font-size: 0.9rem;">
                    🎙️ Premium Voice: {list(ELEVENLABS_VOICES.keys())[list(ELEVENLABS_VOICES.values()).index(voice_id)]}
                </div>
            '''
            return audio_html
        else:
            return f"❌ ElevenLabs API Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"❌ Error in ElevenLabs TTS: {str(e)}"

def text_to_speech(text, provider="elevenlabs", voice_id=None):
    """Convert text to speech using selected provider"""
    try:
        if provider == "elevenlabs" and ELEVENLABS_API_KEY:
            if not voice_id:
                voice_id = ELEVENLABS_VOICES.get(st.session_state.selected_voice, "hpp4J3VqNfWAUOO0d1Us")
            return text_to_speech_elevenlabs(text[:800], voice_id)  # Limit text length
                
    except Exception as e:
        return f"❌ Error in text-to-speech: {str(e)}"

def speech_to_text():
    """Convert speech to text using microphone input"""
    try:
        if not is_microphone_available():
            return "Microphone not available. Please check your audio settings."
        
        speech_recognizer = init_speech_recognizer()
        with sr.Microphone() as source:
            st.session_state.listening = True
            speech_recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Show listening indicator
            listening_placeholder = st.empty()
            listening_placeholder.info("🎤 Listening... Speak now!")
            
            # Listen for audio
            audio = speech_recognizer.listen(source, timeout=SPEECH_TIMEOUT, phrase_time_limit=SPEECH_PHRASE_TIME_LIMIT)
            
            # Recognize speech
            text = speech_recognizer.recognize_google(audio)
            listening_placeholder.empty()
            st.session_state.listening = False
            return text
            
    except sr.WaitTimeoutError:
        st.session_state.listening = False
        return "Timeout: No speech detected"
    except sr.UnknownValueError:
        st.session_state.listening = False
        return "Could not understand audio"
    except sr.RequestError as e:
        st.session_state.listening = False
        return f"Error with speech recognition service: {str(e)}"
    except Exception as e:
        st.session_state.listening = False
        return f"Error: {str(e)}"


# Background listening thread management
_listener_thread = None
_stop_listening = False


def _background_listener_worker():
    """Worker function for background listening in separate thread"""
    global _stop_listening
    try:
        speech_recognizer = init_speech_recognizer()

        while not _stop_listening:
            try:
                with sr.Microphone() as source:
                    st.session_state.is_recording = True
                    speech_recognizer.adjust_for_ambient_noise(source, duration=0.5)

                    # Listen for audio
                    audio = speech_recognizer.listen(
                        source,
                        timeout=SPEECH_TIMEOUT,
                        phrase_time_limit=SPEECH_PHRASE_TIME_LIMIT
                    )

                    # Recognize speech
                    text = speech_recognizer.recognize_google(audio)
                    st.session_state.is_recording = False

                    # Put transcribed text in queue
                    st.session_state.audio_queue.put(text)

            except sr.WaitTimeoutError:
                st.session_state.is_recording = False
                continue
            except sr.UnknownValueError:
                st.session_state.is_recording = False
                st.session_state.audio_queue.put("UNKNOWN_AUDIO")
            except sr.RequestError as e:
                st.session_state.is_recording = False
                st.session_state.audio_queue.put(f"ERROR:{str(e)}")
            except Exception as e:
                st.session_state.is_recording = False
                st.session_state.audio_queue.put(f"ERROR:{str(e)}")
    except Exception as e:
        st.session_state.is_recording = False
        st.session_state.audio_queue.put(f"THREAD_ERROR:{str(e)}")


def start_background_listener():
    """Start background listening in a separate thread"""
    global _listener_thread, _stop_listening

    if not is_microphone_available():
        return "Microphone not available. Cannot start background listening."

    if _listener_thread is not None and _listener_thread.is_alive():
        return "Background listener already running"

    _stop_listening = False
    _listener_thread = threading.Thread(target=_background_listener_worker, daemon=True)
    _listener_thread.start()
    st.session_state.listening = True
    return "Background listener started"


def stop_background_listener():
    """Stop background listening thread gracefully"""
    global _listener_thread, _stop_listening

    _stop_listening = True
    if _listener_thread is not None:
        _listener_thread.join(timeout=2)
    st.session_state.listening = False
    return "Background listener stopped"


def get_transcription_from_queue(timeout=1):
    """Get transcribed text from queue without blocking"""
    try:
        transcription = st.session_state.audio_queue.get(timeout=timeout)

        # Handle error messages
        if isinstance(transcription, str):
            if transcription.startswith("ERROR"):
                error_msg = transcription.replace("ERROR:", "")
                return None, f"Speech recognition error: {error_msg}"
            elif transcription.startswith("THREAD_ERROR"):
                error_msg = transcription.replace("THREAD_ERROR:", "")
                return None, f"Background listener error: {error_msg}"
            elif transcription == "UNKNOWN_AUDIO":
                return None, "Could not understand audio"

        return transcription, None

    except:
        return None, None


def is_background_listener_running():
    """Check if background listener is currently running"""
    global _listener_thread
    return _listener_thread is not None and _listener_thread.is_alive()
