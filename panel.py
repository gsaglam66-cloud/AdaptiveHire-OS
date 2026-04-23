import streamlit as st
import os

# --- API KEY YAPILANDIRMASI ---
# Bu bölümdeki isimlerin Secrets alanıyla birebir eşleşmesi gerekir.
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    st.warning("Lütfen Streamlit Cloud Secrets alanına 'OPENAI_API_KEY' anahtarını ekleyin.")
    st.stop()

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Adaptive Hire: Talent Intelligence OS",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ARAYÜZ TASARIMI (11px Sade Tasarım) ---
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
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: KURUMSAL PANEL ---
with st.sidebar:
    st.image("https://via.placeholder.com/150x50?text=Adaptive+Hire", use_container_width=True)
    st.markdown("### Kurumsal Panel")
    
    with st.expander("📁 Veri Yapılandırma", expanded=True):
        folder_name = st.text_input("Klasör Adı")
        company_name = st.text_input("Firma Adı")
        unit_name = st.text_input("Birim")
        
        if st.button("Yapıyı Kaydet"):
            st.success(f"{folder_name} Kaydedildi.")

# --- ANA EKRAN ---
st.markdown('<p class="main-header">Mülakat Asistanı & Analiz Paneli</p>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    with st.container(border=True):
        st.markdown("**Aktif Mülakat Alanı**")
        candidate = st.text_input("Aday Adı Soyadı")
        if st.button("Asistanı Başlat"):
            st.info(f"{candidate} için mülakat süreci başlatılıyor...")

with col2:
    st.markdown("**Hızlı Raporlama**")
    st.table({"Aday": ["Örnek Aday"], "Durum": ["Beklemede"]})

st.divider()
st.caption("Adaptive Hire OS - Talent Intelligence OS")
