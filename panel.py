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

st.set_page_config(page_title="AdaptiveHire - Dual Audio AI", layout="wide", initial_sidebar_state="expanded")

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
    .chat-container { height: 450px; overflow-y: auto; padding: 20px; background: #f8fafc; border-radius: 15px; border: 1px solid #e2e8f0; }
    .msg { margin-bottom: 15px; padding: 10px 15px; border-radius: 10px; line-height: 1.5; }
    .ik-msg { background: #eff6ff; border-left: 5px solid #2563eb; color: #1e3a8a; }
    .aday-msg { background: #ffffff; border-left: 5px solid #10b981; color: #064e3b; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .speaker-name { font-weight: bold; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 4px; display: block; }
    
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
if 'is_paused' not in st.session_state: st.session_state.is_paused = False

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#2563eb;'>AdaptiveHire</h2>", unsafe_allow_html=True)
    st.session_state.ik_name = st.text_input("Kendi İsminiz (İK)", st.session_state.ik_name)
    st.session_state.aday_name = st.text_input("Aday İsmi (Biliniyorsa)", st.session_state.aday_name)
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
        st.write("**ÇALIŞMA MODU**")
        st.session_state.view_mode = st.radio("Mod", ["Chat", "Sunum", "Otonom Link"], horizontal=True, label_visibility="collapsed")
        
        st.write("<br>**SEGMENT SÜRESİ** (Çoktan Seçmeli)", unsafe_allow_html=True)
        st.radio("Süre", ["15 sn", "30 sn", "1 dk", "2 dk", "5 dk"], index=1, horizontal=True, label_visibility="collapsed")
        
        st.write("<br>**ANALİZ TİPLERİ**", unsafe_allow_html=True)
        st.multiselect("Envanterler", ["DISC", "Metropolitan", "Duygu Analizi"], default=["DISC"])
        
        st.divider()
        if st.button("Mülakatı Başlat →", type="primary", use_container_width=True):
            st.session_state.page = "live"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "live":
    st.markdown(f"### 🎙️ Canlı Görüşme Paneli | {st.session_state.view_mode} Modu")
    
    col_main, col_side = st.columns([2.5, 1])
    
    with col_main:
        if st.session_state.view_mode == "Sunum":
            st.markdown(f'<div class="presentation-slide"><div class="speaker-name" style="color:#3b82f6">MEVCUT SORU</div><div style="font-size:2.2rem; font-weight:bold;">{st.session_state.aday_name}, bize kariyer hedeflerinden bahseder misin?</div></div>', unsafe_allow_html=True)
        else:
            # Karşılıklı Transkript Alanı (Çift Kanal Simulasyonu)
            st.markdown('<div class="chat-container" id="chat-box">', unsafe_allow_html=True)
            
            components.html(f"""
                <div id="display"></div>
                <script>
                    const ik_name = "{st.session_state.ik_name}";
                    const aday_name = "{st.session_state.aday_name}";
                    const Recognition = window.webkitSpeechRecognition || window.SpeechRecognition;
                    
                    if(Recognition) {{
                        const rec = new Recognition();
                        rec.lang = 'tr-TR'; rec.continuous = true; rec.interimResults = true;
                        
                        rec.onresult = (event) => {{
                            let text = "";
                            for (let i = event.resultIndex; i < event.results.length; i++) {{
                                text = event.results[i][0].transcript;
                                let isFinal = event.results[i].isFinal;
                                
                                // Basit bir 'uzunluk' mantığıyla kimin konuştuğunu tahmin etme simulasyonu
                                // Gerçek projede iki ayrı mikrofon girişi veya diarization servisi kullanılır
                                let speaker = (text.length % 2 === 0) ? ik_name : aday_name;
                                let style = (text.length % 2 === 0) ? "ik-msg" : "aday-msg";
                                
                                document.getElementById('display').innerHTML += 
                                    '<div class="msg ' + style + '">' +
                                    '<span class="speaker-name">' + speaker + ':</span>' + text + '</div>';
                            }}
                            window.scrollTo(0,document.body.scrollHeight);
                        }};
                        rec.start();
                    }}
                </script>
            """, height=400)
            st.markdown('</div>', unsafe_allow_html=True)

    with col_side:
        st.markdown("### 🛠️ Canlı Kontrol")
        if st.button("⏸️ Ara Ver / Devam Et", use_container_width=True):
            st.session_state.is_paused = not st.session_state.is_paused
            st.rerun()
            
        st.write("**Veri Müdahalesi**")
        st.slider("Adayın Enerji Seviyesi", 0, 100, 80)
        
        with st.expander("📝 Notlar", expanded=True):
            st.text_area("Görüşme notu...", height=100)
            
        st.divider()
        if st.button("🛑 Mülakatı Bitir", type="primary", use_container_width=True):
            st.session_state.page = "report"
            st.rerun()

elif st.session_state.page == "report":
    st.markdown("# 📑 Mülakat Analiz Raporu")
    st.info(f"İK Uzmanı: {st.session_state.ik_name} | Aday: {st.session_state.aday_name}")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="ah-card"><h4>Diyalog Özeti</h4><p>Toplam 12 dakika süren görüşmede konuşma oranı %40 İK - %60 Aday olarak gerçekleşmiştir.</p></div>', unsafe_allow_html=True)
    with c2:
        fig = go.Figure(go.Scatterpolar(r=[80, 70, 90, 85], theta=['Uyum','Teknik','İletişim','Enerji'], fill='toself'))
        st.plotly_chart(fig)
    
    if st.button("Yeni Mülakat"):
        st.session_state.page = "setup"
        st.rerun()
