import streamlit as st

st.set_page_config(page_title="Adaptive Hire | Premium AI", layout="wide")

# --- NEXHIRE STYLE CSS (Görsel Tasarım Kodları) ---
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #0071e3;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 25px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #005bbd;
        transform: scale(1.05);
    }
    .roi-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #0071e3;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ÜST BÖLÜM (HERO SECTION) ---
col1, col2 = st.columns([2, 1])

with col1:
    st.title("🚀 İşe Alımda Adaptif Zeka Dönemi")
    st.subheader("Mülakatları Otomatize Edin, Maliyetleri %94 Düşürün.")
    st.write("Nexthire ve NLCortex altyapısıyla güçlendirilmiş Adaptive Hire, adayların sadece söylediklerini değil, potansiyellerini de ölçer.")
    if st.button("Ücretsiz Demo Başlat"):
        st.balloons()

with col2:
    # Buraya bir görsel veya ikon gelebilir
    st.image("https://img.icons8.com/clouds/500/artificial-intelligence.png")

st.divider()

# --- ÖZELLİKLER (FEATURES) ---
st.markdown("### ✨ Üstün Adaptif Özellikler")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""<div class='roi-card'>
    <h4>🧠 Bilişsel Analiz</h4>
    <p>Adayın mantık yürütme hızını gerçek zamanlı ölçer.</p>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown("""<div class='roi-card'>
    <h4>🎭 Duygu Tanıma</h4>
    <p>Ses tonu ve kelime seçimlerinden stres seviyesini belirler.</p>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown("""<div class='roi-card'>
    <h4>📊 Veri Odaklı Karar</h4>
    <p>Adayları nesnel puanlarla birbirleriyle kıyaslar.</p>
    </div>""", unsafe_allow_html=True)

# --- FİYAT ÇIPASI ---
st.info("💡 Stratejik Not: Manuel mülakat maliyeti 1.750 ₺ iken, Adaptive Hire ile sadece 105 ₺ ($3).")
