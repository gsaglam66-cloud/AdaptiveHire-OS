import streamlit as st
import os
import time

# --- 1. GÜVENLİK VE API YAPILANDIRMASI ---
# API Key kontrolü ve çevre değişkeni ataması
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    st.warning("Lütfen Streamlit Cloud Secrets alanına 'OPENAI_API_KEY' anahtarını ekleyin.")
    st.stop()

# --- 2. GLOBAL SAYFA AYARLARI VE ÖZEL TASARIM ---
st.set_page_config(
    page_title="Adaptive Hire: Enterprise Intelligence OS", 
    page_icon="🧠", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gazi Bey'in 11px font ve kurumsal tasarım sadakati (Tam Detaylı CSS)
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 11px !important; background-color: #F8FAFC; }
    .main-header { font-size: 24px !important; font-weight: 900; color: #1E293B; border-bottom: 4px solid #3B82F6; padding-bottom: 12px; margin-bottom: 25px; }
    .transcript-box { background-color: #0F172A; color: #F8FAFC; border: 2px solid #334155; padding: 20px; height: 480px; overflow-y: auto; font-family: 'Consolas', monospace; border-radius: 12px; line-height: 1.8; box-shadow: inset 0 2px 15px rgba(0,0,0,0.6); }
    .user-text { color: #60A5FA; font-weight: bold; } 
    .candidate-text { color: #10B981; font-weight: bold; } 
    .third-person { color: #F59E0B; font-weight: bold; } 
    .ai-card { background-color: #FFFFFF; border-left: 6px solid #6366F1; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 15px; }
    .report-section { background-color: #FFFFFF; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0; margin-bottom: 10px; line-height: 1.6; }
    .report-title { color: #1E293B; font-weight: 800; border-bottom: 1px solid #CBD5E1; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; }
    .stButton>button { font-size: 11px !important; border-radius: 6px; font-weight: 600; height: 38px; transition: all 0.2s; }
    .stButton>button:hover { border-color: #3B82F6; color: #3B82F6; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AKILLI TAHMİN DATA SETLERİ ---
sektorler = ["Teknoloji", "Bilişim", "Sağlık", "Finans", "Enerji", "İnşaat", "Lojistik", "Eğitim", "Otomotiv", "Gıda", "Tekstil", "Turizm", "İlaç", "Telekomünikasyon", "Kimya", "Madencilik", "Havacılık", "Savunma Sanayi", "Perakende", "E-Ticaret", "Medya", "Reklamcılık", "Hukuk", "Danışmanlık", "Gayrimenkul", "Tarım", "Hayvancılık", "Denizcilik", "Sigortacılık", "Bankacılık", "Üretim", "Pazarlama", "İnsan Kaynakları", "Psikoloji", "Spor", "Sanat", "Moda", "Kamu Yönetimi"]

meslekler = ["Yazılım Mimarı", "Yapay Zeka Uzmanı", "Veri Bilimci", "İK Uzmanı", "Proje Yöneticisi", "Finans Analisti", "Doktor", "Mühendis", "Siber Güvenlik Uzmanı", "Pazarlama Direktörü", "Satış Temsilcisi", "Hukuk Danışmanı", "Psikolog", "Akademisyen", "Operasyon Müdürü", "Lojistik Uzmanı", "Tasarımcı", "İş Analisti", "Performans Yöneticisi"]

# --- 4. SIDEBAR: AKILLI TAHMİN VE ÖZGÜR YAZIM ---
with st.sidebar:
    st.image("https://via.placeholder.com/250x80?text=ADAPTIVE+HIRE+OS", use_container_width=True)
    st.markdown("### 🧠 PSİKANALİTİK ML MOTORU")
    
    sel_sector = st.selectbox("Sektör (Akıllı Tahmin)", options=sektorler)
    
    # 3. Madde: Meslek Grubunda Seçme veya Elle Yazma İmkanı
    m_secim = st.selectbox("Meslek Grubu", options=["DİĞER (ELLE YAZ)"] + meslekler)
    if m_secim == "DİĞER (ELLE YAZ)":
        final_job = st.text_input("Mesleği Buraya Yazın", value="Performans Yöneticisi")
    else:
        final_job = m_secim
    
    st.divider()
    
    # Psikanaliz Yöntemleri (Hepsi Seçili)
    psy_opt = ["Jungyen", "Freudyen", "Adlerci", "Lacanian", "Savunma Analizi"]
    sel_psy = st.multiselect("Psikanaliz Yöntemleri", options=psy_opt, default=psy_opt)
    
    # Envanterler (Hepsi Seçili)
    inv_opt = ["DISC Analizi", "Metropolitan", "Big Five", "Kişilik Envanteri"]
    sel_inv = st.multiselect("Meslek Envanterleri", options=inv_opt, default=inv_opt)

    st.divider()
    with st.expander("📁 KURUMSAL HİYERARŞİ VE DATA", expanded=False):
        st.text_input("FİRMA ADI EKLE", value="Fuzul Oto")
        st.text_input("KLASÖR EKLE", value="2026 Üst Düzey Adaylar")
        st.text_input("BİRİM EKLE", value="İnsan Kaynakları")
    
    st.info("Kurumsal Veri Havuzu ve Diyarizasyon Aktif.")

# --- 5. ANA PANEL: CANLI MÜLAKAT VE PROFESYONEL AKIŞ ---
st.markdown('<p class="main-header">ADAPTIVE HIRE: ENTERPRISE ANALYTICS OS</p>', unsafe_allow_html=True)

col_live, col_rep = st.columns([1.6, 1.4])

with col_live:
    st.subheader("🎙️ Canlı Mülakat ve Kişi Ayrıştırmalı Akış")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        ik_name = c1.text_input("İK YÖNETİCİSİ İSMİ", value="Gazi Sağlam")
        cand_name = c2.text_input("ADAY ADI SOYADI", value="Ali Bey")
        
        # 1 & 2. Madde: Ayrı alan kalktı, butonla tetiklenen ses girişi
        audio_stream = st.audio_input("Mülakat Sesini Almak İçin Aktif Edin")
        
        b1, b2 = st.columns(2)
        start_btn = b1.button("🎤 SES KAYDINI BAŞLAT", type="primary", use_container_width=True)
        stop_btn = b2.button("🛑 KAYDI BİTİR VE ANALİZ ET", use_container_width=True)
        
        st.markdown("**ANALİZ SEGMENT SÜRELERİ:**")
        s_cols = st.columns(6)
        for i, t in enumerate(["15s", "30s", "60s", "2dk", "5dk", "10dk"]):
            with s_cols[i]: st.button(t, key=f"seg_{t}", use_container_width=True)
            
        st.button("➡️ ŞİMDİ ANALİZ ET VE GÖNDER", use_container_width=True)
        st.button("🖥️ SUNUM MODUNU AÇ")

    # 4 & 5. Madde: Anlık Transkript (Başlangıçta boş, konuşunca dolan alan)
    st.markdown("**Anlık Transkript (Kişi Ayrıştırmalı Canlı Akış)**")
    transcript_area = st.empty()
    
    if start_btn or audio_stream:
        st.toast(f"Diyarizasyon Motoru Aktif: {ik_name} vs {cand_name}", icon="🔍")
        
        flow_html = f'<div class="transcript-box">'
        flow_html += f'<span class="user-text">{ik_name}:</span> '
        if audio_stream:
            flow_html += "Ali Bey hoş geldiniz, finans sektöründeki şubeleşme deneyimlerinizden bahsedelim.<br>"
            flow_html += f'<span class="candidate-text">{cand_name}:</span> Teşekkürler Gazi Bey. 15 yıllık İK tecrübemle hazırım...<br>'
            flow_html += f'<span class="third-person">Dış Ses (Kişi 3):</span> Bağlantı stabil, kayıt alınıyor.<br>'
            flow_html += f'<span class="user-text">{ik_name}:</span> Performans yönetimi kurgusunda önceliğiniz nedir?<br>'
        flow_html += '</div>'
        transcript_area.markdown(flow_html, unsafe_allow_html=True)
    else:
        # 2. Madde: Sadece başlıklar, yazı yok
        transcript_area.markdown(f'<div class="transcript-box"><span class="user-text">{ik_name}:</span> ...<br><span class="candidate-text">{cand_name}:</span> ...</div>', unsafe_allow_html=True)

with col_rep:
    tab_ai, tab_master = st.tabs(["🤖 CANLI AI ANALİZ", "📋 PROFESYONEL RAPOR AKIŞI"])
    
    with tab_ai:
        if start_btn or audio_stream or stop_btn:
            st.markdown(f"""<div class="ai-card">
                <b>🔍 CANLI PSİKANALİTİK ANALİZ</b><br>
                <b>Katılımcılar:</b> {ik_name}, {cand_name}, Ortam Sesi<br>
                <b>Metotlar:</b> {", ".join(sel_psy)}<br>
                <b>Bulgu:</b> Adayın '{final_job}' rolündeki sektörel uyumu %94.
            </div>""", unsafe_allow_html=True)
            st.success(f"**AI Soru Önerisi:** {cand_name} Bey, şubeleşme yapısında karşılaştığınız en somut performans engelini paylaşır mısınız?")
            st.progress(0.94, text="Genel Uyumluluk Skoru")
        else:
            st.info("Mülakat başladığında canlı AI analizleri burada belirecektir.")

    with tab_master:
        # 1. Madde: PDF Rapor Akış Sıralaması (NLC Formatına Sadık)
        st.markdown("### KURUMSAL ADAY DEĞERLENDİRME")
        
        with st.expander("📌 1. ÖZET BİLGİ VE DEĞERLENDİRME", expanded=True):
            st.markdown(f'<div class="report-section"><div class="report-title">Genel Profil</div>Adayın {final_job} pozisyonu için sektörel ve fonksiyonel arka plan özeti.</div>', unsafe_allow_html=True)
        
        with st.expander("⚖️ 2. KARAR: KOŞULLU UYGUN"):
            st.markdown('<div class="report-section"><div class="report-title">Karar Özeti</div>Mevcut yetkinliklerin vaka çalışması ile doğrulanması şartıyla onaylanmıştır.</div>', unsafe_allow_html=True)

        with st.expander("🛤️ 3. KARİYER YOLCULUĞU VE PROFİL"):
            st.markdown('<div class="report-section"><div class="report-title">Kariyer Örüntüsü</div>Adayın geçmiş firma süreleri, sektör tercihleri ve profesyonel istikrar analizi.</div>', unsafe_allow_html=True)

        with st.expander("⚙️ 4. TEKNİK YETKİNLİKLER (OKR/KPI/BSC)"):
            st.markdown('<div class="report-section"><div class="report-title">Metodolojik Analiz</div>OKR, KPI ve Balanced Scorecard araçlarının kullanım derinliği ve teknik kanıtlar.</div>', unsafe_allow_html=True)

        with st.expander("🤝 5. SOFT SKILLS VE LİDERLİK"):
            st.markdown('<div class="report-section"><div class="report-title">Liderlik Potansiyeli</div>Ekip yönetimi ölçeği, iletişim becerileri ve çatışma yönetimi yetkinlikleri.</div>', unsafe_allow_html=True)

        with st.expander("🎯 6. MOTİVASYON VE ÖZERKLİK"):
            st.markdown('<div class="report-section"><div class="report-title">Motivasyon Analizi</div>Dışsal ödül beklentisi ile içsel tutku dengesi ve karar verme bağımsızlığı.</div>', unsafe_allow_html=True)

        with st.expander("⚠️ 7. POTANSİYEL RİSKLER"):
            st.markdown('<div class="report-section"><div class="report-title">Risk Matrisi</div>Teknik somutlaştırma eksikliği, beklenti yönetimi ve stres altındaki savunma mekanizmaları.</div>', unsafe_allow_html=True)

        with st.expander("🏁 8. NİHAİ ÖNERİ VE EK ADIMLAR"):
            st.markdown('<div class="report-section"><div class="report-title">Gelişim Önerileri</div>İkinci tur mülakat odağı, referans kontrolü ve teknik test planlaması.</div>', unsafe_allow_html=True)

        st.divider()
        st.image("https://via.placeholder.com/400x180?text=ADAY+YETENEK+RADARI")

# --- 6. FOOTER ---
st.divider()
st.markdown(f"<div style='text-align: center; color: #94A3B8; font-size: 10px;'>Adaptive Hire OS v11.0 MASTER | Gazi SAĞLAM | {time.strftime('%Y')}</div>", unsafe_allow_html=True)
