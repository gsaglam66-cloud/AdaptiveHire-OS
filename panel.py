import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components
import random

# --- AI AYARI ---
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AdaptiveHire | OS", layout="wide", initial_sidebar_state="expanded")

# --- CSS: KURUMSAL LIGHT MODE & 11PX FONT ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600&display=swap');
    
    html, body, [class*="st-"] { 
        font-family: 'Segoe UI', sans-serif; 
        background-color: #f8fafc; 
        color: #334155;
        font-size: 11px !important;
    }

    h1, h2, h3, h4 { color: #1e293b !important; font-weight: 600 !important; }
    h4 { font-size: 13px !important; margin-bottom: 8px !important; }

    .corporate-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 12px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }

    #chat-scroll {
        height: 480px; overflow-y: auto; padding: 15px;
        background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px;
        display: flex; flex-direction: column; gap: 10px;
    }

    .ik-bubble { 
        background: #fef2f2; color: #991b1b; 
        padding: 8px 12px; border-radius: 0 10px 10px 10px;
        max-width: 80%; align-self: flex-start; border: 1px solid #fee2e2;
        font-size: 11px !important;
    }
    .aday-bubble { 
        background: #eff6ff; color: #1e40af; 
        padding: 8px 12px; border-radius: 10px 0 10px 10px;
        max-width: 80%; align-self: flex-end; border: 1px solid #dbeafe;
        font-size: 11px !important; text-align: left;
    }

    .label-meta { font-size: 9px; font-weight: bold; opacity: 0.6; margin-bottom: 2px; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE KONTROLLERİ ---
if 'page' not in st.session_state: st.session_state.page = "setup"
if 'ik_name' not in st.session_state: st.session_state.ik_name = "İK Uzmanı"
if 'aday_name' not in st.session_state: st.session_state.aday_name = "Aday"

# --- SOL PANEL: İŞLETME ---
with st.sidebar:
    st.markdown("<h4>🏢 Kurumsal Panel</h4>", unsafe_allow_html=True)
    st.text_input("Şirket Bilgisi", "AdaptiveHire Kurumsal", disabled=True)
    st.divider()
    st.session_state.ik_name = st.text_input("Görüşmeci İsmi", st.session_state.ik_name)
    st.session_state.aday_name = st.text_input("Aday İsmi", st.session_state.aday_name)
    if st.button("🏠 Ana Dashboard", use_container_width=True):
        st.session_state.page = "setup"
        st.rerun()

# --- SAYFA AKIŞI ---
if st.session_state.page == "setup":
    st.title("Mülakat Yönetimi")
    col_c = st.columns([1, 2, 1])[1]
    with col_c:
        st.markdown('<div class="corporate-card">', unsafe_allow_html=True)
        st.write("**Oturum Ayarları**")
        st.multiselect("Aktif Analizler", ["Teknik", "Stres", "NLP"], default=["Teknik", "Stres"])
        st.radio("Segment Süresi", ["1 dk", "2 dk", "5 dk"], horizontal=True)
        if st.button("MÜLAKATI BAŞLAT", type="primary", use_container_width=True):
            st.session_state.page = "live"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "live":
    col_chat, col_ana = st.columns([2, 1])

    with col_chat:
        st.markdown(f"**CANLI:** {st.session_state.ik_name} ↔ {st.session_state.aday_name}")
        # JS içindeki tırnak hataları temizlendi
        components.html(f"""
            <div id="chat-scroll" style="background:white; height:480px; overflow-y:auto; padding:15px; display:flex; flex-direction:column; gap:10px; font-family:sans-serif; border:1px solid #e2e8f0; border-radius:8px;"></div>
            <script>
                const ik = "{st.session_state.ik_name}";
                const aday = "{st.session_state.aday_name}";
                const box = document.getElementById('chat-scroll');
                const Recognition = window.webkitSpeechRecognition || window.SpeechRecognition;
                
                if(Recognition) {{
                    const r = new Recognition();
                    r.lang = 'tr-TR'; r.continuous = true; r.interimResults = true;
                    let lastText = "";

                    r.onresult = (e) => {{
                        for (let i = e.resultIndex; i < e.results.length; i++) {{
                            if (e.results[i].isFinal) {{
                                let t = e.results[i][0].transcript.trim();
                                if(t === lastText) return;
                                lastText = t;
                                let isIK = t.toLowerCase().includes('?') || t.toLowerCase().includes('mi');
                                addMsg(t, isIK);
                            }}
                        }}
                    }};
                    function addMsg(text, isIK) {{
                        const d = document.createElement('div');
                        d.style = "display:flex; width:100%; justify-content:" + (isIK ? 'flex-start' : 'flex-end');
                        const b = document.createElement('div');
                        b.style = isIK ? "background:#fef2f2; color:#991b1b; padding:8px 12px; border-radius:0 10px 10px 10px; border:1px solid #fee2e2; max-width:80%; font-size:11px;" : "background:#eff6ff; color:#1e40af; padding:8px 12px; border-radius:10px 0 10px 10px; border:1px solid #dbeafe; max-width:80%; font-size:11px;";
                        b.innerHTML = '<div style="font-size:9px; font-weight:bold; opacity:0.5; margin-bottom:2px;">' + (is
