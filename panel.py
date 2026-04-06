import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components
import random

# --- AI CONFIG ---
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AdaptiveHire - Precise Audio OS", layout="wide", initial_sidebar_state="expanded")

# --- PROFESYONEL TERMİNAL CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #f8fafc; }
    .ah-card { background: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; }
    
    /* Transkript Alanı */
    #chat-container { 
        height: 550px; overflow-y: auto; padding: 25px; 
        background: #020617; border-radius: 15px; border: 1px solid #1e293b;
        display: flex; flex-direction: column; gap: 15px;
    }
    
    /* İK UZMANI - KIRMIZI (SOL) */
    .ik-row { display: flex; justify-content: flex-start; width: 100%; }
    .ik-bubble { 
        background: #450a0a; border-left: 4px solid #ef4444; color: #fecaca;
        padding: 12px 18px; border-radius: 0 15px 15px 15px; max-width: 75%;
        box-shadow: 4px 4px 10px rgba(0,0,0,0.3);
    }

    /* ADAY - MAVİ (SAĞ) */
    .aday-row { display: flex; justify-content: flex-end; width: 100%; }
    .aday-bubble { 
        background: #1e3a8a; border-right: 4px solid #3b82f6; color: #dbeafe;
        padding: 12px 18px; border-radius: 15px 0 15px 15px; max-width: 75%;
        text-align: right; box-shadow: -4px 4px 10px rgba(0,0,0,0.3);
    }
    
    .label { font-size: 0.7rem; font-weight: bold; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "setup"
if 'ik_name' not in st.session_state: st.session_state.ik_name = "İK UZMANI"
if 'aday_name' not in st.session_state: st.session_state.aday_name = "ADAY"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#3b82f6;'>AdaptiveHire</h2>", unsafe_allow_html=True)
    st.session_state.ik_name = st.text_input("İK İsmi", st.session_state.ik_name)
    st.session_state.aday_name = st.text_input("Aday İsmi", st.session_state.aday_name)
    if st.button("🏠 Menüye Dön", use_container_width=True):
        st.session_state.page = "setup"
        st.rerun()

# --- FLOW ---
if st.session_state.page == "setup":
    st.subheader("Mülakat Sistemi")
    st.markdown('<div class="ah-card">', unsafe_allow_html=True)
    st.radio("Segment Süresi", ["15 sn", "30 sn", "1 dk", "2 dk", "5 dk"], index=1, horizontal=True)
    if st.button("🔴 Mülakatı Başlat", type="primary", use_container_width=True):
        st.session_state.page = "live"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "live":
    c1, c2 = st.columns([2.5, 1])
    
    with c1:
        # GELİŞMİŞ JS: KİLİTLEME VE SIFIR TEKRAR MANTIĞI
        components.html(f"""
            <div id="chat-container" style="background:#020617; height:550px; overflow-y:auto; padding:20px; display:flex; flex-direction:column; gap:15px; font-family:sans-serif;">
            </div>
            
            <script>
                const ik_name = "{st.session_state.ik_name}";
                const aday_name = "{st.session_state.aday_name}";
                const chatContainer = document.getElementById('chat-container');
                
                const Rec = window.webkitSpeechRecognition || window.SpeechRecognition;
                if(Rec) {{
                    const r = new Rec();
                    r.lang = 'tr-TR'; r.continuous = true; r.interimResults = true;
                    
                    let lastFinalText = "";

                    r.onresult = (event) => {{
                        let interim = "";
                        for (let i = event.resultIndex; i < event.results.length; i++) {{
                            let transcript = event.results[i][0].transcript.trim();
                            
                            if (event.results[i].isFinal) {{
                                if(transcript === lastFinalText) return; // Tekrarı blokla
                                lastFinalText = transcript;
                                
                                // Analiz: Kim konuşuyor?
                                let textLower = transcript.toLowerCase();
                                let isIK = textLower.includes('?') || textLower.includes('mi') || textLower.includes('neden') || textLower.includes('anlat');
                                
                                createBubble(transcript, isIK);
                            }}
                        }}
                    }};

                    function createBubble(text, isIK) {{
                        const row = document.createElement('div');
                        row.className = isIK ? 'ik-row' : 'aday-row';
                        row.style = "display:flex; width:100%; justify-content:" + (isIK ? 'flex-start' : 'flex-end') + "; margin-bottom:15px;";
                        
                        const bubble = document.createElement('div');
                        const color = isIK ? '#450a0a' : '#1e3a8a';
                        const border = isIK ? 'border-left:4px solid #ef4444' : 'border-right:4px solid #3b82f6';
                        const textColor = isIK ? '#fecaca' : '#dbeafe';
                        const textAlign = isIK ? 'left' : 'right';
                        const label = isIK ? ik_name : aday_name;
                        const labelColor = isIK ? '#ef4444' : '#3b82f6';

                        bubble.style = `background:${{color}}; ${{border}}; color:${{textColor}}; padding:12px 18px; border-radius:12px; max-width:75%; text-align:${{textAlign}}; font-family:sans-serif;`;
                        bubble.innerHTML = `<div style="color:${{labelColor}}; font-size:0.7rem; font-weight:bold; margin-bottom:5px;">${{label}}</div>` + text;
                        
                        row.appendChild(bubble);
                        chatContainer.appendChild(row);
                        chatContainer.scrollTop = chatContainer.scrollHeight;
                    }}
                    
                    r.start();
                }}
            </script>
        """, height=580)

    with c2:
        st.markdown("### 🛠️ Canlı Kontrol")
        st.markdown(f"🔴 **{st.session_state.ik_name}**")
        st.markdown(f"🔵 **{st.session_state.aday_name}**")
        st.divider()
        st.text_area("Anlık Notlar", placeholder="Adayın yetkinlik notlarını buraya girin...")
        if st.button("🛑 Mülakatı Bitir", type="primary", use_container_width=True):
            st.session_state.page = "report"
            st.rerun()

elif st.session_state.page == "report":
    st.title("Mülakat Tamamlandı")
    st.button("Yeni Mülakata Başla", on_click=lambda: st.session_state.update({"page":"setup"}))
