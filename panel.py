import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components

# --- AI CONFIGURATION ---
API_KEY = "BURAYA_API_ANAHTARINI_YAZ" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Sayfa Ayarları
st.set_page_config(page_title="AdaptiveHire - AI Interview OS", layout="wide", initial_sidebar_state="expanded")

# --- GELİŞMİŞ KURUMSAL CSS (NLCortex Standartları) ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e0e0e0; min-width: 300px !important; }
    
    /* Kurumsal Beyaz Kartlar */
    .ah-card {
        background: white; padding: 30px; border-radius: 12px;
        border: 1px solid #eaedf2; box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 20px;
    }
    
    /* Segment Buton Stilleri (Slider yerine Net Yazı) */
    .segment-label { font-weight: 600; color: #475569; margin-bottom: 10px; display: block; }
    
    /* Transkript Ekranı (Beyaz ve Okunaklı) */
    #transcript-container {
        background: white; border: 1px solid #e2e8f0; border-radius: 12px;
        padding: 25px; height: 450px; overflow-y: auto;
        font-family: 'Inter', sans-serif; line-height: 1.8; color: #1e293b;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.01);
    }

    /* Sol Menü Sarı Kartlar */
    .side-item {
        background-color: #fffbe6; border: 1px solid #ffe58f;
        padding: 15px; border-radius: 8px; margin-bottom: 10px;
    }

    /* Mavi Başlat Butonu */
    .stButton>button { border-radius: 8px; height: 45px; transition: 0.3s; }
    .main-blue-btn button { background-color: #2563eb !important; color: white !important; width: 100%; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'step' not in st.session_state: st.session_state.step = "setup"

# --- SIDEBAR (Görsel 1 & 4 Hiyerarşisi) ---
with st.sidebar:
    st.markdown("<h2 style='color:#1e293b;'>AdaptiveHire</h2>", unsafe_allow_html=True)
    st.markdown("🔍 **Görüşme Ara...**")
    st.text_input("search", label_visibility="collapsed", placeholder="Aday ismi yazın...")
    
    if st.button("➕ Yeni Görüşme Aç", use_container_width=True, type="primary"):
        st.session_state.step = "setup"
        st.rerun()

    st.divider()
    st.markdown("<div class='side-item'><b>Görüşme #3</b><br><small>IK Görüşmeleri Profili</small></div>", unsafe_allow_html=True)
    st.markdown("<div class='side-item' style='background:white; border:1px solid #eee;'><b>Görüşme #2</b><br><small>Teknik Değerlendirme</small></div>", unsafe_allow_html=True)

# --- ANA PANEL ---

# 1. KURULUM EKRANI (Görsel 1 & 3 Birebir)
if st.session_state.step == "setup":
    st.subheader("Görüşme Ayarları")
    col_l, col_r = st.columns([1.2, 1])
    
    with col_l:
        st.markdown('<div class="ah-card">', unsafe_allow_html=True)
        st.markdown("### Oturum Ayarları")
        st.caption("Başlamadan önce tercihlerinizi seçin")
        
        st.markdown("<br><b>GÖRÜNÜM MODU</b>", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        m1.button("💬 Chat", use_container_width=True)
        m2.button("♾️ Otonom", use_container_width=True)
        m3.button("🖥️ Sunum", use_container_width=True)
        
        st.markdown("<br><b>GİRİŞ KAYNAĞI</b>", unsafe_allow_html=True)
        g1, g2 = st.columns(2)
        g1.button("🎤 Sadece Mikrofon", use_container_width=True)
        g2.button("🖥️ Mikrofon + Tab Sesi", use_container_width=True)
        
        # SEGMENT SÜRESİ (Yazılı ve Net Görünüm)
        st.markdown("<br><span class='segment-label'>⏱️ SEGMENT SÜRESİ</span>", unsafe_allow_html=True)
        # Çizgi hatasını önlemek için radyo butonu veya yatay buton seti:
        seg_choice = st.select_slider("", options=["15 saniye", "20 saniye", "30 saniye", "1 dakika", "2 dakika", "5 dakika"], value="30 saniye")
        
        st.divider()
        st.markdown('<div class="main-blue-btn">', unsafe_allow_html=True)
        if st.button("Başla →"):
            st.session_state.step = "live"
            st.session_state.seg_val = seg_choice
            st.rerun()
        st.markdown('</div></div>', unsafe_allow_html=True)

    with col_r:
