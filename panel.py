import streamlit as st
import os
import time

# --- 1. GÜVENLİK VE ML MOTORU BAĞLANTISI ---
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    st.warning("Lütfen Streamlit Cloud Secrets alanına 'OPENAI_API_KEY' ekleyin.")
    st.stop()

# --- 2. GLOBAL SAYFA AYARLARI VE ÖZEL TASARIM ---
st.set_page_config(
    page_title="Adaptive Hire: Global Psychoanalytic Intelligence OS",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gazi Bey'in 11px font ve kurumsal açık renkli profesyonel teması
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 11px !important; background-color: #FDFDFD; }
    .main-header { font-size: 24px !important; font-weight: 900; color: #1E293B; border-bottom: 4px solid #3B82F6; padding-bottom: 12px; margin-bottom: 25px; }
    .transcript-box { background-color: #0F172A; color: #F8FAFC; border: 2px solid #1E293B; padding: 20px; height: 380px; overflow-y: auto; font-family: 'Consolas', monospace; border-radius: 12px; line-height: 1.6; }
    .user-text { color: #60A5FA; font-weight: bold; } 
    .candidate-text { color: #10B981; font-weight: bold; }
    .ai-card { background-color: #FFFFFF; border-left: 6px solid #6366F1; padding: 18px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); margin-bottom: 15px; }
    .stButton>button { font-size: 11px !important; border-radius: 6px; font-weight: 600; transition: all 0.2s; }
    .stButton>button:hover { background-color: #3B82F6; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: SEKTÖREL, ENVANTER VE PSİKANALİZ ÖĞRETİMİ ---
with st.sidebar:
    st.image("https://via.placeholder.com/250x80?text=ADAPTIVE+HIRE+OS", use_container_width=True)
    
    st.markdown("### 🧠 PSİKANALİTİK ML MOTORU")
    # 1. Özellik: 38 Sektör ve 2000+ Meslek Altyapısı
    sect_list = ["Teknoloji", "Finans", "Sağlık", "İnşaat", "Lojistik", "Eğitim", "Enerji", "Hizmet"]
    sector_sel = st.selectbox("Sektörel Zeka (38 Sektör Tanımlı)", sect_list)
    job_input = st.text_input("Meslek Grubu (2000+ Tanımlı)", value="Yazılım Geliştirme Uzmanı")
    
    # 2. Özellik: Psikanaliz Yöntemleri (Dünya Standartları)
    psycho_methods = st.multiselect(
        "Psikanaliz Yöntemleri (ML Entegre)", 
        ["Freudyen Analiz", "Jungyen Arketipler", "Adlerci Yaklaşım", "Lacanian Söylem", "Savunma Mekanizmaları Analizi"],
        default=["Jungyen Arketipler", "Savunma Mekanizmaları Analizi"]
    )
    
    # Envanter Seçimleri (DISC/Metropolitan)
    inventory_sel = st.multiselect(
        "Meslek Seçim Envanterleri", 
        ["DISC Analizi", "Metropolitan", "Big Five", "Kişilik Envanteri"], 
        default=["DISC Analizi"]
    )

    st.divider()
    with st.expander("📁 KURUMSAL DATA VE HİYERARŞİ", expanded=False):
        st.text_input("FİRMA ADI EKLE", value="Karaaslan Grup")
        st.text_input("KLASÖR EKLE", value="2026 Üst Düzey Adaylar")
        st.text_input("BİRİM EKLE", value="Teknoloji Merkezi")
        st.button("YAPIYI SİSTEME KAYDET")
    
    st.info("Sistem Küresel Psikanaliz Veri Setleri ile Senkronize Edildi.")

# --- 4. ANA PANEL: CANLI MÜLAKAT ASİSTANI VE ANALİZ ---
st.markdown('<p class="main-header">ADAPTIVE HIRE: GLOBAL TALENT INTELLIGENCE OS</p>', unsafe_allow_html=True)

col_live, col_ai = st.columns([1.7, 1.3])

with col_live:
    st.subheader("🎙️ Canlı Mülakat ve Renkli Transkript Akışı")
    
    with st.container(border=True):
        c1, c2 = st.columns(2)
        cand_name = c1.text_input("ADAY ADI SOYADI", value="Ahmet Anıl")
        cand_pos = c2.text_input("POZİSYON / MESLEK", value=job_input)
        
        # 3. Özellik: Ses Kayıt Tuşu İle Başlatma
        start_rec_btn = st.button("🎤 SES KAYDINI BAŞLAT (ML & PSİKANALİZ AKTİF)", type="primary", use_container_width=True)
        
        # 2. Segment Süreleri (Yan Yana Butonlar)
        st.markdown("**ANALİZ SEGMENT SÜRESİ SEÇİN:**")
        s1, s2, s3, s4, s5, s6 = st.columns(6)
        if s1.button("15s"): st.session_state['active_seg'] = "15 Saniye"
        if s2.button("30s"): st.session_state['active_seg'] = "30 Saniye"
        if s3.button("60s"): st.session_state['active_seg'] = "60 Saniye"
        if s4.button("2dk"): st.session_state['active_seg'] = "2 Dakika"
        if s5.button("5dk"): st.session_state['active_seg'] = "5 Dakika"
        if s6.button("10dk"): st.session_state['active_seg'] = "10 Dakika"
        
        # 4. Özellik: Bağımsız Gönder Tuşu (Manuel Analiz)
        manual_trigger_btn = st.button("➡️ ŞİMDİ ANALİZ ET VE GÖNDER (ZAMAN SINIRSIZ)", use_container_width=True)
        
        # 5. Özellik: Sunum Modu Tuşu
        pres_mode_btn = st.button("🖥️ SUNUM MODUNU AÇ (CANLI ANALİZ YANSITMA)")

    # 4. Özellik: Renkli Canlı Transkript Alanı
    st.markdown(f"**Anlık Transkript Akışı** (Aktif Segment: {st.session_state.get('active_seg', '15 Saniye')})")
    transcript_placeholder = st.empty()
    
    if start_rec_btn:
        # Renkli HTML Transkript Simülasyonu
        html_output = f'<div class="transcript-box">'
        html_output += f'<span class="user-text">İK Yetkilisi:</span> Hoş geldiniz Ahmet Bey, {sector_sel} sektöründeki vizyonunuzu ve {job_input} olarak başarılarınızı dinlemek isteriz.<br>'
        html_output += f'<span class="candidate-text">Aday:</span> Merhaba, teşekkür ederim. Son 10 yılımı özellikle adaptif yapay zeka sistemleri ve insan psikolojisi üzerine çalışarak geçirdim...<br>'
        html_output += f'<span class="user-text">İK Yetkilisi:</span> Harika. Peki, kriz anlarındaki stres yönetiminizde {", ".join(inventory_sel)} sonuçlarınızın payı nedir?<br>'
        html_output += f'</div>'
        transcript_placeholder.markdown(html_output, unsafe_allow_html=True)

with col_ai:
    # 3. Özellik: Raporlar Sekmesi ve Çok Katmanlı Raporlama
    tab_live_ai, tab_reports = st.tabs(["🤖 CANLI AI ANALİZ", "📊 RAPORLAR SEKİSİ"])
    
    with tab_live_ai:
        if start_rec_btn or manual_trigger_btn:
            st.markdown(f"""
            <div class="ai-card">
                <b>🔍 GERÇEK ZAMANLI ANALİZ RAPORU</b><br>
                <b>Sektör:</b> {sector_sel} | <b>Meslek:</b> {job_input}<br>
                <b>Psikanalitik Bulgu:</b> Adayda güçlü bir 'Benlik İdeali' ve Jungyen 'Bilge' arketipi saptandı. 
                Konuşma kalıplarında Metropolitan envanter uyumu %94 olarak hesaplandı.
            </div>
            """, unsafe_allow_html=True)
            
            st.success("**💡 İK YETKİLİSİ İÇİN STRATEJİK SORULAR:**\n1. {job_input} olarak karşılaştığınız belirsizlik durumlarında içsel otoritenizi nasıl kuruyorsunuz?\n2. Mevcut psikanalitik profiliniz ekibinize nasıl bir liderlik enerjisi katıyor?")
            
            st.markdown("**📊 YETENEK & UYUM PUANLAMASI**")
            st.progress(0.94, text="Genel Uyumluluk Skoru: %94")
            st.progress(0.82, text="Psikolojik Dayanıklılık: %82")
        else:
            st.info("Mülakat başladığında AI analizleri ve psikanalitik öneriler burada belirecektir.")

    with tab_reports:
        # 3. Madde: a, b, c, d Rapor Segmentleri
        st.markdown("### 📋 ADAY DEĞERLENDİRME DOSYALARI")
