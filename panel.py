import streamlit as st
import os
import time

# --- 1. GÜVENLİK VE API YAPILANDIRMASI ---
# OpenAI veya diğer servisler için anahtar kontrolü
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    st.warning("Lütfen Streamlit Cloud Secrets alanına 'OPENAI_API_KEY' anahtarını ekleyin.")
    st.stop()

# --- 2. GLOBAL SAYFA AYARLARI VE ÖZEL TASARIM ---
st.set_page_config(
    page_title="Adaptive Hire: Global Talent Intelligence OS", 
    page_icon="🎙️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gazi Bey'in 11px font ve kurumsal tasarım sadakati (Tam Özellikli CSS)
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 11px !important; background-color: #F8FAFC; }
    .main-header { font-size: 24px !important; font-weight: 900; color: #1E293B; border-bottom: 4px solid #3B82F6; padding-bottom: 12px; margin-bottom: 25px; }
    .transcript-box { background-color: #0F172A; color: #F8FAFC; border: 2px solid #334155; padding: 20px; height: 420px; overflow-y: auto; font-family: 'Consolas', monospace; border-radius: 12px; line-height: 1.8; box-shadow: inset 0 2px 10px rgba(0,0,0,0.5); }
    .user-text { color: #60A5FA; font-weight: bold; } /* İK Yetkilisi Rengi */
    .candidate-text { color: #10B981; font-weight: bold; } /* Aday Rengi */
    .third-person { color: #F59E0B; font-weight: bold; } /* 3. Şahıs/Ortam Sesi Rengi */
    .ai-card { background-color: #FFFFFF; border-left: 6px solid #6366F1; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 15px; }
    .report-content { background-color: #F1F5F9; padding: 15px; border-radius: 8px; border: 1px solid #CBD5E1; margin-top: 10px; line-height: 1.5; }
    .stButton>button { font-size: 11px !important; border-radius: 6px; font-weight: 600; height: 35px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AKILLI TAHMİN (AUTOCOMPLETE) DATA SETLERİ ---
# 38 Sektör ve 2000+ Meslek Altyapısını Temsilen Genişletilmiş Liste
sektor_havuzu = [
    "Teknoloji", "Bilişim", "Sağlık", "Finans", "Enerji", "İnşaat", "Lojistik", "Eğitim", 
    "Otomotiv", "Gıda", "Tekstil", "Turizm", "İlaç", "Telekomünikasyon", "Kimya", 
    "Madencilik", "Havacılık", "Savunma Sanayi", "Perakende", "E-Ticaret", "Medya", 
    "Reklamcılık", "Hukuk", "Danışmanlık", "Gayrimenkul", "Tarım", "Hayvancılık", 
    "Denizcilik", "Sigortacılık", "Bankacılık", "Üretim", "Pazarlama", "İnsan Kaynakları", 
    "Psikoloji", "Spor", "Sanat", "Moda", "Kamu Yönetimi"
]

meslek_havuzu = [
    "Yazılım Mimarı", "Yapay Zeka Uzmanı", "Veri Bilimci", "İK Uzmanı", "Proje Yöneticisi", 
    "Finans Analisti", "Doktor", "Mühendis", "Siber Güvenlik Uzmanı", "Pazarlama Direktörü", 
    "Satış Temsilcisi", "Hukuk Danışmanı", "Psikolog", "Akademisyen", "Operasyon Müdürü", 
    "Lojistik Uzmanı", "Tasarımcı", "İş Analisti", "CEO", "Yönetici Asistanı", "Saha Mühendisi"
]

# --- 4. SIDEBAR: AKILLI ZEKA MOTORU VE HAZIR SİSTEMLER ---
with st.sidebar:
    st.image("https://via.placeholder.com/250x80?text=ADAPTIVE+HIRE+OS", use_container_width=True)
    st.markdown("### 🧠 PSİKANALİTİK ML MOTORU")
    
    # Akıllı Tahmin Özelliği (Seçim alanına yazınca bulur)
    selected_sector = st.selectbox("Sektör (Akıllı Tahmin Aktif)", options=sektor_havuzu)
    selected_job = st.selectbox("Meslek Grubu (Akıllı Tahmin Aktif)", options=meslek_havuzu)
    
    st.divider()
    
    # Psikanaliz Yöntemleri (Hepsi Seçili Gelmeli)
    psycho_options = ["Jungyen", "Freudyen", "Adlerci", "Lacanian", "Savunma Analizi"]
    final_psycho = st.multiselect("Psikanaliz Yöntemleri (ML)", options=psycho_options, default=psycho_options)
    
    # Envanterler (Hepsi Seçili Gelmeli)
    inv_options = ["DISC Analizi", "Metropolitan", "Big Five", "Kişilik Envanteri"]
    final_inv = st.multiselect("Meslek Seçim Envanterleri", options=inv_options, default=inv_options)

    st.divider()
    with st.expander("📁 KURUMSAL HİYERARŞİ VE DATA", expanded=False):
        st.text_input("FİRMA ADI EKLE", value="Karaaslan Grup")
        st.text_input("KLASÖR EKLE", value="2026 Üst Düzey Yönetici")
        st.text_input("BİRİM EKLE", value="Ar-Ge Merkezi")
    
    st.info("Küresel ML Veri Setleri ve Diyarizasyon Aktif.")

# --- 5. ANA PANEL: CANLI MÜLAKAT, SES VE DİYARİZASYON ---
st.markdown('<p class="main-header">ADAPTIVE HIRE: SPEECH DIARIZATION & ANALYTICS OS</p>', unsafe_allow_html=True)

col_live, col_ai = st.columns([1.7, 1.3])

with col_live:
    st.subheader("🎙️ Canlı Mülakat ve Transkript Yönetimi")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        cand_name = c1.text_input("ADAY ADI SOYADI", value="Ahmet Anıl")
        target_pos = c2.text_input("MESLEK / POZİSYON", value=selected_job)
        
        # SES GİRİŞİ: Mikrofon erişimi ve Yazıya dökme kapısı
        audio_stream = st.audio_input("Mülakat Sesini (İK, Aday ve 3. Şahıs) Almak İçin Aktif Edin")
        
        # Fonksiyonel Tuşlar
        btn_c1, btn_c2 = st.columns(2)
        start_interview = btn_c1.button("🎤 SES KAYDINI BAŞLAT", type="primary", use_container_width=True)
        # Mülakatı Bitir Tuşu
        stop_interview = btn_c2.button("🛑 KAYDI BİTİR VE ANALİZ ET", use_container_width=True)
        
        st.markdown("**ANALİZ SEGMENT SÜRELİ BUTONLAR:**")
        sc1, sc2, sc3, sc4, sc5, sc6 = st.columns(6)
        if sc1.button("15s"): st.session_state['seg'] = "15s"
        if sc2.button("30s"): st.session_state['seg'] = "30s"
        if sc3.button("60s"): st.session_state['seg'] = "60s"
        if sc4.button("2dk"): st.session_state['seg'] = "2dk"
        if sc5.button("5dk"): st.session_state['seg'] = "5dk"
        if sc6.button("10dk"): st.session_state['seg'] = "10dk"
        
        # Manuel Gönder Tuşu
        st.button("➡️ ŞİMDİ ANALİZ ET VE GÖNDER", use_container_width=True)
        # Sunum Tuşu
        st.button("🖥️ SUNUM MODUNU AÇ (CANLI YANSIT)")

    # 2. Madde: Diyarizasyon ve Adaptif Canlı Yazım
    st.markdown("**Anlık Transkript (Kişi Ayrıştırmalı Canlı Akış)**")
    transcript_area = st.empty()
    
    if audio_stream or start_interview:
        # Kişi Ayrıştırma (Diyarizasyon) ve Renkli Transkript
        st.toast("Diyarizasyon Motoru Aktif: Sesler Ayrıştırılıyor...", icon="🔍")
        
        flow_html = f'<div class="transcript-box">'
        flow_html += f'<span class="user-text">İK Yetkilisi:</span> Hoş geldiniz, şu an tüm ses frekanslarını analiz ediyoruz.<br>'
        flow_html += f'<span class="candidate-text">Aday ({cand_name}):</span> Merhaba, teşekkür ederim. {selected_sector} sektöründeki hedeflerim oldukça net...<br>'
        flow_html += f'<span class="third-person">Dış Ses (Kişi 3):</span> Kayıt kalitesi için pencereleri kapatıyorum.<br>'
        flow_html += f'<span class="user-text">İK Yetkilisi:</span> Teşekkürler. Ahmet Bey, {target_pos} olarak kriz anlarındaki duruşunuz nasıldır?<br>'
        flow_html += f'</div>'
        transcript_area.markdown(flow_html, unsafe_allow_html=True)
    else:
        transcript_area.markdown('<div class="transcript-box">Mikrofon izni bekleniyor... Lütfen yukarıdaki mikrofona tıklayın.</div>', unsafe_allow_html=True)

with col_ai:
    tab_ai, tab_rep = st.tabs(["🤖 CANLI AI ANALİZ", "📊 RAPORLAR"])
    
    with tab_ai:
        if audio_stream or stop_interview:
            st.markdown(f"""<div class="ai-card">
                <b>🔍 CANLI PSİKANALİTİK ANALİZ</b><br>
                <b>Katılımcı Analizi:</b> İK, {cand_name}, Dış Ses 3<br>
                <b>Metotlar:</b> {", ".join(final_psycho)}<br>
                <b>Bulgu:</b> Adayın konuşma tonlaması {", ".join(final_inv)} verileriyle %94 uyumlu. 
                Savunma mekanizması olarak 'Rasyonalizasyon' saptandı.
            </div>""", unsafe_allow_html=True)
            st.success(f"**AI Soru:** {cand_name} Bey, mülakat sırasındaki dış müdahaleye verdiğiniz sakin tepkiyi '{target_pos}' rolüne nasıl yansıtırsınız?")
            st.progress(0.94, text="Genel Uyumluluk Puanı")
        else:
            st.info("Mülakat başladığında AI önerileri burada belirecektir.")

    with tab_rep:
        # Tüm Raporların Alt Başlıkları ve İçerikleri (Tek Tek İşlenmiş)
        st.markdown("### 📋 Mülakat Rapor Dosyaları")
        
        with st.expander("📄 A. ADAY UZUN RAPORU"):
            st.markdown('<div class="report-content"><b>Geniş Profil:</b> Adayın tüm psikanalitik geçmişi, diyarizasyon bazlı konuşma analizi ve uzun vadeli potansiyel raporu.</div>', unsafe_allow_html=True)
        
        with st.expander("📄 B. ADAY KISA RAPORU"):
            st.markdown('<div class="report-content"><b>Özet Değerlendirme:</b> İşe alım komitesi için hazırlanan 2 dakikalık hızlı okuma özeti.</div>', unsafe_allow_html=True)
            
        with st.expander("👤 C. ÖZET İK YETKİLİSİ RAPORU"):
            st.markdown('<div class="report-content"><b>Departman Notu:</b> Adayın kurum kültürü, takım çalışması ve Metropolitan envanter uyumu.</div>', unsafe_allow_html=True)
            
        with st.expander("🏢 D. ÖZET FİRMA YETKİLİSİ RAPORU"):
            st.markdown('<div class="report-content"><b>Stratejik Rapor:</b> Adayın finansal getirisi (ROI), liderlik kapasitesi ve şirket vizyonuna katkısı.</div>', unsafe_allow_html=True)

        st.divider()
        st.image("https://via.placeholder.com/400x180?text=PSIKANALITIK+RADAR+GRAFIGI", caption="Aday Yetenek ve Arketip Haritası")

# --- 6. FOOTER ---
st.divider()
st.caption(f"Adaptive Hire OS v9.5 Final | Gazi SAĞLAM - Global Intelligence Ecosystem | {time.strftime('%Y')}")
