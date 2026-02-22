"""
Configuration settings for the Document Intelligence Platform
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')

# OpenMP Configuration (for fixing threading issues)
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
os.environ['OMP_NUM_THREADS'] = '1'

# Set API keys in environment
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY if OPENAI_API_KEY else ""
os.environ['GROQ_API_KEY'] = GROQ_API_KEY if GROQ_API_KEY else ""

# LLM Configuration
LLM_MODEL = "llama-3.1-8b-instant"
LLM_TEMPERATURE = 0.1
LLM_MAX_TOKENS = 1000

# Document Processing Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
BATCH_SIZE = 10
SEPARATORS = ["\n\n", "\n", ". ", " ", ""]

# Retrieval Configuration
RETRIEVAL_SEARCH_TYPE = "similarity"
RETRIEVAL_K = 4

# Voice Configuration
SPEECH_RATE = 150
SPEECH_VOLUME = 0.8
SPEECH_TIMEOUT = 10
SPEECH_PHRASE_TIME_LIMIT = 15

# ElevenLabs Voice Options
ELEVENLABS_VOICES = {
    "Rachel": "21m00Tcm4TlvDq8ikWAM",
    "Domi": "AZnzlk1XvdvUeBnXmlld",
    "Bella": "EXAVITQu4vr4xnSDxMaL",
    "Antoni": "ErXwobaYiN019PkySvjV",
    "Elli": "MF3mGyEYCl7XYWbV9V6O",
    "Josh": "TxGEqnHWrfWFTfGW9XjX",
    "Arnold": "VR6AewLTigWG4xSOukaG",
    "Adam": "pNInz6obpgDQGcFmaJgB",
    "Sam": "yoZ06aMxZJJ28mfd3POQ"
}

# Page Configuration
PAGE_TITLE = "Document Intelligence Platform"
PAGE_ICON = "🔍"
