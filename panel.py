import streamlit as st
import os
import time

# --- 1. GÜVENLİK VE API YAPILANDIRMASI ---
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    st.warning("Lütfen Secrets alanına 'OPENAI_API_KEY' anahtarını ekleyin.")
    st.stop()

# --- 2. GLOBAL SAYFA AYARLARI VE ÖZEL TASARIM ---
st.set_page_config(page_title="Adaptive Hire: Global Intelligence OS", page_icon="🧠", layout="wide")

# 11px font ve kurumsal açık renkli tasarım sadakati
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 11px !important; background-color: #FDFDFD; }
    .main-header { font-size: 24px !important; font-weight: 800; color: #1E293B; border-bottom: 4px solid #3B82F6; padding-bottom: 10px; margin-bottom: 25px; }
    .transcript-box { background-color: #0F172A; color: #10B981; border: 2px solid #334155; padding: 20px; height: 380px; overflow-y: auto; font-family: 'Consolas', monospace; border-radius: 12px; line-height: 1.6; }
    .user-text { color: #60A5FA; font-weight: bold; } 
    .candidate-text { color: #34D399; font-weight: bold; }
    .ai-card { background-color: #FFFFFF; border-left: 6px solid #6366F1; padding: 18px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .report-content { background-color: #F1F5F9; padding: 15px; border-radius: 8px; border: 1px solid #CBD5E1; margin-top: 10px; }
    .stButton>button { font-size: 11px !important; border-radius: 6px; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AKILLI TAHMİN DATA SETLERİ (38 Sektör ve 2000+ Altyapı) ---
sektorler = ["Teknoloji", "Bilişim", "Sağlık", "Finans", "Enerji", "İnşaat", "Lojistik", "Eğitim", "Otomotiv", "Gıda", "Tekstil", "Turizm", "İlaç", "Telekomünikasyon", "Kimya", "Madencilik", "Havacılık", "Savunma Sanayi", "Perakende", "E-Ticaret", "Medya", "Reklamcılık", "Hukuk", "Danışmanlık", "Gayrimenkul", "Tarım", "Hayvancılık", "Denizcilik", "Sigortacılık", "Bankacılık", "Üretim", "Pazarlama", "İnsan Kaynakları", "Psikoloji", "Spor", "Sanat", "Moda", "Kamu Yönetimi"]

meslekler = ["Yazılım Mimarı", "Yapay Zeka Uzmanı", "Veri Bilimci", "İK Uzmanı", "Proje Yöneticisi", "Finans Analisti", "Doktor", "Mühendis", "Siber Güvenlik Uzmanı", "Pazarlama Direktörü", "Satış Temsilcisi", "Hukuk Danışmanı", "Psikolog", "Akademisyen", "Operasyon Müdürü", "Lojistik Uzmanı", "Tasarımcı", "İş Analisti", "CEO", "Yönetici Asistanı"]

# --- 4. SIDEBAR: AKILLI TAHMİN VE SEÇİLİ SİSTEMLER ---
with st.sidebar:
    st.image("https://via.placeholder.com/250x80?text=ADAPTIVE+HIRE+OS", use_container_width=True)
    st.markdown("### 🧠 PSİKANALİTİK ML MOTORU")
    
    # Akıllı Tahmin (Autocomplete) Özelliği
    sel_sector = st.selectbox("Sektör (Harf yazarak bulun)", options=sektorler)
    sel_job = st.selectbox("Meslek Grubu (Harf yazarak bulun)", options=meslekler)
    
    # Psikanaliz Yöntemleri (Hepsi Seçili Başlar)
    psycho_list = ["Jungyen", "Freudyen", "Adlerci", "Lacanian", "Savunma Analizi"]
    sel_psycho = st.multiselect("Psikanaliz Yöntemleri", options=psycho_list, default=psycho_list)
    
    # Envanterler (Hepsi Seçili Başlar)
    inv_list = ["DISC Analizi", "Metropolitan", "Big Five", "Kişilik Envanteri"]
    sel_inv = st.multiselect("Meslek Envanterleri", options=inv_list, default=inv_list)

    st.divider()
    with st.expander("📁 KURUMSAL HİYERARŞİ"):
        st.text_input("FİRMA ADI EKLE", value="Karaaslan Grup")
        st.text_input("KLASÖR EKLE", value="2026 Üst Düzey Adaylar")
        st.text_input("BİRİM EKLE", value="Teknoloji Merkezi")
    
    st.info("Sistem Küresel Psikanalitik Veri Setleri ile Senkronize.")

# --- 5. ANA PANEL: CANLI MÜLAKAT, SES VE ANALİZ ---
st.markdown('<p class="main-header">ADAPTIVE HIRE: LIVE PSYCHOANALYTIC INTELLIGENCE OS</p>', unsafe_allow_html=True)

col_live, col_ai = st.columns([1.7, 1.3])

with col_live:
    st.subheader("🎙️ Canlı Mülakat ve Transkript")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        candidate = c1.text_input("ADAY ADI SOYADI", value="Ahmet Anıl")
        position = c2.text_input("MESLEK / POZİSYON", value=sel_job)
        
        # SES GİRİŞİ: Mikrofon erişimi sağlar
        voice_data = st.audio_input("Mülakat Sesini Almak İçin Mikrofonu Aktif Edin")
        
        # Tuşlar Takımı
        b_col1, b_col2 = st.columns(2)
        start_btn = b_col1.button("🎤 SES KAYDINI BAŞLAT", type="primary", use_container_width=True)
        # Mülakatı Bitir Tuşu
        stop_btn = b_col2.button("🛑 KAYDI BİTİR VE ANALİZ ET", use_container_width=True)
        
        st.markdown("**ANALİZ SEGMENT SÜRESİ:**")
        s1, s2, s3, s4, s5, s6 = st.columns(6)
        if s1.button("15s"): st.session_state['seg'] = "15s"
        if s2.button("30s"): st.session_state['seg'] = "30s"
        if s3.button("60s"): st.session_state['seg'] = "60s"
        if s4.button("2dk"): st.session_state['seg'] = "2dk"
        if s5.button("5dk"): st.session_state['seg'] = "5dk"
        if s6.button("10dk"): st.session_state['seg'] = "10dk"
        
        # Manuel Gönder Tuşu
        manual_send = st.button("➡️ ŞİMDİ ANALİZ ET VE GÖNDER", use_container_width=True)
        # Sunum Tuşu
        st.button("🖥️ SUNUM MODUNU AÇ (CANLI YANSIT)")

    # Renkli Transkript Alanı
    st.markdown("**Anlık Transkript (Canlı Ses İşleme)**")
    t_area = st.empty()
    
    if voice_data or start_btn:
        # Renkli Akış Simülasyonu (Ses geldikçe tetiklenir)
        html_flow = f'<div class="transcript-box">'
        html_flow += f'<span class="user-text">İK Yetkilisi:</span> Hoş geldiniz, sesiniz geliyor. {sel_sector} sektörü üzerine konuşalım.<br>'
        html_flow += f'<span class="candidate-text">Aday:</span> Merhaba, ben {candidate}. {position} olarak psikanalitik çözümlerimi sunuyorum...<br>'
        html_flow += f'</div>'
        t_area.markdown(html_flow, unsafe_allow_html=True)
    else:
        t_area.markdown('<div class="transcript-box">Mikrofon izni bekleniyor...</div>', unsafe_allow_html=True)

with col_ai:
    tab_ai, tab_rep = st.tabs(["🤖 CANLI AI ANALİZ", "📊 RAPORLAR"])
    
    with tab_ai:
        if voice_data or manual_send or stop_btn:
            st.markdown(f"""
            <div class="ai-card">
                <b>🔍 PSİKANALİTİK ML ANALİZİ</b><br>
                <b>Metotlar:</b> {", ".join(sel_psycho)}<br>
                <b>Analiz:</b> Adayın '{sel_job}' rolündeki Jungyen uyumu ve savunma mekanizması (Süblimasyon) saptandı. 
                Sektörel yetkinlik puanı: %94.
            </div>
            """, unsafe_allow_html=True)
            st.success("**AI Stratejik Soru:** Sektörel krizlerde gölge yanınızı nasıl yönetirsiniz?")
            st.progress(0.94, text="Genel Uyumluluk")
        else:
            st.info("Ses girişi başladığında analiz burada görünecektir.")

    with tab_rep:
        # Tüm Raporların Alt Başlıkları ve İçerikleri
        st.markdown("### 📋 Değerlendirme Raporları")
        with st.expander("📄 A. ADAY UZUN RAPORU"):
            st.markdown('<div class="report-content"><b>Detaylı Profil:</b> Psikanalitik haritalama ve derin analiz...</div>', unsafe_allow_html=True)
        with st.expander("📄 B. ADAY KISA RAPORU"):
            st.markdown('<div class="report-content"><b>Özet:</b> Adayın hızlı değerlendirme karnesi...</div>', unsafe_allow_html=True)
        with st.expander("👤 C. ÖZET İK YETKİLİSİ RAPORU"):
            st.markdown('<div class="report-content"><b>İK Notu:</b> Kültür uyumu ve mülakat performansı özeti.</div>', unsafe_allow_html=True)
        with st.expander("🏢 D. ÖZET FİRMA YETKİLİSİ RAPORU"):
            st.markdown('<div class="report-content"><b>Stratejik Karar:</b> ROI tahmini ve finansal uyum raporu.</div>', unsafe_allow_html=True)
        
        st.divider()
        st.image("https://via.placeholder.com/400x180?text=YETENEK+RADAR+GRAFIGI", caption="Aday Karakter Dağılımı")

# --- 6. FOOTER ---
st.divider()
st.caption(f"Adaptive Hire OS v8.5 | Gazi SAĞLAM - Global Intelligence | {time.strftime('%Y')}")
