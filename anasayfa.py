import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Adaptive Hire | Enterprise", layout="wide")

# Başlık ve Görsel Tasarım
st.markdown("<h1 style='text-align: center; color: #0071e3;'>Mülakat Maliyetlerinizi %94 Azaltın</h1>", unsafe_allow_html=True)
st.write("---")

# ROI (Kazanç) Tablosu
st.subheader("📊 Operasyonel Karşılaştırma Analizi")
col1, col2 = st.columns(2)

with col1:
    st.error("❌ Geleneksel Yöntem")
    st.write("- Aday Başı Maliyet: **1.750 ₺ ($50)**")
    st.write("- Analiz Süresi: **45 Dakika**")
    st.write("- İnsan Hatası Payı: **Yüksek**")

with col2:
    st.success("✅ Adaptive Hire OS")
    st.write("- Aday Başı Maliyet: **105 ₺ ($3.00)**")
    st.write("- Analiz Süresi: **2 Saniye**")
    st.write("- İnsan Hatası Payı: **Sıfır (Kontrollü AI)**")

st.divider()

# Fiyat Çıpası
st.info("💡 **Kurumsal Teklif:** 1.000 adaylık alımlarda birim fiyat 105 ₺'den başlar. Tasarrufunuz yıllık 1.6 Milyon ₺ üzerindedir.")

if st.button("Hemen Demo Randevusu Al"):
    st.balloons()
    st.write("Harika! Uzmanlarımız sizinle iletişime geçecek.")
