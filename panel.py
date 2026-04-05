import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder
import plotly.graph_objects as go
from fpdf import FPDF # PDF kütüphanesini çağırdık

# --- AI AYARI ---
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Adaptive Hire | Pro Report", layout="wide")

st.title("🎙️ AI Sesli Analiz ve Kurumsal Raporlama")

# Aday Bilgileri (PDF için lazım)
aday_isim = st.text_input("Adayın Adı Soyadı:", placeholder="Örn: Ahmet Yılmaz")

# Ses ve Metin Girişi
audio = mic_recorder(start_prompt="🎤 Kaydı Başlat", stop_prompt="🛑 Kaydı Bitir", key='recorder')
aday_metni = st.text_area("Analiz Edilecek Metin:")

if st.button("🚀 Analizi Gerçekleştir ve Rapor Hazırla"):
    if aday_metni and aday_isim:
        with st.spinner('AI Rapor Hazırlıyor...'):
            prompt = f"Bir İK uzmanı gibi davran. Aday {aday_isim} için şu metni analiz et: '{aday_metni}'. Sonucu 'Özet', 'Güçlü Yönler' ve 'Gelişim Alanları' başlıklarıyla Türkçe ver."
            response = model.generate_content(prompt)
            analiz_sonucu = response.text
            
            st.markdown("### 📊 Analiz Önizleme")
            st.info(analiz_sonucu)

            # --- PDF OLUŞTURMA MANTIĞI ---
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="ADAPTIVE HIRE - ADAY DEGERLENDIRME RAPORU", ln=True, align='C')
            pdf.ln(10)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Aday: {aday_isim}", ln=True)
            pdf.ln(5)
            # AI sonucunu PDF'e yazdırıyoruz (Türkçe karakter sorunu olmaması için latinize edilir veya standart font kullanılır)
            pdf.multi_cell(0, 10, txt=analiz_sonucu.encode('latin-1', 'ignore').decode('latin-1'))
            
            # PDF'i Belleğe Al
            pdf_output = pdf.output(dest='S').encode('latin-1')
            
            st.download_button(
                label="📥 Profesyonel PDF Raporu İndir",
                data=pdf_output,
                file_name=f"{aday_isim}_Mulakat_Raporu.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("Lütfen aday ismini ve analiz metnini doldurun.")
