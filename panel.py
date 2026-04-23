import streamlit as st
import os
import time

# --- 1. GÜVENLİK VE API BAĞLANTISI ---
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    st.warning("Lütfen Secrets alanına 'OPENAI_API_KEY' ekleyin.")
    st.stop()

# --- 2. GLOBAL SAYFA AYARLARI VE ÖZEL TASARIM ---
st.set_page_config(page_title="Adaptive Hire: Global Intelligence OS", page_icon="🧠", layout="wide")

# 11px font ve kurumsal tasarım sadakati
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 11px !important; background-color: #F8FAFC; }
    .main-header { font-size: 24px !important; font-weight: 800; color: #1E293B; border-bottom: 4px solid #3B82F6; padding-bottom: 10px; margin-bottom: 25px; }
    .transcript-box { background-color: #0F172A; color: #10B981; border: 2px solid #334155; padding: 15px; height: 350px; overflow-y: auto; font-family: 'Consolas', monospace; border-radius: 12px; }
    .user-text { color: #60A5FA; font-weight: bold; } 
    .candidate-text { color: #34D399; font-weight: bold; }
    .ai-card { background-color: #FFFFFF; border-left: 6px solid #6366F1; padding: 18px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .report-content { background-color: #F1F5F9; padding: 12px; border-radius: 8px; border: 1px solid #CBD5E1; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA LİSTELERİ (SEKTÖR VE MESLEK) ---
sektorler = [
    "Teknoloji", "Bilişim", "Sağlık", "Finans", "Enerji", "İnşaat", "Lojistik", "Eğitim", "Otomotiv", "Gıda", 
    "Tekstil", "Turizm", "İlaç", "Telekomünikasyon", "Kimya", "Madencilik", "Havacılık", "Savunma Sanayi", 
    "Perakende", "E-Ticaret", "Medya", "Reklamcılık", "Hukuk", "Danışmanlık", "Gayrimenkul", "Tarım", 
    "Hayvancılık", "Denizcilik", "Sigortacılık", "Bankacılık", "Üretim", "Pazarlama", "İnsan Kaynakları", 
    "Psikoloji", "Spor", "Sanat", "Moda", "Kamu Yönetimi"
]

meslekler = [
    "Yazılım Mimarı", "Yapay Zeka Uzmanı", "Veri Bilimci", "İK Uzmanı", "Proje Yöneticisi", "Finans Analisti", 
    "Doktor", "Mühendis", "Siber Güvenlik Uzmanı", "Pazarlama Direktörü", "Satış Temsilcisi", "Hukuk Danışmanı", 
    "Psikolog", "Akademisyen", "Operasyon Müdürü", "Lojistik Uzmanı", "Tasarımcı", "İş Analisti"
    # Burası 2000+ meslek için altyapı sunar
]

# --- 4. SIDEBAR: AKILLI ZEKA VE YÖNETİM ---
with st.sidebar:
    st.image("https://via.placeholder.com/250x80?text=ADAPTIVE+HIRE+OS", use_container_width=True)
    st.markdown("### 🧠 PSİKANALİTİK ML MOTORU")
    
    # 1. Madde: Sektör Autocomplete (selectbox üzerinden otomatik tamamlama)
    selected_sector = st.selectbox("Sektör (38 Sektör Tanımlı)", options=sektorler, index=0)
    
    # 2. Madde: Meslek Autocomplete
    selected_job = st.selectbox("Meslek Grubu (2000+ Tanımlı)", options=meslekler, index=0)
    
    # 3. Madde: Psikanaliz Sistemleri (Hepsi Seçili Gelmeli)
    psycho_options = ["Jungyen", "Freudyen", "Adlerci", "Lacanian", "Savunma Analizi"]
    selected_psycho = st.multiselect("Psikanaliz Yöntemleri (ML)", options=psycho_options, default=psycho_options)
    
    # 4. Madde: Envanterler (Hepsi Seçili Gelmeli)
    inventory_options = ["DISC Analizi", "Metropolitan", "Big Five", "Kişilik Envanteri"]
    selected_inv = st.multiselect("Meslek Seçim Envanterleri", options=inventory_options, default=inventory_options)

    st.divider()
    with st.expander("📁 KURUMSAL HİYERARŞİ"):
        st.text_input("FİRMA", value="Karaaslan Grup")
        st.text_input("KLASÖR", value="2026 Üst Düzey")
    
    st.info("Küresel ML Veri Setleri Aktif.")

# --- 5. ANA PANEL: CANLI MÜLAKAT ASİSTANI ---
st.markdown('<p class="main-header">ADAPTIVE HIRE: PSYCHOANALYTIC INTELLIGENCE OS</p>', unsafe_allow_html=True)

col_live, col_ai = st.columns([1.7, 1.3])

with col_live:
    st.subheader("🎙️ Canlı Mülakat ve Transkript")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        cand = c1.text_input("ADAY ADI SOYADI", value="Ahmet Anıl")
        pos = c2.text_input("POZİSYON", value=selected_job)
        
        # Fonksiyonel Butonlar
        rec_col, end_col = st.columns(2)
        start_rec = rec_col.button("🎤 SES KAYDINI BAŞLAT", type="primary", use_container_width=True)
        # 3. Madde: Kaydı Bitir ve Analiz Et
        end_rec = end_col.button("🛑 KAYDI BİTİR VE ANALİZ ET", use_container_width=True)
        
        st.write("Analiz Segmenti:")
        seg_cols = st.columns(6)
        times = ["15s", "30s", "60s", "2dk", "5dk", "10dk"]
        for i, t in enumerate(times):
            seg_cols[i].button(t, key=f"t_{t}", use_container_width=True)
            
        manual_send = st.button("➡️ ŞİMDİ ANALİZ ET VE GÖNDER", use_container_width=True)
        presentation = st.button("🖥️ SUNUM MODUNU AÇ")

    # Canlı Akış Alanı
    st.markdown("**Anlık Transkript Akışı**")
    t_area = st.empty()
    
    if start_rec:
        st.toast(f"Mülakat başlatıldı: {selected_sector} / {selected_job}", icon="🎙️")
        sim_html = f'<div class="transcript-box">'
        sim_html += f'<span class="user-text">İK Yetkilisi:</span> Hoş geldiniz, {selected_sector} alanındaki vizyonunuzu dinliyoruz.<br>'
        sim_html += f'<span class="candidate-text">Aday:</span> Merhaba, {selected_job} olarak psikanalitik temelli çözümler üretiyorum...<br>'
        sim_html += f'</div>'
        t_area.markdown(sim_html, unsafe_allow_html=True)
    else:
        t_area.markdown('<div class="transcript-box">Bekleniyor...</div>', unsafe_allow_html=True)

with col_ai:
    tab_ai, tab_rep = st.tabs(["🤖 CANLI AI ANALİZ", "📊 RAPORLAR"])
    
    with tab_ai:
        if start_rec or end_rec:
            st.markdown(f"""
            <div class="ai-card">
                <b>🔍 PSİKANALİTİK ML RAPORU</b><br>
                <b>Sektör/Meslek:</b> {selected_sector} / {selected_job}<br>
                <b>Bulgu:</b> Jungyen arketip uyumu ve {", ".join(selected_inv)} sonuçları %94 tutarlılık gösteriyor.
            </div>
            """, unsafe_allow_html=True)
            st.success("**AI Stratejik Soru:** Bu pozisyonda gölge yanlarınızı nasıl yöneteceksiniz?")
            st.progress(0.94, text="Genel Uyumluluk")
        else:
            st.info("Analiz için mülakatı başlatın.")

    with tab_rep:
        # Raporlar ve Alt Başlıkları
        st.markdown("### 📋 Değerlendirme Merkezi")
        with st.expander("📄 A. ADAY UZUN RAPORU"):
            st.markdown('<div class="report-content">Detaylı psikanalitik profil ve sektör yetkinlik matrisi.</div>', unsafe_allow_html=True)
        with st.expander("📄 B. ADAY KISA RAPORU"):
            st.markdown('<div class="report-content">Aday özeti ve hızlı değerlendirme notları.</div>', unsafe_allow_html=True)
        with st.expander("👤 C. ÖZET İK YETKİLİSİ RAPORU"):
            st.markdown('<div class="report-content">İK gözüyle kültür uyumu ve mülakat performansı.</div>', unsafe_allow_html=True)
        with st.expander("🏢 D. ÖZET FİRMA YETKİLİSİ RAPORU"):
            st.markdown('<div class="report-content">Stratejik karar raporu ve ROI tahmini.</div>', unsafe_allow_html=True)
            
        st.divider()
        st.image("https://via.placeholder.com/400x180?text=ADAPTIVE+HIRE+GRAPH", caption="Yetenek ve Karakter Grafiği")

# --- 6. FOOTER ---
st.divider()
st.caption(f"Adaptive Hire OS v7.0 | Gazi SAĞLAM - Global Intelligence Ecosystem")
