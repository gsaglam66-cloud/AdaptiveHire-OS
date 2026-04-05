import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(page_title="Adaptive Hire | Enterprise Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- NLC & NEXTHIRE STYLE CSS ---
st.markdown("""
    <style>
    .stSidebar { background-color: #f0f2f6; border-right: 1px solid #d1d5db; }
    .folder-label { font-weight: bold; color: #4b5563; font-size: 0.85rem; margin-bottom: -10px; }
    .setup-card {
        background-color: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid #f3f4f6;
    }
    .segment-btn > div > button {
        border-radius: 12px !important;
        height: 45px;
        border: 1px solid #e5e7eb !important;
    }
    .start-btn > div > button {
        background-color: #2563eb !important;
        color: white !important;
        font-weight: bold !important;
        padding: 20px !important;
        border-radius: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SOL PANEL: HİYERARŞİK KLASÖR MANTIĞI ---
with st.sidebar:
    st.markdown("### 📂 Kayıt Arşivi")
    
    # 1. Seviye: Kurum Klasörü
    with st.expander("🏢 **TÜRKİYE TEKNOLOJİ A.Ş.**", expanded=True):
        # 2. Seviye: Çalışılacak Kişi (İK Sorumlusu)
        st.markdown("<p class='folder-label'>👤 İK Sorumlusu:</p>", unsafe_allow_html=True)
        ik_sorumlusu = st.selectbox("", ["Şamil ALBAYRAK", "Zeynep GÜNEŞ", "Caner DEMİR"], label_visibility="collapsed")
        
        st.divider()
        
        # 3. Seviye: Mülakat Yapılan Adaylar
        st.markdown("<p class='folder-label'>📝 Adaylar:</p>", unsafe_allow_html=True)
        st.button("📄 Aday: Mehmet CAN (Mühendis)", use_container_width=True)
        st.button("📄 Aday: Ayşe YILMAZ (Analist)", use_container_width=True)
        st.button("📄 Aday: Fatma GÖK (Tasarımcı)", use_container_width=True)

    st.button("➕ Yeni Kurum/Klasör Ekle", use_container_width=True)

# --- ANA EKRAN: OTURUM AYARLARI ---
st.title(f"🚀 Yeni Görüşme Başlat")
st.caption(f"Hiyerarşi: {ik_sorumlusu} > Yeni Aday Analizi")

col_left, col_right = st.columns([1.6, 1])

with col_left:
    st.markdown('<div class="setup-card">', unsafe_allow_html=True)
    
    st.subheader("🛠️ Oturum Yapılandırması")
    
    # Görünüm Modları
    st.write("**GÖRÜNÜM MODU**")
    m1, m2, m3 = st.columns(3)
    m1.button("💬 Chat Modu", use_container_width=True)
    m2.button("♾️ Otonom Akış", use_container_width=True)
    m3.button("🖥️ Sunum Paneli", use_container_width=True)
    
    # Giriş Kaynakları
    st.write("**🎤 GİRİŞ KAYNAĞI**")
    g1, g2 = st.columns(2)
    g1.button("🎤 Sadece Mikrofon", use_container_width=True)
    g2.button("🔊 Mikrofon + Sistem Sesi", use_container_width=True)
    
    # Segment Süreleri (İstediğin 5 ve 10 dk dahil)
    st.write("**⏱️ ADAPTİF ANALİZ SEGMENTİ (SÜRE)**")
    st.caption("Sistem bu süre dolduğunda otomatik olarak derin analiz üretir.")
    
    s1, s2, s3, s4 = st.columns(4)
    s1.button("15 sn", key="15s")
    s2.button("20 sn", key="20s")
    s3.button("30 sn", key="30s")
    s4.button("1 dk", key="1m")
    
    s5, s6, s7, s8 = st.columns(4)
    s5.button("2 dk", key="2m")
    s6.button("3 dk", key="3m")
    s7.button("5 dk", key="5m")  # Yeni Eklenen
    s8.button("10 dk", key="10m") # Yeni Eklenen
    
    st.divider()
    
    # BAŞLAT BUTONU
    st.markdown('<div class="start-btn">', unsafe_allow_html=True)
    if st.button("CANLI MÜLAKATI BAŞLAT →"):
        st.session_state.mulakat_basladi = True
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.write("**👁️ CANLI ÖNİZLEME PANELİ**")
    if st.session_state.get('mulakat_basladi', False):
        st.success("🟢 SİSTEM DİNLİYOR...")
        st.chat_message("assistant").write("Mülakat başladı. Lütfen adaya ilk soruyu yöneltin veya otonom modu bekleyin.")
        # Buraya anlık ses dalgası görseli veya simülasyonu gelecek
    else:
        st.info("Ayarları tamamlayıp 'Başlat' butonuna bastığınızda mülakat odası aktifleşecektir.")
        st
