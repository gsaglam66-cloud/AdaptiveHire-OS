import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components
import random
import string

# --- AI AYARI ---
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AdaptiveHire - Smooth Audio AI", layout="wide", initial_sidebar_state="expanded")

# --- GELİŞMİŞ CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #fcfdfe; }
    .ah-card { background: white; padding: 25px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 20px; }
    
    /* Segment Butonları */
    div[data-testid="stHorizontalBlock"] .stRadio > div { gap: 10px; }
    .stRadio label {
        background: white !important; border: 1px solid #cbd5e1 !important;
        padding: 8px 18px !important; border-radius: 8px !important; font-weight: 500;
    }

    /* Transkript Balonları Tasarımı */
    .chat-container { height: 480px; overflow-y: auto; padding: 20px; background: #f8fafc; border-radius: 15px; border: 1px solid #e2e8f0; }
    .msg { margin-bottom: 12px; padding: 12px 18px; border-radius: 12px; line-height: 1.6; font-size: 1.05rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05); animation: fadeIn 0.3s ease; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
    
    .ik-msg { background: #eff6ff; border-left: 5px solid #2563eb; color: #1e3a8a; align-self: flex-start; }
    .aday-msg { background: #ffffff; border-left: 5px solid #10b981; color: #064e3b; align-self: flex-end; }
    .speaker-name { font-weight: bold; font-size: 0.8rem; text-transform: uppercase; margin-bottom: 4px; display: block; opacity: 0.7; }
    
    .presentation-slide {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: white; padding: 80px; border-radius: 20px; text-align: center;
        min-height: 400px; display: flex; flex-direction: column; justify-content: center;
        border: 4px solid #3b82f6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "setup"
if 'view_mode' not in st.session_state: st.session_state.view_mode = "Chat"
if 'ik_name' not in st.session_state: st.session_state.ik_name = "İK UZMANI"
if 'aday_name' not in st.session_state: st.session_state.aday_name = "ADAY"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#2563eb;'>AdaptiveHire</h2>", unsafe_allow_html=True)
    st.session_state.ik_name = st.text_input("İK İsmi", st.session_state.ik_name)
    st.session_state.aday_name = st.text_input("Aday İsmi", st.session_state.aday_name)
    st.divider()
    if st.button("🏠 Ana Menü", use_container_width=True):
        st.session_state.page = "setup"
        st.rerun()

# --- ANA AKIŞ ---
if st.session_state.page == "setup":
    st.subheader("Mülakat Yapılandırması")
    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.markdown('<div class="ah-card">', unsafe_allow_html=True)
        st.write("**GÖRÜNÜM MODU**")
        st.session_state.view_mode = st.radio("Mod", ["Chat", "Sunum", "Otonom Link"], horizontal=True, label_visibility="collapsed")
        
        st.write("<br>**SEGMENT SÜRESİ**", unsafe_allow_html=True)
        st.radio("Süre", ["15 sn", "30 sn", "1 dk", "2 dk", "5 dk"], index=1, horizontal=True, label_visibility="collapsed")
        
        st.divider()
        if st.button("Mülakatı Başlat →", type="primary", use_container_width=True):
            st.session_state.page = "live"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "live":
    st.markdown(f"### 🎙️ Canlı Görüşme | {st.session_state.view_mode}")
    col_main, col_side = st.columns([2.5, 1])
    
    with col_main:
        if st.session_state.view_mode == "Sunum":
            st.markdown(f'<div class="presentation-slide"><div class="speaker-name" style="color:#3b82f6">SORU</div><div style="font-size:2.5rem; font-weight:bold;">{st.session_state.aday_name}, bu pozisyon için seni en çok ne heyecanlandırıyor?</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="chat-container" id="chat-box">', unsafe_allow_html=True)
            # TEKRARLARI ÖNLEYEN GÜNCELLENMİŞ JS (Sadece Final Sonuçları Alır)
            components.html(f"""
                <div id="display" style="display:flex; flex-direction:column;"></div>
                <script>
                    const ik_name = "{st.session_state.ik_name}";
                    const aday_name = "{st.session_state.aday_name}";
                    const Recognition = window.webkitSpeechRecognition || window.SpeechRecognition;
                    
                    if(Recognition) {{
                        const rec = new Recognition();
                        rec.lang = 'tr-TR'; 
                        rec.continuous = true; 
                        rec.interimResults = false; // TEKRARI ÖNLEYEN KRİTİK AYAR
                        
                        rec.onresult = (event) => {{
                            for (let i = event.resultIndex; i < event.results.length; i++) {{
                                if (event.results[i].isFinal) {{
                                    let text = event.results[i][0].transcript;
                                    
                                    // Basit speaker tahmini (Sırayla değişen mantık)
                                    let isIK = (document.querySelectorAll('.msg').length % 2 === 0);
                                    let speaker = isIK ? ik_name : aday_name;
                                    let style = isIK ? "ik-msg" : "aday-msg";
                                    
                                    const msgDiv = document.createElement('div');
                                    msgDiv.className = 'msg ' + style;
                                    msgDiv.innerHTML = '<span class="speaker-name">' + speaker + '</span>' + text;
                                    document.getElementById('display').appendChild(msgDiv);
                                    
                                    // Otomatik aşağı kaydır
                                    window.scrollTo(0, document.body.scrollHeight);
                                }}
                            }}
                        }};
                        rec.start();
                    }}
                </script>
            """, height=450)
            st.markdown('</div>', unsafe_allow_html=True)

    with col_side:
        st.markdown("### 🎛️ Kontrol")
        st.slider("Canlı Puan (Teknik)", 0, 100, 75)
        st.text_area("Notlar", height=150, placeholder="Mülakat notlarını buraya yazın...")
        st.divider()
        if st.button("🛑 Mülakatı Bitir", type="primary", use_container_width=True):
            st.session_state.page = "report"
            st.rerun()

elif st.session_state.page == "report":
    st.markdown("# 📑 Mülakat Raporu")
    st.write("Mülakat başarıyla tamamlandı.")
    if st.button("Yeniden Başla"):
        st.session_state.page = "setup"
        st.rerun()
