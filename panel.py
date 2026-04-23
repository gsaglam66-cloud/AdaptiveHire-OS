import streamlit as st
import os

# --- API KEY YAPILANDIRMASI ---
# Streamlit Cloud üzerinde 'Settings > Secrets' kısmına eklediğiniz 
# OPENAI_API_KEY değerini çeker.
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    st.error("Lütfen Streamlit Cloud Secrets alanına 'OPENAI_API_KEY' anahtarını ekleyin.")
    st.stop()

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Adaptive Hire: Talent Intelligence OS",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ARAYÜZ TASARIMI (Sizin isteğinize göre: Sade ve 11px odaklı) ---
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-size: 11px !important;
        background-color: #F8F9FA;
    }
    .main-header {
        font-size: 18px !important;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 20px;
    }
    .stButton>button {
        font-size: 11px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: İK UZMANI YÖNETİM ALANI ---
with st.sidebar:
    st.image("https://via.placeholder.com/150x50?text=Adaptive+Hire", use_container_width=True)
    st.markdown("### Kurumsal Panel")
    
    # İK Uzmanı için Klasörleme Mantığı
    with st.expander("📁 Klasör Yapılandırma", expanded=True):
        folder_name = st.text_input("Yeni Klasör Adı")
        company_name = st.text_input("Firma Adı")
        unit_name = st.text_input("Çalışılan Birim")
        
        if st.button("Yapıyı Oluştur"):
            st.success(f"{folder_name} başarıyla oluşturuldu.")

    st.divider()
    st.info("Kullanıcı: gazisaglam1@gmail.com")

# --- ANA PANEL ---
st.markdown('<p class="main-header">Mülakat Asistanı & Veri Yönetimi</p>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Aktif Mülakat Alanı")
    # Mülakat ekleme adımları
    with st.container(border=True):
        st.markdown("**Yeni Mülakat Başlat**")
        candidate_name = st.text_input("Aday Adı Soyadı")
        interview_type = st.selectbox("Mülakat Tipi", ["Teknik", "Yetkinlik Bazlı", "Kültür Uyumu"])
        
        if st.button("Mülakat Asistanını Çalıştır"):
            st.write(f"{candidate_name} için mülakat asistanı hazırlandı...")

with col2:
    st.subheader("Hızlı Raporlama")
    # Daha sonra raporlamalar için data alanı
    st.write("Son 5 Mülakat Verisi")
    data_preview = {
        "Aday": ["Örnek Aday 1", "Örnek Aday 2"],
        "Durum": ["Analiz Edildi", "Beklemede"],
        "Skor": [85, "-"]
    }
    st.table(data_preview)

# --- ALT BİLGİ ---
st.markdown("---")
st.caption("Adaptive Hire OS - Yapay Zeka Destekli İK Yönetim Sistemi")
