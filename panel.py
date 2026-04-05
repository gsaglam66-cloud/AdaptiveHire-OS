import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Adaptive Hire | Operasyon", layout="wide")

# Üst Panel (Bakiye ve Durum)
st.title("🛠️ İK Operasyon Merkezi")
c1, c2 = st.columns(2)
c1.metric("Kalan Kullanım Kredisi", "2,450 Seans")
c2.info("💰 **Sistem Notu:** Birim Satış: $3.00 | Üretim Maliyeti: $0.25")

st.divider()

# Mülakat Alanı
st.subheader("🎙️ Canlı Aday Değerlendirme")
col_sol, col_sag = st.columns([2, 1])

with col_sol:
    st.markdown("**Sistem Tarafından Üretilen Stratejik Soru:**")
    st.warning("Teknik projelerinizde hız ve kalite arasındaki dengeyi nasıl kuruyorsunuz?")
    
    # İK Süper Güç Butonları
    st.write("---")
    if st.button("✅ Analizi Onayla ve Raporla ($3.00)"):
        st.success("Analiz tamamlandı. Aday DNA'sı sisteme işlendi.")
        st.balloons()
        
    if st.button("🗑️ Hatalı Analizi Sil (Kredi İade Et)"):
        st.error("Kayıt imha edildi. 1 Kredi hesabınıza geri yüklendi.")

with col_sag:
    st.write("**Aday Yetkinlik Radarı**")
    # Radar Grafiği (Görsel Zenginlik)
    fig = go.Figure(go.Scatterpolar(
      r=[80, 90, 70, 85],
      theta=['Hız','Disiplin','Odak','Teknik'],
      fill='toself'
    ))
    st.plotly_chart(fig, use_container_width=True)
