import streamlit as st

st.title("🤝 White Label İş Ortaklığı")
st.write("Kendi İK markanızı bizim altyapımızla kurun.")

col1, col2 = st.columns(2)
col1.metric("Sizin Alış Fiyatınız", "105 ₺")
col2.metric("Önerilen Satış Fiyatı", "875 ₺")

st.write("### Neden Ortak Olmalısınız?")
st.write("- %800 Kâr Marjı")
- "Kendi logonuz ve domain adresiniz."