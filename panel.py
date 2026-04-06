import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components
import random

# --- AI CONFIG ---
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AdaptiveHire | AI Intelligence", layout="wide", initial_sidebar_state="expanded")

# --- PREMIUM NLCORTEX STYLE CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; background-color: #050810; color: #e2e8f0; }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
    }

    /* Chat Container */
    #chat-scroll {
        height: 520px; overflow-y: auto; padding: 20px;
        background: rgba(2, 6, 23, 0.5); border-radius: 15px;
        display: flex; flex-direction: column; gap: 15px;
    }

    /* Modern Bubbles */
    .ik-bubble { 
        background: linear-gradient(135deg, #450a0a 0%, #7f1d1d 100%);
        color: #fecaca; padding: 15px; border-radius: 4px 20px 20px 20px;
        max-width: 85%; align-self: flex-start; border-left: 4px solid #ef4444;
    }
    .aday-bubble { 
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        color: #dbeafe; padding: 15px; border-radius: 20px 4px 20px 20px;
        max-width: 85%; align-self: flex-end; border-right: 4px solid #3b82f6; text-align: right;
    }

    /* Status Indicators */
    .indicator-label { font-size: 0.75rem; color: #94a3b8; margin-bottom: 5px; text-transform: uppercase; }
    .neon-text-red { color: #f87171; text-shadow: 0 0 10px rgba(248, 113, 113, 0.5); }
    .neon-text-blue { color: #60a5fa; text-shadow: 0 0 10px rgba(96, 165, 250, 0.5); }
    
    /* Ses Dalgası Simülasyonu */
    .wave-container { display: flex; align-items: center; gap: 3px; height: 30px; }
    .wave-bar { width: 3px; background: #3b82f6; border-radius: 50px; animation: wave 1s ease-in-out infinite; }
    @keyframes wave { 0%, 100% { height: 5px; } 50% { height: 25px; } }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "setup"
if 'ik_name' not in st.session_state: st.session_state.ik_name = "İK Direktörü"
if 'aday_name' not in st.session_state: st.session_state.aday_name = "Aday"

# --- ⬅️ SOL PANEL: İŞLETME & KİMLİK ---
with st.sidebar:
    st.markdown("<div class='glass-card' style='text-align:center;'>", unsafe_allow_html=True)
    st.markdown("### 💠 NE X T H I R E")
    st.markdown("<p style='font-size:0.8rem; opacity:0.6;'>Enterprise Intelligence v2.0</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    with st.expander("🏢 İşletme Detayları", expanded=True):
        st.text_input("Kurum", "Global Corp AI")
        st.text_input("Departman", "Talent Acquisition")
    
    with st.expander("👤 Katılımcılar", expanded=True):
        st.session_state.ik_name = st.text_input("Görüşmeci", st.session_state.ik_name)
        st.session_state.aday_name = st.text_input("Aday", st.session_state.aday_name)
    
    if st.button("🔌 Sistemi Kapat", use_container_width=True):
        st.session_state.page = "setup"
        st.rerun()

# --- ANA AKIŞ ---
if st.session_state.page == "setup":
    st.markdown("<h2 style='text-align:center;'>Mülakat Kontrol Merkezi</h2>", unsafe_allow_html=True)
    col_s1, col_s2, col_s3 = st.columns([1,2,1])
    with col_s2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.write("🎯 **Analiz Katmanları**")
        st.multiselect("Aktif Modüller", ["DISC", "NLP Stres Analizi", "Bilişsel Yük", "Teknik Skor"], default=["DISC", "NLP Stres Analizi"])
        st.write("<br>⏱️ **Segment Yapılandırması**", unsafe_allow_html=True)
        st.radio("Süre", ["30 sn", "1 dk", "2 dk", "5 dk"], horizontal=True, label_visibility="collapsed")
        st.divider()
        if st.button("🚀 CANLI OTURUMU BAŞLAT", type="primary", use_container_width=True):
            st.session_state.page = "live"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "live":
    # 3'lü Panel Yapısı (Sol zaten sidebar, Orta: Chat, Sağ: NLCortex Analiz)
    col_mid, col_right = st.columns([2.2, 1])

    # 🎙️ ORTA PANEL: CANLI AKIŞ
    with col_mid:
        st.markdown(f"<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;'><div><span class='neon-text-red'>● LIVE</span> <span style='margin-left:10px; opacity:0.8;'>{st.session_state.ik_name} vs {st.session_state.aday_name}</span></div><div class='wave-container'><div class='wave-bar'></div><div class='wave-bar' style='animation-delay:0.1s'></div><div class='wave-bar' style='animation-delay:0.2s'></div><div class='wave-bar' style='animation-delay:0.3s'></div></div></div>", unsafe_allow_html=True)
        
        components.html(f"""
            <div id="chat-scroll" style="background:rgba(2, 6, 23, 0.6); height:520px; overflow-y:auto; padding:20px; display:flex; flex-direction:column; gap:15px; font-family:'Inter', sans-serif; border-radius:15px;"></div>
            <script>
                const ik_name = "{st.session_state.ik_name}";
                const aday_name = "{st.session_state.aday_name}";
                const scrollDiv = document.getElementById('chat-scroll');
                const Recognition = window.webkitSpeechRecognition || window.SpeechRecognition;
                
                if(Recognition) {{
                    const rec = new Recognition();
                    rec.lang = 'tr-TR'; rec.continuous = true; rec.interimResults = true;
                    let lastFinal = "";

                    rec.onresult = (event) => {{
                        for (let i = event.resultIndex; i < event.results.length; i++) {{
                            if (event.results[i].isFinal) {{
                                let text = event.results[i][0].transcript.trim();
                                if(text === lastFinal) return;
                                lastFinal = text;

                                let isIK = text.toLowerCase().includes('?') || text.toLowerCase().includes('neden') || text.toLowerCase().includes('anlat');
                                const row = document.createElement('div');
                                row.style = "display:flex; width:100%; margin-bottom:15px; justify-content:" + (isIK ? 'flex-start' : 'flex-end');
                                
                                const bubble = document.createElement('div');
                                const bg = isIK ? 'linear-gradient(135deg, #450a0a, #7f1d1d)' : 'linear-gradient(135deg, #1e3a8a, #1e40af)';
                                const border = isIK ? 'border-left:4px solid #ef4444' : 'border-right:4px solid #3b82f6';
                                const radius = isIK ? '4px 20px 20px 20px' : '20px 4px 20px 20px';

                                bubble.style = `background:${{bg}}; color:white; padding:15px; border-radius:${{radius}}; max-width:80%; ${{border}}; box-shadow:0 4px 15px rgba(0,0,0,0.3);`;
                                bubble.innerHTML = `<div style="color:${{isIK?'#f87171':'#60a5fa'}}; font-size:0.7rem; font-weight:bold; margin-bottom:5px; text-transform:uppercase;">${{isIK?ik_name:aday_name}}</div>` + text;
                                
                                row.appendChild(bubble);
                                scrollDiv.appendChild(row);
                                scrollDiv.scrollTop = scrollDiv.scrollHeight;
                            }}
                        }}
                    }};
                    rec.start();
                }}
            </script>
        """, height=550)

    # ➡️ SAĞ PANEL: NLCORTEX ANALYTICS
    with col_right:
        st.markdown("#### 🧠 Psikometrik Analiz")
        
        with st.container():
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            
            # Anlık Göstergeler (Gauge Simülasyonu)
            st.markdown("<p class='indicator-label'>Dürüstlük & Tutarlılık</p>", unsafe_allow_html=True)
            st.progress(85)
            
            st.markdown("<p class='indicator-label'>Bilişsel Yük (Stres)</p>", unsafe_allow_html=True)
            st.progress(30)
            
            st.markdown("<p class='indicator-label'>Teknik Derinlik</p>", unsafe_allow_html=True)
            st.progress
