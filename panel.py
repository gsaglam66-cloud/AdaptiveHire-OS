import streamlit as st

# Sayfa Yapısı
st.set_page_config(page_title="NLC Cortex | Adaptive Hire", layout="wide", initial_sidebar_state="expanded")

# --- NLC STYLE CSS ---
st.markdown("""
    <style>
    /* Sol Menü (Past Interviews) */
    .stSidebar { background-color: #f8f9fa; border-right: 1px solid #dee2e6; }
    
    /* Ana Kart Tasarımı */
    .setup-card {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
    }
    
    /* Segment Butonları Tasarımı */
    div.stButton > button {
        border-radius: 8px;
        border: 1px solid #dee2e6;
        background-color: white;
        transition: 0.2s;
    }
    div.stButton > button:hover { border-color: #0071e3; color: #0071e3; }
    
    /* Başlat Butonu (Mavi) */
    .main-btn > div > button {
        background-color: #0071e3 !important;
        color: white !important;
        width: 100%;
        padding: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SOL MENÜ (Görüşme Geçmişi) ---
with st.sidebar:
    st.subheader("📁 Danışan Görüşmeleri")
    st.info("👤 Şamil ALBAYRAK\n\nKayıt Tarihi: 08.12.2025")
    st.button("➕ Yeni Görüşme Aç", use_container_width=True)
    st.divider()
    
    # Geçmiş Görüşme Listesi
    for i in range(9, 5, -1):
        with st.expander(f"📌 Görüşme {i}"):
            st.write("IK Görüşmeleri Profili")
            st.caption("Gelişmiş Tarama Uzmanı v2")

# --- ANA EKRAN (Oturum Ayarları) ---
st.header(f"Görüşme 9")

col_main, col_preview = st.columns([1.5, 1])

with col_main:
    st.markdown('<div class="setup-card">', unsafe_allow_html=True)
    st.subheader("Oturum Ayarları")
    st.caption("Başlamadan önce tercihlerinizi seçin")
    
    # 1. Görünüm Modu
    st.write("**GÖRÜNÜM MODU**")
    m1, m2, m3 = st.columns(3)
    m1.button("💬 Chat", use_container_width=True)
    m2.button("♾️ Otonom", use_container_width=True)
    m3.button("🖥️ Sunum", use_container_width=True)
    
    # 2. Giriş Kaynağı
    st.write("**GİRİŞ KAYNAĞI**")
    g1, g2 = st.columns(2)
    g1.button("🎤 Sadece Mikrofon", use_container_width=True)
    g2.button("📠 Mikrofon + Tab Sesi", use_container_width=True)
    
    g3, g4 = st.columns(2)
    g3.button("🖥️ Mikrofon + Sistem", use_container_width=True)
    g4.button("🤖 Toplantı Botu", use_container_width=True)
    
    # 3. Segment Süresi
    st.write("**⏱️ SEGMENT SÜRESİ**")
    st.caption("Ses kaydı bu süre dolduğunda otomatik olarak analiz edilip AI'ya gönderilir.")
    seg1, seg2, seg3, seg4, seg5 = st.columns(5)
    seg1.button("15 sn")
    seg2.button("20 sn")
    seg3.button("30 sn")
    seg4.button("1 dk")
    seg5.button("2 dk")
    
    st.divider()
    st.markdown('<div class="main-btn">', unsafe_allow_html=True)
    if st.button("Başla →"):
        st.switch_page("panel.py") # Buraya mülakatın başladığı sayfayı bağlayabiliriz
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_preview:
    st.write("**ÖNİZLEME**")
    st.image("https://cdn-icons-png.flaticon.com/512/2593/2593491.png", width=100)
    st.caption("Standart sohbet görünümü aktif.")
    # Sohbet simülasyonu
    st.chat_message("assistant").write("Merhaba, analiz için hazırım.")
    st.chat_message("user").write("...")
