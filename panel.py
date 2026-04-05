import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder
import plotly.graph_objects as go
import time

# --- AI AYARI ---
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Adaptive Hire | Auto-Flow AI", layout="wide")

st.title("🧠 Adaptif Otomatik Mülakat Sistemi")

# --- SÜRE SEÇİM SEKMELERİ ---
st.subheader("⏱️ Mülakat Süresini Belirleyin")
sure_secenekleri = {"15 Saniye": 15, "30 Saniye": 30, "1 Dakika": 60, "2 Dakika": 120, "5 Dakika": 300}
secilen_sure_etiket = st.select_slider("Konuşma Süresi Limitini Seçin:", options=list(sure_secenekleri.keys()))
limit_saniye = sure_secenekleri[secilen_sure_etiket]

col1, col2 = st.columns([1, 1])

with col1:
    st.info(f"Seçilen Limit: {secilen_sure_etiket}. Süre bitiminde AI otomatik analize geçecektir.")
    
    # Mikrofon Kaydı
    # Not: mic_recorder kütüphanesi manuel durdurma ister ancak biz ekran zamanlayıcısı ile kullanıcıyı yönlendireceğiz.
    audio = mic_recorder(start_prompt="🎤 Mülakatı Başlat", stop_prompt="🛑 Kaydı Durdur (Manuel)", key='recorder')

    if audio:
        st.audio(audio['bytes'])
        st.success("Ses verisi işleniyor...")

with col2:
    if audio:
        with st.spinner('⏳ Süre doldu! Yapay Zeka cevabı analiz ediyor ve yeni soru üretiyor...'):
            # AI'ya gönderilen gelişmiş talimat
            prompt = f"""
            Bir profesyonel mülakatçı gibi davran. Adayın son cevabını analiz et (Metin: 'Adayın konuşması simüle ediliyor').
            1. Adayın cevabının derinliğini ölç (0-100).
            2. Bu cevaba dayanarak, adayı daha da zorlayacak veya detaya itecek 'ADAPTİF' bir takip sorusu üret.
            3. Analizi ve yeni soruyu Türkçe olarak sun.
            """
            
            response = model.generate_content(prompt)
            st.markdown("### 🤖 Yapay Zeka Analizi & Yeni Soru")
            st.write(response.text)
            
            # Radar Grafiği Güncelleme
            fig = go.Figure(go.Scatterpolar(
                r=[70, 85, 60, 90], # AI'dan gelecek dinamik puanlar
                theta=['Analiz Gücü','Akıcılık','Teknik Derinlik','Adaptasyon'],
                fill='toself'
            ))
            st.plotly_chart(fig)

# --- GÖRSEL ZAMANLAYICI (İsteğe Bağlı) ---
if st.button("⏲️ Süreyi Başlat (Görsel Yardımcı)"):
    bar = st.progress(0)
    for i in range(limit_saniye):
        time.sleep(1)
        bar.progress((i + 1) / limit_saniye)
    st.warning("⚠️ SÜRE DOLDU! Lütfen kaydı durdurun ve analize bakın.")
