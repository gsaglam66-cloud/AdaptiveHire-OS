import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder
import plotly.graph_objects as go

# --- AI AYARI ---
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Adaptive Hire | Real-Time AI", layout="wide")

# --- CSS: Butonları ve Arayüzü Özelleştir ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    .critical-btn>button { background-color: #ff4b4b; color: white; border: none; }
    .analysis-box { background-color: #1e1e1e; padding: 20px; border-radius: 10px; border-left: 5px solid #0071e3; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 Canlı Adaptif Mülakat Asistanı")

# Üst Panel: Kontrol Mekanizması
col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1, 2, 1])

with col_ctrl1:
    st.subheader("⏱️ Otomatik Analiz Aralığı")
    periyot = st.selectbox("Sistem ne sıklıkla araya girsin?", 
                          ["15 Saniye", "30 Saniye", "1 Dakika", "2 Dakika", "5 Dakika"])

with col_ctrl2:
    st.subheader("🎙️ Canlı Dinleme")
    # Kayıt cihazı sürekli açık kalabilir
    audio = mic_recorder(start_prompt="🎤 Mülakatı Başlat (Dinlemeye Geç)", 
                         stop_prompt="🛑 Mülakatı Bitir", key='live_recorder')

with col_ctrl3:
    st.subheader("🚨 Manuel Komut")
    st.write("Kritik bir detay mı yakaladınız?")
    if st.button("🎯 ANLIK ANALİZ İSTE", help="Periyodu beklemeden son konuşmayı analiz eder."):
        st.session_state.force_analyze = True

# --- ANALİZ VE AKIŞ MANTIĞI ---
if audio or st.session_state.get('force_analyze', False):
    st.divider()
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown("<div class='analysis-box'>", unsafe_allow_html=True)
        with st.spinner(f'Yapay Zeka {periyot} aralığını veya manuel komutu işliyor...'):
            # Buradaki prompt, sistemin "asistan" rolünü pekiştirir
            prompt = f"""
            Şu an canlı bir mülakatın içerisindesin. 
            Mülakatçının seçtiği analiz aralığı: {periyot}.
            Gelen son konuşma verilerini analiz et:
            1. Adayın son cümlesindeki satır arası mesajları yakala.
            2. Mülakatçıya aday hakkında gizli bir ipucu ver (Örn: 'Aday teknik konuda özgüvenli ama ekip çalışmasında tereddütlü görünüyor').
            3. Derhal mülakatçının sorabileceği, adayı 'köşeye sıkıştıracak' veya 'derine inecek' yeni bir soru üret.
            Analizi profesyonel Türkçe ile yap.
            """
            
            # Simüle edilmiş yanıt (API'den gelecek)
            try:
                response = model.generate_content(prompt)
                st.write("### 🤖 AI Asistan Notu & Yeni Soru")
                st.info(response.text)
            except:
                st.error("API bağlantısı kontrol edilmeli.")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.write("📊 **Anlık Yetkinlik Skoru**")
        fig = go.Figure(go.Scatterpolar(
            r=[65, 80, 55, 70], 
            theta=['Dürüstlük','Teknik','Stres Yönetimi','Uyum'],
            fill='toself'
        ))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    # Manuel komut bayrağını sıfırla
    if st.session_state.get('force_analyze'):
        st.session_state.force_analyze = False
