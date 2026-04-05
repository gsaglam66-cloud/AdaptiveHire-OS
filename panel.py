import streamlit as st

st.title("🛠️ İK Operasyon Paneli")
st.sidebar.metric("Birim Fiyat", "105 ₺ ($3.00)")
st.sidebar.info("Gizli Maliyet: 8.75 ₺. Kârınız: 96 ₺")

st.subheader("🎙️ Canlı Mülakat ve Analiz")
st.info("Soru: Projelerinizde disiplin ve hızı nasıl dengeliyorsunuz?")

if st.button("✅ Analizi Onayla ve Raporla"):
    st.balloons()
    st.write("Rapor oluşturuldu. $3.00 bakiyeden düşüldü.")

if st.button("🗑️ Hatalı Kaydı Sil (Kredi İade)"):
    st.warning("İnsan Denetimi: Kayıt silindi, bakiye korundu.")