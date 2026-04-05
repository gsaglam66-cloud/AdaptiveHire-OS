import streamlit as st

st.set_page_config(page_title="Adaptive Hire | Tasarruf Merkezi", layout="wide")

st.markdown("# 🚀 Mülakat Maliyetini %94 Düşürün")
st.write("Geleneksel mülakatlar pahalıdır. Adaptive Hire ile saniyeler içinde analiz yapın.")

# ROI Tablosu (Parayı gösteren kısım)
st.table({
    "Kriter": ["Birim Maliyet", "Hız", "Yıllık Tasarruf (1000 Aday)"],
    "Manuel Süreç": ["1.750 ₺", "45 Dakika", "0 ₺"],
    "Adaptive Hire": ["105 ₺ ($3)", "2 Saniye", "1.645.000 ₺"]
})

st.success("💡 Stratejik Not: Bu sistemle her mülakatta cebinizde 1.645 ₺ kalır.")