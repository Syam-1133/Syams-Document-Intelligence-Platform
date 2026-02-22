"""
Dark theme CSS styling for the Document Intelligence Platform
"""

DARK_THEME_CSS = """
<style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .main-header {
        font-size: 2.8rem;
        color: #00d4aa;
        margin-bottom: 1rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #00d4aa, #0099cc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 2px 10px rgba(0, 212, 170, 0.3);
    }
    .sub-header {
        font-size: 1.4rem;
        color: #66fcf1;
        margin-bottom: 1.5rem;
        text-align: center;
        font-weight: 300;
    }
    .metric-card {
        background: linear-gradient(135deg, #1f2833, #0b0c10);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #00d4aa;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        border: 1px solid #45a29e;
    }
    .success-box {
        background: linear-gradient(135deg, #1a472a, #0d1f14);
        border: 1px solid #2e8b57;
        border-radius: 8px;
        padding: 1.2rem;
        margin: 1rem 0;
        color: #90ee90;
    }
    .warning-box {
        background: linear-gradient(135deg, #4a3c1a, #2d240f);
        border: 1px solid #ffd700;
        border-radius: 8px;
        padding: 1.2rem;
        margin: 1rem 0;
        color: #ffd700;
    }
    .response-box {
        background: rgba(15, 23, 42, 0.95);
        border: 2px solid;
        border-image: linear-gradient(135deg, #00f5ff, #0066ff, #9d4edd) 1;
        border-radius: 8px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 102, 255, 0.4),
                0 0 25px rgba(0, 245, 255, 0.3);
        color: #e2e8f0;
        line-height: 1.8;
        min-height: 300px;
        width: 100%;
        max-width: 100%;
        overflow-y: auto;
    }
    .source-box {
        background: linear-gradient(135deg, #2d3047, #1a1c2b);
        border: 1px solid #5d5f7e;
        border-radius: 6px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        color: #c5c6c7;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1f2833, #0b0c10);
        color: white;
    }
    .stButton button {
        background: linear-gradient(135deg, #00d4aa, #0099cc);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #0099cc, #00d4aa);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 212, 170, 0.4);
    }
    .stTextInput input, .stTextArea textarea {
        background: #1f2833 !important;
        color: white !important;
        border: 1px solid #45a29e !important;
        border-radius: 8px !important;
    }
    .stExpander {
        background: #1f2833;
        border: 1px solid #45a29e;
        border-radius: 8px;
    }
    .tab-content {
        background: #0e1117;
        padding: 1rem;
        border-radius: 10px;
    }
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-online {
        background-color: #00ff00;
        box-shadow: 0 0 10px #00ff00;
    }
    .status-offline {
        background-color: #ff4444;
        box-shadow: 0 0 10px #ff4444;
    }
    .chat-bubble {
        background: linear-gradient(135deg, #2d3047, #1a1c2b);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid #5d5f7e;
    }
    .chat-question {
        background: linear-gradient(135deg, #1a472a, #0d1f14);
        border-left: 4px solid #00d4aa;
    }
    .chat-answer {
        background: linear-gradient(135deg, #1a1f2e, #0f131f);
        border-left: 4px solid #4cc9f0;
    }
    .upload-section {
        background: linear-gradient(135deg, #1f2833, #0b0c10);
        padding: 2rem;
        border-radius: 12px;
        border: 2px dashed #45a29e;
        text-align: center;
        margin-bottom: 2rem;
    }
    .voice-controls {
        background: linear-gradient(135deg, #2d1a4c, #1a1c2b);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #8a2be2;
        margin: 1rem 0;
    }
    .voice-active {
        background: linear-gradient(135deg, #1a472a, #0d1f14);
        border: 2px solid #00ff00;
        animation: pulse 2s infinite;
    }
    .premium-voice {
        background: linear-gradient(135deg, #4a1a6c, #2d1a4c);
        border: 2px solid #ff6b6b;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    @keyframes pulse {
        0% { border-color: #00ff00; }
        50% { border-color: #00d4aa; }
        100% { border-color: #00ff00; }
    }
    .voice-selection {
        background: linear-gradient(135deg, #1f2833, #0b0c10);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #45a29e;
        margin: 0.5rem 0;
    }
    .voice-option {
        padding: 0.8rem;
        margin: 0.3rem 0;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 1px solid #45a29e;
    }
    .voice-option:hover {
        background: linear-gradient(135deg, #2d3047, #1a1c2b);
        border-color: #8a2be2;
    }
    .voice-option.selected {
        background: linear-gradient(135deg, #4a1a6c, #2d1a4c);
        border-color: #ff6b6b;
    }
</style>
"""
