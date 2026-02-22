"""
Analytics Tab UI Component
"""
import streamlit as st
from datetime import datetime

def render_analytics_tab():
    """Render the analytics tab with system statistics"""
    st.markdown("### 📊 SYSTEM ANALYTICS")
    
    if "vectors" in st.session_state:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📈 DOCUMENT STATISTICS")
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1f2833, #0b0c10); padding: 1.5rem; border-radius: 10px; border: 1px solid #45a29e;'>
                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;'>
                    <div style='text-align: center;'>
                        <h4 style='color: #66fcf1; margin: 0;'>Total Documents</h4>
                        <h3 style='color: #00d4aa; margin: 0.5rem 0;'>{len(st.session_state.final_documents)}</h3>
                    </div>
                    <div style='text-align: center;'>
                        <h4 style='color: #66fcf1; margin: 0;'>Text Chunks</h4>
                        <h3 style='color: #00d4aa; margin: 0.5rem 0;'>{len(st.session_state.final_documents)}</h3>
                    </div>
                    <div style='text-align: center;'>
                        <h4 style='color: #66fcf1; margin: 0;'>Document Source</h4>
                        <h3 style='color: #00d4aa; margin: 0.5rem 0; font-size: 0.9rem;'>{st.session_state.document_source}</h3>
                    </div>
                    <div style='text-align: center;'>
                        <h4 style='color: #66fcf1; margin: 0;'>Vector Dimension</h4>
                        <h3 style='color: #00d4aa; margin: 0.5rem 0;'>1536</h3>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### ⚡ PERFORMANCE METRICS")
            if st.session_state.chat_history:
                avg_response_time = sum([chat['response_time'] for chat in st.session_state.chat_history]) / len(st.session_state.chat_history)
                voice_queries = len([chat for chat in st.session_state.chat_history if chat.get('voice_query')])
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1f2833, #0b0c10); padding: 1.5rem; border-radius: 10px; border: 1px solid #45a29e;'>
                    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;'>
                        <div style='text-align: center;'>
                            <h4 style='color: #66fcf1; margin: 0;'>Total Queries</h4>
                            <h3 style='color: #00d4aa; margin: 0.5rem 0;'>{len(st.session_state.chat_history)}</h3>
                        </div>
                        <div style='text-align: center;'>
                            <h4 style='color: #66fcf1; margin: 0;'>Voice Queries</h4>
                            <h3 style='color: #00d4aa; margin: 0.5rem 0;'>{voice_queries}</h3>
                        </div>
                        <div style='text-align: center;'>
                            <h4 style='color: #66fcf1; margin: 0;'>Avg Response Time</h4>
                            <h3 style='color: #00d4aa; margin: 0.5rem 0;'>{avg_response_time:.2f}s</h3>
                        </div>
                        <div style='text-align: center;'>
                            <h4 style='color: #66fcf1; margin: 0;'>Session Start</h4>
                            <h3 style='color: #00d4aa; margin: 0.5rem 0;'>{datetime.now().strftime('%H:%M')}</h3>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("No query data available yet")
