import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components

# --- AI YAPILANDIRMASI ---
# API anahtarınızı buraya ekleyin
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Sayfa Ayarları
st.set_page_config(page_title="AdaptiveHire - AI Recruitment OS", layout="wide", initial_sidebar_state="expanded")

# --- KURUMSAL TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #fcfdfe; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #f1f5f9; }
    
    /* Segment Süreleri - Özel Çoktan Seçmeli Tasarımı */
    .stRadio > div { flex-direction: row !important; gap: 10px; }
    .stRadio label {
        background: white !important;
        border: 1px solid #cbd5e1 !important;
        padding: 8px 16px !important;
        border-radius: 8px !important;
        cursor: pointer;
        transition: 0.2s;
        font-size: 0.9rem;
    }
    .stRadio label:hover { border-color: #2563eb !important; background: #eff6ff !important; }
    
    /* Transkript ve Kartlar */
    .ah-card { background: white; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 20px; }
    #transcript-box { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; height: 450px; overflow-y: auto; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "setup"

# --- SIDEBAR: PROFİL YÖNETİMİ (Görsel 1 & 11) ---
with st.sidebar:
    st.markdown("<h2 style='color:#2563eb;'>AdaptiveHire</h2>", unsafe_allow_html=True)
    st.markdown("### 👤 Profil Yönetimi")
    
    with st.expander("📁 Klasörlerim", expanded=True):
        st.info("📂 IK Görüşmeleri Profili")
        st.write("📂 Teknik Değerlendirme")
    
    if st.button("➕ Yeni Görüşme Oluştur", use_container_width=True, type="primary"):
        st.session_state.page = "setup"
        st.rerun()

# --- ANA AKIŞ ---

# 1. EKRAN: OTURUM AYARLARI (Görsel 3, 13 & Çoktan Seçmeli Segmentler)
if st.session_state.page == "setup":
    st.subheader("Oturum Ayarları")
    col_config, col_preview = st.columns([1.5, 1])

    with col_config:
        st.markdown('<div class="ah-card">', unsafe_allow_html=True)
        
        st.write("**GÖRÜNÜM MODU**")
        m1, m2, m3 = st.columns(3)
        m1.button("💬 Chat", use_container_width=True)
        m2.button("♾️ Otonom", use_container_width=True)
        m3.button("🖥️ Sunum", use_container_width=True)
        
        st.write("<br>**SEGMENT SÜRESİ** (Çoktan Seçmeli)", unsafe_allow_html=True)
        # Çizgi yerine ayrı ayrı kutucuklar halinde seçim
        selected_seg = st.radio(
            "Süre Seçimi",
            options=["15 saniye", "20 saniye", "30 saniye", "1 dakika", "2 dakika", "5 dakika", "10 dakika"],
            index=2,
            horizontal=True,
            label_visibility="collapsed"
        )
        
        st.write("<br>**GİRİŞ KAYNAĞI**", unsafe_allow_html=True)
        g1, g2 = st.columns(2)
        g1.button("🎤 Sadece Mikrofon", use_container_width=True)
        g2.button("🖥️ Sistem Sesi", use_container_width=True)
        
        st.divider()
        if st.button("Mülakatı Başlat →", type="primary", use_container_width=True):
            st.session_state.page = "live"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_preview:
        st.write("**ÖNİZLEME**")
        st.markdown(f'<div class="ah
