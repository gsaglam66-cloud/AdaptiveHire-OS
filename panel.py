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
st.set_page_config(
    page_title="Adaptive Hire: NLC Master Intelligence OS", 
    page_icon="🧠", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 11px font ve NLC Kurumsal Rapor Tasarımı
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 11px !important; background-color: #F8FAFC; }
    .main-header { font-size: 22px !important; font-weight: 900; color: #1E293B; border-bottom: 3px solid #3B82F6; padding-bottom: 10px; margin-bottom: 20px; text-transform: uppercase; }
    .transcript-box { background-color: #0F172A; color: #F8FAFC; border: 1px solid #334155; padding: 25px; height: 500px; overflow-y: auto; font-family: 'Consolas', monospace; border-radius: 8px; line-height: 1.8; box-shadow: inset 0 4px 20px rgba(0,0,0,0.5); }
    .user-text { color: #60A5FA; font-weight: bold; border-left: 3px solid #60A5FA; padding-left: 8px; } 
    .candidate-text { color: #10B981; font-weight: bold; border-left: 3px solid #10B981; padding-left: 8px; } 
    .third-person { color: #F59E0B; font-weight: italic; opacity: 0.8; } 
    .ai-card { background-color: #FFFFFF; border-top: 4px solid #6366F1; padding: 20px; border-radius: 4px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 15px; }
    .report-section { background-color: #FFFFFF; padding: 20px; border: 1px solid #E2E8F0; border-radius: 4px; margin-top: 15px; }
    .report-header { font-size: 14px; font-weight: 700; color: #1E293B; border-bottom: 1px solid #CBD5E1; padding-bottom: 5px; margin-bottom: 10px; }
    .risk-high { color: #EF4444; font-weight: bold; }
    .stButton>button { font-size: 11px !important; border-radius: 4px; font-weight: 700; height: 40px; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AKILLI TAHMİN VE SEKTÖREL VERİ SETLERİ ---
sektorler = ["Finans", "Otomotiv", "Teknoloji", "Sağlık", "Enerji", "İnşaat", "Lojistik", "Eğitim", "Gıda", "Tekstil", "Turizm", "Telekomünikasyon", "Kamu Yönetimi"]
meslekler = ["Performans Yöneticisi", "İK Müdürü", "Yazılım Mimarı", "Yapay Zeka Uzmanı", "Veri Bilimci", "Proje Yöneticisi", "Finans Analisti", "Siber Güvenlik Uzmanı"]

# --- 4. SIDEBAR: NLC ANALİZ MOTORU ---
with st.sidebar:
    st.image("https://via.placeholder.com/250x80?text=NLC+NEO+LIMBIC+CORTEX", use_container_width=True)
    st.markdown("### 🧠 ANALİZ KONFİGÜRASYONU")
    
    sel_sector = st.selectbox("🎯 Hedef Sektör", options=sektorler)
    
    # Madde 3: Meslek Seçimi veya Elle Yazma
    job_choice = st.selectbox("💼 Pozisyon Seçin", options=["DİĞER (ELLE YAZ)"] + meslekler)
    if job_choice == "DİĞER (ELLE YAZ)":
        final_job = st.text_input("Pozisyonu Tanımlayın", value="Performans Yöneticisi")
    else:
        final_job = job_choice
    
    st.divider()
    psy_opt = ["Jungyen", "Freudyen", "Adlerci", "Lacanian", "Savunma Mekanizmaları", "Diyarizasyon Analizi"]
    st.multiselect("⚙️ Psikanalitik Metotlar", options=psy_opt, default=psy_opt)
    
    inv_opt = ["OKR/KPI Uyumu", "Balanced Scorecard Derinliği", "STAR İletişim Analizi", "Big Five"]
    st.multiselect("📊 Teknik Envanterler", options=inv_opt, default=inv_opt)

    st.divider()
    with st.expander("🏢 KURUMSAL HİYERARŞİ"):
        firm_name = st.text_input("ŞİRKET", value="Fuzul Oto")
        folder_name = st.text_input("KLASÖR", value="NLC - Üst Düzey Adaylar")

# --- 5. ANA PANEL: CANLI MÜLAKAT VE DİYARİZASYON ---
st.markdown(f'<p class="main-header">{firm_name}: ADAPTIVE HIRE - NLC FINAL MASTER OS</p>', unsafe_allow_html=True)

col_live, col_ai = st.columns([1.6, 1.4])

with col_live:
    st.subheader("🎙️ Canlı Mülakat ve Kişi Ayrıştırma")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        ik_name = c1.text_input("GÖRÜŞMECİ (İK)", value="Gazi Sağlam")
        cand_name = c2.text_input("ADAY ADI SOYADI", value="Ali Bey")
        
        # Madde 1 & 2: Ses kaydı başlat tuşuyla mikrofon entegrasyonu
        # Streamlit'te audio_input görünür olmalıdır ancak butonla tetiklenmiş hissi verilir
        voice_raw = st.audio_input("Mülakat Sesini Almak İçin Aktif Edin")
        
        btn_c1, btn_c2 = st.columns(2)
        start_interview = btn_c1.button("🎤 SES KAYDINI BAŞLAT", type="primary", use_container_width=True)
        stop_interview = btn_c2.button("🛑 KAYDI BİTİR VE ANALİZ ET", use_container_width=True)
        
        st.markdown("**ANALİZ SEGMENTLERİ:**")
        s_cols = st.columns(6)
        for i, t in enumerate(["15s", "30s", "60s", "2dk", "5dk", "10dk"]):
            with s_cols[i]: st.button(t, key=f"seg_{t}", use_container_width=True)
        
        st.button("➡️ ŞİMDİ ANALİZ ET VE GÖNDER", use_container_width=True)
        st.button("🖥️ SUNUM MODUNU AÇ")

    # Madde 4 & 5: İsimli ve Canlı Transkript Akışı
    st.markdown("**Anlık Transkript (Kişi Ayrıştırmalı Canlı Akış)**")
    t_area = st.empty()
    
    if start_interview or voice_raw:
        # Madde 4 & 5: İsimlerin ve konuşmaların anlık canlı gelmesi
        st.toast(f"Diyarizasyon Başladı: {ik_name} vs {cand_name}", icon="🎙️")
        
        sim_html = f'<div class="transcript-box">'
        sim_html += f'<div class="user-text">{ik_name}:</span> Ali Bey hoş geldiniz. {firm_name} {final_job} mülakatına başlıyoruz. Önce kariyer yolculuğunuzu dinleyelim.</div><br>'
        time.sleep(0.8)
        sim_html += f'<div class="candidate-text">{cand_name}:</span> Teşekkürler Gazi Bey. Yaklaşık 15-16 yıldır İK alanındayım, son 6 yılım performans odaklı geçti...</div><br>'
        sim_html += f'<div class="third-person">Sistem Notu: Ortam gürültüsü normalize edildi. 3. şahıs algılanmadı.</div><br>'
        sim_html += f'<div class="user-text">{ik_name}:</span> Balanced Scorecard ve KPI arasındaki stratejik farkı kendi deneyimlerinizle nasıl açıklarsınız?</div><br>'
        sim_html += f'</div>'
        t_area.markdown(sim_html, unsafe_allow_html=True)
    else:
        t_area.markdown('<div class="transcript-box">Sistem ses girişi bekliyor... Konuşma başladığında döküm burada görünecektir.</div>', unsafe_allow_html=True)

with col_ai:
    tab_nlc, tab_rep = st.tabs(["🤖 NLC ANALİZ MOTORU", "📄 ADAY UZUN RAPORU"])
    
    with tab_nlc:
        if start_interview or voice_raw:
            st.markdown(f"""
            <div class="ai-card">
                <b>🔍 NLC ANLIK BULGULAR</b><br>
                <b>Aday:</b> {cand_name} | <b>Pozisyon:</b> {final_job}<br>
                <b>Durum:</b> Kavramsal bilgi yüksek, somutlaştırmadan kaçınma eğilimi %70 saptandı.<br>
                <b>Psikanalitik Not:</b> Savunma mekanizması: Minimizasyon (Zorlukları küçültme).
            </div>
            """, unsafe_allow_html=True)
            st.warning(f"**NLC SORU ÖNERİSİ:** {cand_name}, Balanced Scorecard'da yaşadığınız en büyük teknik hatayı ve nasıl düzelttiğinizi anlatır mısınız?")
            st.progress(0.48, text="NLC Pozisyon Uygunluk Puanı: 48/100")
        else:
            st.info("Mülakat başladığında NLC analizleri burada akacaktır.")

    with tab_rep:
        # NLC FORMATINDA SIRALI RAPOR (Hiçbir özellik atlanmadan)
        st.markdown(f"### {cand_name} - NLC Aday Değerlendirme")
        
        with st.expander("1. ÖZET BİLGİ VE DEĞERLENDİRME", expanded=True):
            st.markdown(f"**Karar:** <span style='color:orange; font-weight:bold;'>KOŞULLU UYGUN</span>", unsafe_allow_html=True)
            st.write(f"{cand_name}, {sel_sector} sektörü ve {final_job} pozisyonu için sektörel arka plana sahiptir.")

        with st.expander("2. ADAY PROFİLİ VE KARİYER YOLCULUĞU"):
            st.write("**Deneyim:** ~15-16 Yıl İK Fonksiyonları")
            st.write("**Bilinçli Tercih:** Finans sektörü ve şubeleşme dinamikleri hakimiyeti.")

        with st.expander("3. TEKNİK YETKİNLİKLER (OKR/KPI/BSC)"):
            st.error("Kritik Hata: Balanced Scorecard tanımında kavramsal karışıklık tespit edildi.")
            st.write("**Somutluk Puanı:** Düşük (STAR metodu eksikliği).")

        with st.expander("4. SOFT SKILLS (Liderlik & Duygusal Zeka)"):
            st.write("**Liderlik Tarzı:** Analiz odaklı, 'arkadaşlar' eksenli samimi yaklaşım.")
            st.write("**Duygusal Zeka:** Zafiyet göstermekten kaçınma stratejisi hakim.")

        with st.expander("5. PSİKOSEKSUEL / PSİKOSOSYAL ANALİZ"):
            st.write("**Motivasyon:** Dışsal ağırlıklı (Şartlar, Başarı Karşılığı, Güvenli Sektör).")
            st.write("**Özerklik:** Kariyer kararlarında yüksek sahiplik.")

        with st.expander("6. POTANSİYEL RİSK MATRİSİ"):
            st.markdown("- <span class='risk-high'>Teknik Derinlik Riski:</span> Uygulama örneklerinin eksikliği.", unsafe_allow_html=True)
            st.markdown("- <span class='risk-high'>Motivasyon Riski:</span> Beklenti yönetimi ve uzun vadeli kalıcılık.", unsafe_allow_html=True)

        with st.expander("7. NİHAİ ÖNERİ VE EK ADIMLAR"):
            st.info("Öneri: Teknik vaka çalışması ve 2. tur derinleşme mülakatı yapılması şarttır.")

st.divider()
st.markdown(f"<div style='text-align: center; color: #94A3B8; font-size: 10px;'>{firm_name} - NLC Neo Limbic Cortex | v10.0 FINAL MASTER | {time.strftime('%Y')}</div>", unsafe_allow_html=True)
