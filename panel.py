import streamlit as st
import time

# Sayfa Ayarları
st.set_page_config(page_title="Adaptive Hire OS", layout="wide", initial_sidebar_state="expanded")

# --- GELİŞMİŞ CSS: SIRI EFEKTİ & SİLİK YAZI STİLLERİ ---
st.markdown("""
    <style>
    /* Siri Halkası Animasyonu */
    .siri-container { display: flex; justify-content: center; align-items: center; height: 150px; margin: 20px 0; }
    .siri-sphere {
        width: 100px; height: 100px; border-radius: 50%;
        background: linear-gradient(45deg, #00d2ff, #3a7bd5, #ff00c1, #9d50bb);
        background-size: 400% 400%;
        animation: siri-wave 3s ease infinite, siri-glow 2s ease-in-out infinite alternate;
    }
    @keyframes siri-wave {
        0% { background-position: 0% 50%; transform: scale(1); }
        50% { background-position: 100% 50%; transform: scale(1.05); }
        100% { background-position: 0% 50%; transform: scale(1); }
    }
    @keyframes siri-glow {
        from { box-shadow: 0 0 20px rgba(58,123,213,0.4); }
        to { box-shadow: 0 0 50px rgba(255,0,193,0.6); }
    }
    
    /* Yan Menü Klasör Yapısı */
    .folder-label { color: #6b7280; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin-top: 10px; }
    
    /* Kart Tasarımı */
    .setup-card {
        background-color: white; padding: 30px; border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05); border: 1px solid #f0f0f0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SOL PANEL: ARŞİV VE HİYERARŞİ ---
with st.sidebar:
    st.markdown("### 📂 Kayıt Arşivi")
    
    # Kurum Klasörü
    with st.expander("🏢 Kurum Seçin...", expanded=True):
        # BURASI: Şamil Albayrak ismini silik bir yer tutucu yaptık
        st.markdown("<p class='folder-label'>Sorumlu Uzman:</p>", unsafe_allow_html=True)
        uzman_adi = st.text_input("", placeholder="Örn: Şamil Albayrak", label_visibility="collapsed")
        
        st.divider()
        st.markdown("<p class='folder-label'>Mülakat Yapılan Aday:</p>", unsafe_allow_html=True)
        st.text_input("", placeholder="Örn: Mehmet Can", label_visibility="collapsed")

    st.button("➕ Yeni Klasör Oluştur", use_container_width=True)

# --- ANA AKIŞ MANTIĞI ---
if 'mulakat_aktif' not in st.session_state:
    st.session_state.mulakat_aktif = False

if not st.session_state.mulakat_aktif:
    # 1. EKRAN: KURULUM (NLCortex Modu)
    st.title("🚀 Oturum Yapılandırması")
    st.write(f"Aktif Oturum: {uzman_adi if uzman_adi else 'Yeni Görüşme'}")

    col_left, col_right = st.columns([1.5, 1])
    
    with col_left:
        st.markdown('<div class="setup-card">', unsafe_allow_html=True)
        
        st.write("**⚙️ ADAPTİF ANALİZ SEGMENTİ**")
        s1, s2, s3, s4, s5 = st.columns(5)
        s1.button("15 sn")
        s2.button("30 sn")
        s3.button("1 dk")
        s4.button("5 dk")
        s5.button("10 dk")
        
        st.divider()
        st.write("**🎙️ GİRİŞ KAYNAĞI**")
        g1, g2 = st.columns(2)
        g1.button("🎤 Mikrofon")
        g2.button("🖥️ Sistem Sesi")
        
        st.divider()
        if st.button("CANLI MÜLAKATI BAŞLAT →", use_container_width=True):
            st.session_state.mulakat_aktif = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # 2. EKRAN: MÜLAKAT ODASI (SIRI MODU)
    col_info, col_main, col_stats = st.columns([1, 2, 1])

    with col_info:
        st.markdown("### 📋 Oturum")
        st.caption(f"Uzman: {uzman_adi if uzman_adi else 'Tanımlanmadı'}")
        st.divider()
        if st.button("🛑 Oturumu Sonlandır"):
            st.session_state.mulakat_aktif = False
            st.rerun()

    with col_main:
        st.markdown("<h2 style='text-align: center;'>Sistem Dinliyor...</h2>", unsafe_allow_html=True)
        
        # SIRI HALKASI
        st.markdown("<div class='siri-container'><div class='siri-sphere'></div></div>", unsafe_allow_html=True)
        
        st.divider()
        st.chat_message("assistant").write("Cevap bekleniyor... (Otomatik analiz 30sn sonra tetiklenecek)")

    with col_stats:
        st.markdown("### ⚡ AI Öngörüleri")
        st.metric("Duygu Kararlılığı", "%88")
        st.info("💡 Adayın teknik terminoloji kullanımı yüksek. Bir sonraki soruda pratik uygulama detaylarını isteyin.")
