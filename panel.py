import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder
import plotly.graph_objects as go

# --- AI AYARI ---
# Buraya kendi API anahtarını yapıştırmayı unutma!
API_KEY = "SENİN_API_KEYİN" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Sayfa Ayarları
st.set_page_config(page_title="Adaptive Hire OS", layout="wide")

# --- SIRI & TRANSKRIPT STİLLERİ ---
st.markdown("""
    <style>
    .siri-container { display: flex; justify-content: center; align-items: center; height: 120px; }
    .siri-sphere {
        width: 80px; height: 80px; border-radius: 50%;
        background: linear-gradient(45deg, #00d2ff, #3a7bd5, #ff00c1, #9d50bb);
        background-size: 400% 400%;
        animation: siri-wave 2s ease infinite alternate;
        box-shadow: 0 0 30px rgba(0,210,255,0.5);
    }
    @keyframes siri-wave { from { transform: scale(1); opacity: 0.8; } to { transform: scale(1.2); opacity: 1; } }
    
    .transcript-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 15px;
        height: 300px;
        overflow-y: auto;
        border: 1px solid #e0e0e0;
        font-family: 'Courier New', Courier, monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# --- PANEL AKIŞI ---
if 'mulakat_aktif' not in st.session_state:
    st.session_state.mulakat_aktif = False

if not st.session_state.mulakat_aktif:
    # --- KURULUM EKRANI (Önceki Adımlardaki Yapı) ---
    st.title("🚀 Oturum Yapılandırması")
    col1, col2 = st.columns([1,1])
    with col1:
        segment = st.selectbox("Adaptif Analiz Aralığı", ["15 Saniye", "30 Saniye", "1 Dakika", "5 Dakika", "10 Dakika"])
    if st.button("CANLI MÜLAKATI BAŞLAT"):
        st.session_state.mulakat_aktif = True
        st.session_state.segment_vakti = segment
        st.rerun()

else:
    # --- CANLI MÜLAKAT ODASI ---
    col_info, col_main, col_stats = st.columns([0.8, 2, 1])

    with col_info:
        st.markdown("### 📋 Oturum")
        st.caption(f"Aralık: {st.session_state.segment_vakti}")
        if st.button("🛑 Bitir"):
            st.session_state.mulakat_aktif = False
            st.rerun()

    with col_main:
        st.markdown("<div class='siri-container'><div class='siri-sphere'></div></div>", unsafe_allow_html=True)
        
        # SES KAYIT BİLEŞENİ (Canlı Dinleme)
        st.write("🎙️ **Sistem Dinliyor ve Çeviriyor...**")
        audio = mic_recorder(start_prompt="🎤 Dinlemeyi Başlat", stop_prompt="🛑 Duraklat", key='live_mic')
        
        # TRANSKRİPT ALANI
        st.markdown("#### 🗨️ Canlı Transkript")
        if audio:
            # Not: Gerçek hayatta burada ses-metin dönüşümü yapılır. 
            # Prototipte AI'ya ses verisinin geldiğini simüle ediyoruz.
            st.session_state.last_speech = "Aday: 'Yapay zeka modellerini veri setleriyle eğitiyorum...'" # Simülasyon
            
        st.markdown(f"<div class='transcript-box'>{st.session_state.get('last_speech', 'Ses bekleniyor...')}</div>", unsafe_allow_html=True)

    with col_stats:
        st.markdown("### 🤖 Adaptif Analiz")
        
        # SİSTEMİN ADAPTİF TEPKİSİ
        if audio:
            with st.spinner('Segment Analiz Ediliyor...'):
                # AI'dan Adaptif Soru İstiyoruz
                prompt = f"Mülakatta aday şunu dedi: '{st.session_state.get('last_speech')}'. Seçilen segment: {st.session_state.segment_vakti}. Bu cevaba göre adayı zorlayacak tek bir adaptif soru ve bir mülakatçı önerisi yaz."
                response = model.generate_content(prompt)
                
                st.success("🎯 Yeni Adaptif Soru")
                st.write(response.text)
                
                # Radar Grafiği
                fig = go.Figure(go.Scatterpolar(r=[80, 70, 90, 65], theta=['Hız','Odak','Teknik','Uyum'], fill='toself'))
                fig.update_layout(height=250, margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("İlk ses verisi geldiğinde adaptif öneriler burada belirecektir.")
