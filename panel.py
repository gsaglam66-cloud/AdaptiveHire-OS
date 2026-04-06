import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components
import random

# --- AI AYARI ---
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AdaptiveHire - Intelligent Diarization", layout="wide", initial_sidebar_state="expanded")

# --- CSS (Değişmedi) ---
st.markdown("""
    <style>
    .stApp { background-color: #fcfdfe; }
    .ah-card { background: white; padding: 25px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 20px; }
    .chat-container { height: 500px; overflow-y: auto; padding: 20px; background: #f8fafc; border-radius: 15px; border: 1px solid #e2e8f0; display: flex; flex-direction: column; }
    .msg { margin-bottom: 12px; padding: 12px 18px; border-radius: 12px; max-width: 80%; line-height: 1.6; animation: fadeIn 0.3s ease; }
    .ik-msg { background: #eff6ff; border-left: 5px solid #2563eb; color: #1e3a8a; align-self: flex-start; }
    .aday-msg { background: #ffffff; border-left: 5px solid #10b981; color: #064e3b; align-self: flex-end; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .speaker-name { font-weight: bold; font-size: 0.75rem; text-transform: uppercase; margin-bottom: 4px; display: block; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "setup"
if 'ik_name' not in st.session_state: st.session_state.ik_name = "İK UZMANI"
if 'aday_name' not in st.session_state: st.session_state.aday_name = "ADAY"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#2563eb;'>AdaptiveHire</h2>", unsafe_allow_html=True)
    st.session_state.ik_name = st.text_input("İK Uzmanı İsmi", st.session_state.ik_name)
    st.session_state.aday_name = st.text_input("Aday İsmi", st.session_state.aday_name)
    st.divider()
    if st.button("🏠 Ana Menü", use_container_width=True):
        st.session_state.page = "setup"
        st.rerun()

# --- ANA AKIŞ ---
if st.session_state.page == "setup":
    st.subheader("Mülakat Kurulumu")
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown('<div class="ah-card">', unsafe_allow_html=True)
        st.write("**ÇALIŞMA MODU**")
        st.radio("Mod", ["Chat", "Sunum", "Otonom"], horizontal=True, label_visibility="collapsed")
        
        st.write("<br>**SEGMENT SÜRESİ** (Çoktan Seçmeli)", unsafe_allow_html=True)
        st.radio("Süre", ["15 sn", "30 sn", "1 dk", "2 dk", "5 dk"], index=1, horizontal=True, label_visibility="collapsed")
        
        st.divider()
        if st.button("Mülakatı Başlat →", type="primary", use_container_width=True):
            st.session_state.page = "live"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "live":
    st.markdown(f"### 🎙️ Canlı Görüşme: {st.session_state.ik_name} vs {st.session_state.aday_name}")
    
    col_main, col_side = st.columns([2.5, 1])
    
    with col_main:
        st.markdown('<div class="chat-container" id="chat-box">', unsafe_allow_html=True)
        
        # GÜNCELLENMİŞ JS: Akıllı Kişi Tanıma Algoritması
        components.html(f"""
            <div id="display" style="display:flex; flex-direction:column;"></div>
            <script>
                const ik_name = "{st.session_state.ik_name}";
                const aday_name = "{st.session_state.aday_name}";
                const Recognition = window.webkitSpeechRecognition || window.SpeechRecognition;
                
                let lastSpeaker = null;

                if(Recognition) {{
                    const rec = new Recognition();
                    rec.lang = 'tr-TR'; rec.continuous = true; rec.interimResults = false;
                    
                    rec.onresult = (event) => {{
                        for (let i = event.resultIndex; i < event.results.length; i++) {{
                            if (event.results[i].isFinal) {{
                                let text = event.results[i][0].transcript.trim().toLowerCase();
                                let currentSpeaker = "";
                                
                                // AKILLI ANALİZ: Soru ekleri, giriş kelimeleri veya bağlam analizi
                                // 1. Eğer cümle soru ekiyle bitiyorsa veya "neden, nasıl, anlatır mısın" içeriyorsa %90 İK'dır.
                                if (text.endsWith('mu') || text.endsWith('mi') || text.endsWith('mısınız') || 
                                    text.includes('neden') || text.includes('anlat') || text.includes('hoş geldiniz')) {{
                                    currentSpeaker = ik_name;
                                }} 
                                // 2. Eğer "yaptım, çalıştım, mezunuyum, yeteneğim" gibi ifadeler varsa %90 Adaydır.
                                else if (text.includes('yaptım') || text.includes('çalıştım') || text.includes('deneyim') || text.includes('mezun')) {{
                                    currentSpeaker = aday_name;
                                }}
                                // 3. Belirsiz durumlarda mülakat akışını (son konuşanı) baz al
                                else {{
                                    currentSpeaker = (lastSpeaker === ik_name) ? aday_name : ik_name;
                                }}

                                lastSpeaker = currentSpeaker;
                                let style = (currentSpeaker === ik_name) ? "ik-msg" : "aday-msg";
                                
                                const msgDiv = document.createElement('div');
                                msgDiv.className = 'msg ' + style;
                                msgDiv.innerHTML = '<span class="speaker-name">' + currentSpeaker + '</span>' + text;
                                document.getElementById('display').appendChild(msgDiv);
                                
                                window.scrollTo(0, document.body.scrollHeight);
                            }}
                        }}
                    }};
                    rec.start();
                }}
            </script>
        """, height=480)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_side:
        st.markdown("### 🎛️ Yönetici Paneli")
        st.info("Sistem konuşma içeriğinden kimin konuştuğunu analiz ediyor.")
        if st.button("🛑 Mülakatı Bitir", type="primary", use_container_width=True):
            st.session_state.page = "report"
            st.rerun()

elif st.session_state.page == "report":
    st.markdown("# 📑 Mülakat Raporu")
    st.button("Yeniden Başla", on_click=lambda: st.session_state.update({"page": "setup"}))
