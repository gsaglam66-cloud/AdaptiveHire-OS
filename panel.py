import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components
import random

# --- AI AYARI ---
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AdaptiveHire - Real-Time Dual Audio", layout="wide", initial_sidebar_state="expanded")

# --- GELİŞMİŞ RENKLİ CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #fcfdfe; }
    .ah-card { background: white; padding: 25px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 20px; }
    
    /* Transkript Konteynırı */
    .chat-box { height: 500px; overflow-y: auto; padding: 20px; background: #1e1e1e; border-radius: 15px; display: flex; flex-direction: column; gap: 10px; }
    
    /* İK Uzmanı Stili (KIRMIZI) */
    .ik-bubble { 
        background: #450a0a; border-left: 5px solid #ef4444; color: #fca5a5; 
        padding: 12px; border-radius: 8px; align-self: flex-start; max-width: 85%;
        font-family: 'Courier New', Courier, monospace;
    }
    .ik-label { color: #ef4444; font-weight: bold; font-size: 0.8rem; margin-bottom: 5px; display: block; }

    /* Aday Stili (MAVİ) */
    .aday-bubble { 
        background: #172554; border-left: 5px solid #3b82f6; color: #bfdbfe; 
        padding: 12px; border-radius: 8px; align-self: flex-end; max-width: 85%;
        font-family: 'Courier New', Courier, monospace; text-align: right;
    }
    .aday-label { color: #3b82f6; font-weight: bold; font-size: 0.8rem; margin-bottom: 5px; display: block; }

    .interim-text { opacity: 0.6; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "setup"
if 'ik_name' not in st.session_state: st.session_state.ik_name = "İK UZMANI"
if 'aday_name' not in st.session_state: st.session_state.aday_name = "ADAY"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#2563eb;'>AdaptiveHire</h2>", unsafe_allow_html=True)
    st.session_state.ik_name = st.text_input("İK Uzmanı:", st.session_state.ik_name)
    st.session_state.aday_name = st.text_input("Aday:", st.session_state.aday_name)
    st.divider()
    if st.button("🏠 Dashboard", use_container_width=True):
        st.session_state.page = "setup"
        st.rerun()

# --- ANA AKIŞ ---
if st.session_state.page == "setup":
    st.subheader("Mülakat Paneli")
    st.markdown('<div class="ah-card">', unsafe_allow_html=True)
    st.write("**SEGMENT SÜRESİ**")
    st.radio("Süre Seçin", ["15 sn", "30 sn", "1 dk", "2 dk", "5 dk"], index=1, horizontal=True, label_visibility="collapsed")
    if st.button("Mülakatı Başlat →", type="primary", use_container_width=True):
        st.session_state.page = "live"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "live":
    st.markdown(f"### 🎙️ Canlı Görüşme Aktif")
    
    col_main, col_side = st.columns([2.5, 1])
    
    with col_main:
        # GERÇEK ZAMANLI VE RENKLİ TRANSKRİPT MOTORU
        components.html(f"""
            <div id="container" style="background:#1e1e1e; height:500px; overflow-y:auto; padding:15px; display:flex; flex-direction:column; gap:12px; border-radius:15px; font-family:sans-serif;">
            </div>
            
            <script>
                const ik_name = "{st.session_state.ik_name}";
                const aday_name = "{st.session_state.aday_name}";
                const container = document.getElementById('container');
                
                const Recognition = window.webkitSpeechRecognition || window.SpeechRecognition;
                if(Recognition) {{
                    const rec = new Recognition();
                    rec.lang = 'tr-TR';
                    rec.continuous = true;
                    rec.interimResults = true; // Hız için true yapıldı
                    
                    let currentDiv = null;

                    rec.onresult = (event) => {{
                        let interimTranscript = '';
                        let finalTranscript = '';

                        for (let i = event.resultIndex; i < event.results.length; i++) {{
                            const transcript = event.results[i][0].transcript;
                            if (event.results[i].isFinal) {{
                                finalTranscript += transcript;
                            }} else {{
                                interimTranscript += transcript;
                            }}
                        }}

                        if (finalTranscript || interimTranscript) {{
                            const text = (finalTranscript || interimTranscript).toLowerCase();
                            
                            // AKILLI ANALİZ VE RENK ATAMASI
                            let isIK = text.includes('mi') || text.includes('mısınız') || text.includes('neden') || text.includes('anlat') || text.includes('hoş gel');
                            let speaker = isIK ? ik_name : aday_name;
                            let bubbleClass = isIK ? 'background:#450a0a; border-left:5px solid #ef4444; color:#fca5a5; align-self:flex-start;' : 'background:#172554; border-left:5px solid #3b82f6; color:#bfdbfe; align-self:flex-end; text-align:right;';
                            let labelColor = isIK ? '#ef4444' : '#3b82f6';

                            if (!currentDiv || event.results[event.resultIndex].isFinal) {{
                                currentDiv = document.createElement('div');
                                currentDiv.style = bubbleClass + "padding:12px; border-radius:8px; max-width:80%; font-size:1rem; margin-bottom:10px;";
                                container.appendChild(currentDiv);
                            }}

                            currentDiv.innerHTML = `<span style="color:${{labelColor}}; font-weight:bold; font-size:0.7rem; display:block; margin-bottom:4px;">${{speaker}}</span>` + 
                                                   (finalTranscript ? finalTranscript : `<span style="opacity:0.6;">${{interimTranscript}}</span>`);
                            
                            container.scrollTop = container.scrollHeight;
                        }}
                    }};
                    rec.start();
                }}
            </script>
        """, height=530)

    with col_side:
        st.markdown("### 📊 Analiz")
        st.error(f"🔴 {st.session_state.ik_name} (Kırmızı)")
        st.info(f"🔵 {st.session_state.aday_name} (Mavi)")
        st.divider()
        if st.button("🛑 Mülakatı Bitir", type="primary", use_container_width=True):
            st.session_state.page = "report"
            st.rerun()

elif st.session_state.page == "report":
    st.success("Mülakat Raporu Hazırlandı.")
    st.button("Dashboard'a Dön", on_click=lambda: st.session_state.update({"page": "setup"}))
