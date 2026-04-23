import streamlit as st
import os
import time

# --- 1. GÜVENLİK & API ---
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    st.warning("Lütfen Secrets alanına 'OPENAI_API_KEY' ekleyin.")
    st.stop()

# --- 2. SAYFA AYARLARI & ÖZEL TASARIM ---
st.set_page_config(page_title="Adaptive Hire OS", page_icon="🎯", layout="wide")

# 11px font hassasiyeti ve profesyonel mülakat arayüzü
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 11px !important; background-color: #FDFDFD; }
    .main-header { font-size: 20px !important; font-weight: 700; color: #0F172A; border-bottom: 2px solid #3B82F6; padding-bottom: 10px; }
    .transcript-box { background-color: #000000; color: #00FF00; border: 1px solid #1E293B; padding: 15px; height: 250px; overflow-y: scroll; font-family: 'Courier New', monospace; border-radius: 8px; }
    .ai-card { background-color: #F1F5F9; border-left: 5px solid #3B82F6; padding: 15px; border-radius: 8px; }
    .stButton>button { font-size: 11px !important; height: 38px; border-radius: 6px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: İK UZMANI YÖNETİM PANELİ ---
with st.sidebar:
    st.image("https://via.placeholder.com/200x60?text=ADAPTIVE+HIRE", use_container_width=True)
    st.markdown("### 🛠 KURUMSAL YÖNETİM")
    
    with st.expander("📁 VERİ & DATA YAPISI", expanded=True):
        st.text_input("KLASÖR EKLE", value="2026 Teknik Kadro")
        st.text_input("FİRMA ADI EKLE", value="Karaaslan Grup")
        st.text_input("BİRİM EKLE", value="Yazılım Geliştirme")
        st.button("YAPIYI KAYDET")

    st.divider()
    # İK YETKİLİSİ SEGMENT SEÇİMİ (İstediğiniz 2. madde)
    st.markdown("### ⏱️ ANALİZ SEGMENTİ")
    segment_time = st.selectbox("Analiz Periyodu Seçin", 
                                ["15 Saniye", "30 Saniye", "60 Saniye", "2 Dakika", "5 Dakika", "10 Dakika"])
    
    # Saniyeye çevirme mantığı
    time_map = {"15 Saniye": 15, "30 Saniye": 30, "60 Saniye": 60, "2 Dakika": 120, "5 Dakika": 300, "10 Dakika": 600}
    target_time = time_map[segment_time]

    st.info(f"Oturum: gazisaglam1@gmail.com")

# --- 4. ANA PANEL: CANLI MÜLAKAT ANALİZİ ---
st.markdown('<p class="main-header">ADAPTIVE HIRE: TALENT INTELLIGENCE OS (CANLI ANALİZ)</p>', unsafe_allow_html=True)

col_live, col_ai = st.columns([1.8, 1.2])

with col_live:
    st.subheader("🎙️ Mülakat ve Transkript")
    
    with st.container(border=True):
        c1, c2 = st.columns(2)
        candidate = c1.text_input("Aday Adı Soyadı", value="Ahmet Anıl")
        position = c2.text_input("Başvurulan Pozisyon", value="Yapay Zeka Uzmanı")
        
        # SES KAYIT TUŞU İLE BAŞLATMA (İstediğiniz 3. madde)
        btn_col1, btn_col2 = st.columns([1, 1])
        start_rec = btn_col1.button("🎤 SES KAYDINI BAŞLAT", type="primary", use_container_width=True)
        # MANUEL ANALİZ GÖNDERİMİ (İstediğiniz 4. madde)
        manual_send = btn_col2.button("➡️ ŞİMDİ ANALİZ ET (GÖNDER)", use_container_width=True)

    # Transkript Ekranı
    st.markdown("**Canlı Transkript Akışı**")
    transcript_placeholder = st.empty()
    status_placeholder = st.empty()

    if start_rec:
        status_placeholder.error("🔴 Kayıt Alınıyor ve Transkript İşleniyor...")
        
        # Simülasyon Akışı
        full_text = ">> Sistem: Bağlantı kuruldu. Ses yakalanıyor...\n"
        for s in range(1, target_time + 1):
            time.sleep(1)
            if s == 3: full_text += ">> Aday: Merhaba, ben son projelerimde Streamlit ve LLM mimarileri üzerine çalıştım...\n"
            if s == 10: full_text += ">> Aday: Özellikle büyük veri setlerinin anlık analizinde adaptif yaklaşımlar sergiliyorum.\n"
            
            transcript_placeholder.markdown(f'<div class="transcript-box">{full_text}</div>', unsafe_allow_html=True)
            
            # Segment süresine ulaşıldığında veya Manuel Gönder tıklandığında (Simülasyon gereği burada kontrol ediyoruz)
            if s == target_time:
                st.session_state['analysis_ready'] = True
                break

with col_ai:
    st.subheader("🤖 AI Soru & Analiz Önerisi")
    
    # Analiz tetiklendiğinde görünecek alan
    if 'analysis_ready' in st.session_state or manual_send:
        with st.container():
            st.markdown(f"""
            <div class="ai-card">
                <b>🔍 SEGMENT ANALİZİ ({segment_time}):</b><br>
                Adayın 'Adaptif Yaklaşımlar' ve 'LLM Mimarileri' konusundaki teknik terminolojisi yüksek bulundu. 
                Sektörel deneyimi hakkında tutarlı veriler sağlıyor.
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("**💡 İK YETKİLİSİ İÇİN ÖNERİLEN SORULAR:**")
            st.info("1. Adaptif yaklaşımlarınızda hangi algoritma kütüphanelerini tercih ediyorsunuz?")
            st.info("2. Projelerinizde veri güvenliğini nasıl optimize ettiniz?")
            
            st.markdown("**📊 ANLIK PUANLAMA**")
            st.progress(0.85, text="Teknik Uyumluluk: %85")
            st.progress(0.70, text="Kültür Uyumu: %70")
            
            if st.button("Raporu Klasöre Kaydet"):
                st.success(f"Analiz '{os.path.join('Karaaslan Grup', candidate)}' yoluna kaydedildi.")
    else:
        st.write("Analiz segmenti tamamlandığında veya 'Gönder' ok tuşuna bastığınızda yapay zeka önerileri burada görünecektir.")

# --- 5. FOOTER ---
st.divider()
st.caption("Adaptive Hire OS v2.5 | 'Gazi SAĞLAM - Talent Intelligence OS'")
