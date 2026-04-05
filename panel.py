import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder
import plotly.graph_objects as go

# --- AI AYARI ---
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" # Burayı güncellemeyi unutma!
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Adaptive Hire | Voice AI", layout="wide")

st.title("🎙️ AI Sesli Analiz ve Çoklu Dil Paneli")

col_sol, col_sag = st.columns([1, 1])

with col_sol:
    st.subheader("Adayı Dinle")
    st.write("Mikrofona tıkla ve adayın cevabını kaydet (Her dilde konuşabilir):")
    
    # Mikrofon Bileşeni
    audio = mic_recorder(start_prompt="🎤 Kaydı Başlat", stop_prompt="🛑 Kaydı Bitir", key='recorder')

if audio:
    # Burada normalde bir ses-metin servisi (Whisper vb.) kullanılır. 
    # Şimdilik entegrasyonu basitleştirmek için AI'ya ham metin analizi yaptırıyoruz.
    st.audio(audio['bytes'])
    st.success("Ses kaydı başarıyla alındı!")

# Manuel Giriş veya Ses Analiz Alanı
aday_metni = st.text_area("Analiz Edilecek Metin (Veya yukarıdaki sesi buraya yazın):")

if st.button("🚀 Derinlemesine AI Analizi Yap"):
    if aday_metni:
        with st.spinner('Yapay Zeka Çoklu Dil ve Karakter Analizi Yapıyor...'):
            # AI Talimatı: Dil ne olursa olsun Türkçe analiz etmesini istiyoruz
            prompt = f"""
            Aşağıdaki metni bir İK uzmanı gibi analiz et. 
            Metin hangi dilde olursa olsun sonucu Türkçe ver.
            Metin: '{aday_metni}'
            
            Lütfen şu formatta cevap ver:
            1. Genel Özet
            2. Güçlü Yönler
            3. Gelişim Alanları
            4. Puanlama (0-100): Hız, Disiplin, Teknik, Uyum
            """
            
            response = model.generate_content(prompt)
            st.markdown("### 📊 Stratejik Analiz Raporu")
            st.info(response.text)
            
            # Radar Grafiği
            fig = go.Figure(go.Scatterpolar(
                r=[80, 75, 90, 85], # Burası AI yanıtından çekilebilir
                theta=['Hız','Disiplin','Teknik','Uyum'],
                fill='toself',
                line_color='#0071e3'
            ))
            st.plotly_chart(fig)
    else:
        st.warning("Lütfen bir metin girin veya ses kaydı yapın.")
