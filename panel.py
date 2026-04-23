import streamlit as st
import os
import time

# --- 1. GÜVENLİK VE API YAPILANDIRMASI ---
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    st.error("Kritik Hata: 'OPENAI_API_KEY' bulunamadı. Lütfen Secrets ayarlarını kontrol edin.")
    st.stop()

# --- 2. GLOBAL SAYFA AYARLARI VE KURUMSAL TASARIM ---
st.set_page_config(
    page_title="Adaptive Hire: Enterprise Intelligence OS", 
    page_icon="🧠", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 11px Font ve Profesyonel Arayüz Tasarımı (CSS)
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 11px !important; background-color: #F8FAFC; }
    .main-header { font-size: 24px !important; font-weight: 900; color: #1E293B; border-bottom: 4px solid #3B82F6; padding-bottom: 12px; margin-bottom: 25px; }
    .transcript-box { background-color: #0F172A; color: #F8FAFC; border: 2px solid #334155; padding: 20px; height: 500px; overflow-y: auto; font-family: 'Consolas', monospace; border-radius: 12px; line-height: 1.8; box-shadow: inset 0 2px 15px rgba(0,0,0,0.6); }
    .user-text { color: #60A5FA; font-weight: bold; } 
    .candidate-text { color: #10B981; font-weight: bold; } 
    .third-person { color: #F59E0B; font-weight: bold; } 
    .ai-card { background-color: #FFFFFF; border-left: 6px solid #6366F1; padding: 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 15px; }
    .report-section { background-color: #FFFFFF; padding: 15px; border-radius: 8px; border: 1px solid #E2E8F0; margin-bottom: 12px; line-height: 1.6; }
    .report-title { color: #1E293B; font-weight: 800; border-bottom: 1px solid #CBD5E1; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; }
    .stButton>button { font-size: 11px !important; border-radius: 6px; font-weight: 600; height: 40px; transition: all 0.2s; width: 100%; }
    .stButton>button:hover { border-color: #3B82F6; color: #3B82F6; transform: translateY(-1px); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AKILLI TAHMİN VE SEKTÖREL VERİ SETLERİ ---
sektorler = ["Teknoloji", "Bilişim", "Sağlık", "Finans", "Enerji", "İnşaat", "Lojistik", "Eğitim", "Otomotiv", "Gıda", "Tekstil", "Turizm", "İlaç", "Telekomünikasyon", "Kimya", "Madencilik", "Havacılık", "Savunma Sanayi", "Perakende", "E-Ticaret", "Medya", "Reklamcılık", "Hukuk", "Danışmanlık", "Gayrimenkul", "Tarım", "Hayvancılık", "Denizcilik", "Sigortacılık", "Bankacılık", "Üretim", "Pazarlama", "İnsan Kaynakları", "Psikoloji", "Spor", "Sanat", "Moda", "Kamu Yönetimi"]

meslekler = ["Yazılım Mimarı", "Yapay Zeka Uzmanı", "Veri Bilimci", "İK Uzmanı", "Proje Yöneticisi", "Finans Analisti", "Doktor", "Mühendis", "Siber Güvenlik Uzmanı", "Pazarlama Direktörü", "Satış Temsilcisi", "Hukuk Danışmanı", "Psikolog", "Akademisyen", "Operasyon Müdürü", "Lojistik Uzmanı", "Tasarımcı", "İş Analisti", "Performans Yöneticisi"]

# --- 4. SIDEBAR: ZEKA MOTORU VE ÖZGÜR GİRİŞ ---
with st.sidebar:
    st.image("https://via.placeholder.com/250x80?text=ADAPTIVE+HIRE+OS", use_container_width=True)
    st.markdown("### 🧠 PSİKANALİTİK ML MOTORU")
    
    sel_sector = st.selectbox("Sektör Seçimi (Akıllı Tahmin)", options=sektorler)
    
    # Meslek Seçimi veya Özgür Yazım
    m_secim = st.selectbox("Meslek Grubu", options=["DİĞER (ELLE YAZ)"] + meslekler)
    final_job = st.text_input("Mesleği Tanımlayın", value="Performans Yöneticisi") if m_secim == "DİĞER (ELLE YAZ)" else m_secim
    
    st.divider()
    
    # ML Metotları ve Envanterler
    psy_opt = ["Jungyen", "Freudyen", "Adlerci", "Lacanian", "Savunma Analizi"]
    sel_psy = st.multiselect("Psikanaliz Yöntemleri (ML)", options=psy_opt, default=psy_opt)
    
    inv_opt = ["DISC Analizi", "Metropolitan", "Big Five", "Kişilik Envanteri"]
    sel_inv = st.multiselect("Meslek Envanterleri", options=inv_opt, default=inv_opt)

    st.divider()
    with st.expander("📁 KURUMSAL HİYERARŞİ", expanded=False):
        st.text_input("FİRMA ADI", value="Kurumsal Şirket")
        st.text_input("KLASÖR", value="2026 Aday Portföyü")
        st.text_input("BİRİM", value="İnsan Kaynakları")

# --- 5. ANA PANEL: DİYARİZASYON VE RAPORLAMA ---
st.markdown('<p class="main-header">ADAPTIVE HIRE: ENTERPRISE ANALYTICS OS v12.0</p>', unsafe_allow_html=True)

col_live, col_rep = st.columns([1.6, 1.4])

with col_live:
    st.subheader("🎙️ Canlı Mülakat ve Kişi Ayrıştırmalı Akış")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        # 1. Madde: İsimler Gazi/Ali yerine İK Yöneticisi/Aday olarak güncellendi
        ik_label = c1.text_input("MÜLAKATÇI ROLÜ", value="İK Yöneticisi")
        cand_label = c2.text_input("ADAY TANIMI", value="Aday")
        
        # 2. Madde: Tüm ses özellikleri "Ses Kaydını Başlat" altına toplandı
        audio_stream = st.audio_input("Mülakat Sesini Kaydetmek İçin Mikrofonu Açın")
        
        b1, b2 = st.columns(2)
        start_btn = b1.button("🎤 SES KAYDINI BAŞLAT", type="primary")
        stop_btn = b2.button("🛑 KAYDI BİTİR VE ANALİZ ET")
        
        st.markdown("**ANALİZ SEGMENTLERİ:**")
        s_cols = st.columns(6)
        for i, t in enumerate(["15s", "30s", "60s", "2dk", "5dk", "10dk"]):
            with s_cols[i]: st.button(t, key=f"seg_{t}")
            
        st.button("➡️ ŞİMDİ ANALİZ ET VE GÖNDER")
        st.button("🖥️ SUNUM MODUNU AÇ")

    # 4 & 5. Madde: İsimli ve Canlı Transkript Alanı
    st.markdown("**Anlık Transkript (Kişi Ayrıştırmalı Canlı Akış)**")
    t_area = st.empty()
    
    if start_btn or audio_stream:
        st.toast(f"Diyarizasyon Aktif: {ik_label} ve {cand_label} ayrıştırılıyor.", icon="🔍")
        
        # Canlı Akış Simülasyonu
        flow_html = f'<div class="transcript-box">'
        flow_html += f'<span class="user-text">{ik_label}:</span> '
        if audio_stream:
            flow_html += f"Hoş geldiniz. {sel_sector} sektöründeki hedeflerinizi dinlemek istiyoruz.<br>"
            flow_html += f'<span class="candidate-text">{cand_label}:</span> Merhaba. {final_job} pozisyonu için vizyonum şu yöndedir...<br>'
            flow_html += f'<span class="third-person">Dış Ses:</span> (Ortam sesi bastırıldı, odaklanma başarılı.)<br>'
            flow_html += f'<span class="user-text">{ik_label}:</span> Teknik metodolojilerinizdeki somut başarıları detaylandırır mısınız?<br>'
        flow_html += '</div>'
        t_area.markdown(flow_html, unsafe_allow_html=True)
    else:
        t_area.markdown(f'<div class="transcript-box"><span class="user-text">{ik_label}:</span> ...<br><span class="candidate-text">{cand_label}:</span> ...</div>', unsafe_allow_html=True)

with col_rep:
    tab_ai, tab_master = st.tabs(["🤖 CANLI AI ANALİZ", "📋 PROFESYONEL RAPOR AKIŞI"])
    
    with tab_ai:
        if audio_stream or stop_btn:
            st.markdown(f"""<div class="ai-card">
                <b>🔍 CANLI PSİKANALİTİK ANALİZ</b><br>
                <b>Katılımcılar:</b> {ik_label}, {cand_label}<br>
                <b>Metotlar:</b> {", ".join(sel_psy)}<br>
                <b>Bulgu:</b> Adayın konuşma hızı ve savunma mekanizmaları {", ".join(sel_inv)} ile analiz ediliyor.
            </div>""", unsafe_allow_html=True)
            st.success(f"**AI Soru Önerisi:** {cand_label}, kariyerinizdeki en büyük başarısızlık anında hangi savunma mekanizmasını kullandınız?")
            st.progress(0.88, text="Mevcut Uyumluluk Skoru")
        else:
            st.info("Mülakat başladığında AI verileri burada akacaktır.")

    with tab_master:
        # NLC PDF Formatına Sadık Rapor Akışı
        st.markdown("### KURUMSAL ADAY DEĞERLENDİRME")
        
        with st.expander("📌 1. ÖZET BİLGİ VE DEĞERLENDİRME", expanded=True):
            st.markdown(f'<div class="report-section"><div class="report-title">Genel Profil</div>Adayın sektörel ve fonksiyonel arka planının 7 boyutlu analizi.</div>', unsafe_allow_html=True)
        
        with st.expander("⚖️ 2. KARAR: KOŞULLU UYGUN"):
            st.markdown('<div class="report-section"><div class="report-title">Karar Özeti</div>Belirlenen belirsizliklerin teknik vaka çalışmasıyla netleştirilmesi önerilir.</div>', unsafe_allow_html=True)

        with st.expander("🛤️ 3. KARİYER YOLCULUĞU VE PROFİL"):
            st.markdown('<div class="report-section"><div class="report-title">Kariyer Örüntüsü</div>İstikrar analizi, firma süreleri ve profesyonel gelişim eğrisi.</div>', unsafe_allow_html=True)

        with st.expander("⚙️ 4. TEKNİK YETKİNLİKLER (OKR/KPI/BSC)"):
            st.markdown('<div class="report-section"><div class="report-title">Metodolojik Derinlik</div>Teknik araçlara hakimiyet ve somut uygulama örneklerinin STAR analizi.</div>', unsafe_allow_html=True)

        with st.expander("🤝 5. SOFT SKILLS VE LİDERLİK"):
            st.markdown('<div class="report-section"><div class="report-title">Yönetsel Beceri</div>İletişim, çatışma yönetimi ve ekip kurma yetkinlikleri.</div>', unsafe_allow_html=True)

        with st.expander("🎯 6. MOTİVASYON VE ÖZERKLİK"):
            st.markdown('<div class="report-section"><div class="report-title">İtki Analizi</div>Adayı harekete geçiren içsel ve dışsal faktörlerin dengesi.</div>', unsafe_allow_html=True)

        with st.expander("⚠️ 7. POTANSİYEL RİSKLER"):
            st.markdown('<div class="report-section"><div class="report-title">Risk Matrisi</div>Kavramsal hatalar, somutlaştırmadan kaçınma ve stres altındaki tutum.</div>', unsafe_allow_html=True)

        with st.expander("🏁 8. NİHAİ ÖNERİ VE EK ADIMLAR"):
            st.markdown('<div class="report-section"><div class="report-title">Sonuç</div>Mülakat sonrası atılması gereken stratejik adımlar ve vaka senaryosu.</div>', unsafe_allow_html=True)

        st.divider()
        st.image("https://via.placeholder.com/400x180?text=ADAY+KARAKTER+RADARI", caption="Analiz Sonucu Yetenek Haritası")

# --- 6. FOOTER ---
st.divider()
st.markdown(f"<div style='text-align: center; color: #94A3B8; font-size: 10px;'>Adaptive Hire OS v12.0 MASTER | Kurumsal Zeka Ekosistemi | {time.strftime('%Y')}</div>", unsafe_allow_html=True)
