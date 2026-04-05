import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components

# --- AI AYARI ---
# Kendi API anahtarını tırnak içine yapıştır
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Adaptive Hire OS", layout="wide", initial_sidebar_state="expanded")

# --- GELİŞMİŞ TASARIM VE SIRI ANIMASYONU ---
st.markdown("""
    <style>
    .stSidebar { background-color: #f0f2f6; }
    .setup-card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    
    /* Siri Halkası Animasyonu */
    .siri-container { display: flex; justify-content: center; height: 100px; margin: 10px 0; }
    .siri-sphere {
        width: 70px; height: 70px; border-radius: 50%;
        background: linear-gradient(45deg, #00d2ff, #3a7bd5, #ff00c1, #9d50bb);
        background-size: 400% 400%;
        animation: siri-pulse 2s infinite ease-in-out alternate;
    }
    @keyframes siri-pulse { from { transform: scale(1); box-shadow: 0 0 20px #3a7bd5; } to { transform: scale(1.2); box-shadow: 0 0 40px #ff00c1; } }
    
    /* Transkript Kutusu Tasarımı */
    #transcript-display {
        background-color: #1e1e1e; color: #00ff00; padding: 15px;
        border-radius: 10px; font-family: 'Courier New', monospace;
        height: 250px; overflow-y: auto; margin-top: 10px;
        line-height: 1.5; font-size: 14px;
    }
    .folder-label { color: #6b7280; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SOL PANEL: HİYERARŞİK ARŞİV MANTIĞI ---
with st.sidebar:
    st.markdown("### 📂 Kayıt Arşivi")
    with st.expander("🏢 Kurum Seçin...", expanded=True):
        st.markdown("<p class='folder-label'>Sorumlu Uzman:</p>", unsafe_allow_html=True)
        uzman = st.text_input("uzman_input", placeholder="Örn: Şamil Albayrak", label_visibility="collapsed")
        
        st.markdown("<p class='folder-label'>Aday İsmi:</p>", unsafe_allow_html=True)
        aday = st.text_input("aday_input", placeholder="Örn: Mehmet Can", label_visibility="collapsed")
    
    st.divider()
    st.button("➕ Yeni Klasör Oluştur", use_container_width=True)

# --- ANA AKIŞ KONTROLÜ ---
if 'mulakat_aktif' not in st.session_state:
    st.session_state.mulakat_aktif = False

if not st.session_state.mulakat_aktif:
    # --- 1. EKRAN: KURULUM (SETUP) ---
    st.title("🚀 Oturum Yapılandırması")
    col_l, col_r = st.columns([1.5, 1])
    
    with col_l:
        st.markdown('<div class="setup-card">', unsafe_allow_html=True)
        st.write("**⏱️ ADAPTİF ANALİZ SEGMENTİ (SÜRE)**")
        segment_sure = st.select_slider("Analiz periyodu seçin:", options=["15 sn", "30 sn", "1 dk", "2 dk", "5 dk", "10 dk"])
        
        st.divider()
        st.write("**🎙️ GİRİŞ KAYNAĞI**")
        g1, g2 = st.columns(2)
        g1.button("🎤 Sadece Mikrofon", use_container_width=True)
        g2.button("🖥️ Sistem Sesi", use_container_width=True)
        
        st.divider()
        if st.button("CANLI MÜLAKATI BAŞLAT →", use_container_width=True):
            st.session_state.mulakat_aktif = True
            st.session_state.current_segment = segment_sure
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_r:
        st.info("Ayarları tamamlayıp 'Başlat' butonuna bastığınızda mülakat odası aktifleşecektir.")
        st.image("https://cdn-icons-png.flaticon.com/512/3649/3649460.png", width=150)

else:
    # --- 2. EKRAN: CANLI MÜLAKAT ODASI ---
    st.header(f"🎙️ Görüşme: {aday if aday else 'Yeni Aday'}")
    
    c1, c2, c3 = st.columns([0.8, 2
