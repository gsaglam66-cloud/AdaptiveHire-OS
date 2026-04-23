import streamlit as st
import os

# --- 1. API KEY & GÜVENLİK YAPILANDIRMASI ---
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    st.warning("Lütfen Streamlit Cloud Secrets alanına 'OPENAI_API_KEY' anahtarını ekleyin.")
    st.stop()

# --- 2. SAYFA AYARLARI VE TASARIM ---
st.set_page_config(
    page_title="Adaptive Hire: Talent Intelligence OS",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sizin isteğiniz: Açık renkli arka plan ve 11px font büyüklüğü
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-size: 11px !important;
        background-color: #FDFDFD;
    }
    .main-header {
        font-size: 20px !important;
        font-weight: bold;
        color: #0F172A;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .stButton>button {
        font-size: 11px !important;
        border-radius: 5px;
    }
    .ik-box {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: İK UZMANI KURUMSAL PANEL ---
with st.sidebar:
    st.image("https://via.placeholder.com/200x60?text=ADAPTIVE+HIRE", use_container_width=True)
    st.markdown("### 🛠 KURUMSAL YÖNETİM")
    
    # Tam Klasörleme Mantığı
    with st.expander("📁 KLASÖR & DATA YAPISI", expanded=True):
        st.write("Yeni bir veri alanı tanımlayın:")
        folder_name = st.text_input("KLASÖR EKLE", placeholder="Örn: 2026 Teknik Kadro")
        company_name = st.text_input("FİRMA ADI EKLE", placeholder="Örn: Karaaslan Grup")
        unit_name = st.text_input("ÇALIŞILAN BİRİM EKLE", placeholder="Örn: Yazılım Geliştirme")
        
        if st.button("YAPIYI KAYDET VE OLUŞTUR"):
            st.success(f"Sistem hazırlandı: {folder_name}")

    st.divider()
    st.markdown("### 🤖 ASİSTAN AYARLARI")
    ai_mode = st.radio("Asistan Modu", ["Otonom Mülakat", "Soru Hazırlama", "Rapor Analizi"])
    
    st.info(f"Oturum: gazisaglam1@gmail.com")

# --- 4. ANA PANEL: MÜLAKAT ASİSTANI VE RAPORLAMA ---
st.markdown('<p class="main-header">ADAPTIVE HIRE: TALENT INTELLIGENCE OS</p>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎙️ Mülakat Asistanı Modülü")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            candidate_name = st.text_input("Aday Adı Soyadı")
        with c2:
            position = st.text_input("Pozisyon")
            
        interview_step = st.selectbox("Mülakat Adımı", [
            "MÜLAKAT ASİSTANI EKLE", 
            "TEKNİK MÜLAKAT BAŞLAT", 
            "YETKİNLİK ANALİZİ",
            "MÜLAKAT TAMAMLA"
        ])
        
        if st.button("MÜLAKAT BAŞLAT / ANALİZ ET"):
            if candidate_name:
                st.write(f"**{candidate_name}** için {interview_step} süreci başlatıldı...")
                st.progress(25)
                st.info("Yapay zeka sesli/yazılı veri toplama alanı aktif.")
            else:
                st.error("Lütfen aday ismi giriniz.")

with col2:
    st.subheader("📊 Veri & Raporlama")
    with st.container(border=True):
        st.write("Son Yapılan Mülakatlar")
        # Örnek raporlama datası
        report_data = {
            "Aday": ["Ahmet Anıl", "Örnek Aday"],
            "Birim": ["Yazılım", "İK"],
            "Puan": ["92", "84"],
            "Durum": ["Olumlu", "İncelemede"]
        }
        st.table(report_data)
        
        if st.button("DETAYLI RAPOR AL"):
            st.download_button("PDF Raporu İndir", "Örnek Veri", "rapor.txt")

# --- 5. ALT BİLGİ ---
st.divider()
st.markdown("""
    <div style='text-align: center; color: #94A3B8;'>
        Adaptive Hire OS © 2026 | Next Generation Recruitment Intelligence
    </div>
    """, unsafe_allow_html=True)
