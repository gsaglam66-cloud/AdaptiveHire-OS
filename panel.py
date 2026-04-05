import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go

# --- AI AYARI (Buraya Kendi API Anahtarını Yapıştır) ---
API_KEY = "BURAYA_ALDIĞIN_API_KEYİ_YAPIŞTIR"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Adaptive Hire | AI Core", layout="wide")

st.title("🧠 AI Destekli Aday Analiz Merkezi")

# Kullanıcı Girişi (Adayın Cevabı)
aday_cevabi = st.text_area("Adayın Cevabını Buraya Yapıştırın:", placeholder="Örn: Projelerimde önce planlama yaparım, sonra ekip koordinasyonuna odaklanırım...")

if st.button("🚀 AI Analizini Başlat"):
    if aday_cevabi:
        with st.spinner('Yapay Zeka Adayı İnceliyor...'):
            # AI'ya gönderdiğimiz gizli talimat (Prompt Engineering)
            prompt = f"Bir İK uzmanı gibi davran. Şu aday cevabını analiz et: '{aday_cevabi}'. Analiz sonucunda adaya Hız, Disiplin, Odak ve Teknik becerileri için 0-100 arası puan ver ve kısa bir yorum yap. Format: Hız:X, Disiplin:X, Odak:X, Teknik:X"
            
            response = model.generate_content(prompt)
            st.success("Analiz Tamamlandı!")
            
            # Sonuçları Göster
            st.markdown(f"### 📋 AI Değerlendirmesi")
            st.write(response.text)
            
            # Radar Grafiği için Örnek Veri (Burayı daha sonra otomatik parse edeceğiz)
            fig = go.Figure(go.Scatterpolar(
              r=[85, 70, 90, 65], # Bu rakamlar AI'dan gelen verilere göre değişecek
              theta=['Hız','Disiplin','Odak','Teknik'],
              fill='toself'
            ))
            st.plotly_chart(fig)
    else:
        st.warning("Lütfen önce bir aday cevabı girin.")
