import streamlit as st
import os
import time

# --- 1. GÜVENLİK & ML MODELLERİ BAĞLANTISI ---
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    st.warning("Lütfen Secrets alanına 'OPENAI_API_KEY' anahtarını ekleyin.")
    st.stop()

# --- 2. SAYFA AYARLARI & GLOBAL TASARIM ---
st.set_page_config(page_title="Adaptive Hire: Global Talent OS", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 11px !important; background-color: #F8FAFC; }
    .main-header { font-size: 24px !important; font-weight: 800; color: #1E293B; border-bottom: 4px solid #3B82F6; padding-bottom: 12px; margin-bottom: 25px; }
    .transcript-box { background-color: #111827; color: #F3F4F6; border: 1px solid #1E293B; padding: 15px; height: 350px; overflow-y: auto; font-family: 'Consolas', monospace; border-radius: 12px; }
    .user-text { color: #60A5FA; font-weight: bold; } /* İK Yetkilisi Rengi */
    .candidate-text { color: #34D399; font-weight: bold; } /* Aday Rengi */
    .ai-card { background-color: #FFFFFF; border-left: 6px solid #6366F1; padding: 18px; border-radius: 12px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
    .report-btn { margin-bottom: 5px; width: 100%; text-align: left; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: SEKTÖREL ML VE ENVANTER YAPILANDIRMASI ---
with st.sidebar:
    st.image("https://via.placeholder.com/250x80?text=ADAPTIVE+HIRE+OS", use_container_width=True)
    st.markdown("### 🧠 ML & SEKTÖREL ZEKA")
    
    # 1. ve 2. Madde: Sektör ve Envanter Öğretimi
    sector = st.selectbox("Sektör Seçimi (38 Sektör)", ["Teknoloji", "Sağlık", "Enerji", "İnşaat", "Finans", "Lojistik"])
    job_group = st.text_input("Meslek Grubu (2000+ Tanımlı)", value="Yapay Zeka Mimarı")
    
    inventory_mode = st.multiselect("Envanter Algoritması", 
                                    ["DISC Analizi", "Metropolitan", "Big Five", "Kişilik Envanteri"],
                                    default=["DISC Analizi"])

    st.divider()
    with st.expander("📁 KURUMSAL HİYERARŞİ", expanded=False):
        st.text_input("FİRMA", value="Karaaslan Grup")
        st.text_input("KLASÖR", value="2026 Üst Düzey")

    st.info(f"Sistem 2000+ meslek datasıyla optimize edildi.")

# --- 4. ANA PANEL: CANLI MÜLAKAT ASİSTANI ---
st.markdown('<p class="main-header">ADAPTIVE HIRE: GLOBAL TALENT INTELLIGENCE OS</p>', unsafe_allow_html=True)

col_live, col_ai = st.columns([1.8, 1.2])

with col_live:
    st.subheader("🎙️ Canlı Mülakat ve Renkli Transkript")
    
    with st.container(border=True):
        c1, c2 = st.columns(2)
        candidate = c1.text_input("ADAY ADI SOYADI", value="Ahmet Anıl")
        position = c2.text_input("MESLEK / POZİSYON", value=job_group)
        
        # Ses Kayıt ve Segment Kontrolü
        start_rec = st.button("🎤 SES KAYDINI BAŞLAT VE ML SÜRECİNİ TETİKLE", type="primary", use_container_width=True)
        
        st.markdown("**ANALİZ PERİYODU SEÇİN:**")
        seg_cols = st.columns(6)
        times = ["15s", "30s", "60s", "2dk", "5dk", "10dk"]
        for idx, t in enumerate(times):
            seg_cols[idx].button(t, key=f"btn_{t}", use_container_width=True)

        manual_send = st.button("➡️ ŞİMDİ ANALİZ ET VE GÖNDER", use_container_width=True)
        # 5. Madde: Sunum Tuşu
        presentation_mode = st.button("🖥️ SUNUM MODUNU AÇ (TAM EKRAN ANALİZ)", use_container_width=False)

    # 4. Madde: Renkli Transkript Akışı
    st.markdown("**Anlık Transkript (Canlı)**")
    trans_placeholder = st.empty()
    
    if start_rec:
        st.toast(f"{sector} sektörü ve {inventory_mode} modelleri yüklendi.", icon="🧠")
        # Renkli simülasyon metni
        sim_text = f'<div class="transcript-box">'
        sim_text += f'<span class="user-text">İK Yetkilisi:</span> Hoş geldiniz Ahmet Bey, {sector} sektöründeki deneyimlerinizden bahseder misiniz?<br>'
        sim_text += f'<span class="candidate-text">Aday:</span> Merhaba, özellikle {job_group} olarak son 5 yılda adaptif sistemler geliştirdim...<br>'
        sim_text += f'<span class="user-text">İK Yetkilisi:</span> DISC envanterine göre baskın karakteriniz projelerinize nasıl yansıyor?<br>'
        sim_text += f'</div>'
        trans_placeholder.markdown(sim_text, unsafe_allow_html=True)

with col_ai:
    # 3. Madde: Raporlar Sekmesi ve Çoklu Raporlama
    tab1, tab2 = st.tabs(["🤖 CANLI AI ANALİZ", "📊 RAPORLAR"])
    
    with tab1:
        if start_rec or manual_send:
            st.markdown(f'<div class="ai-card"><b>🔍 ML TABANLI ANALİZ</b><br>Sektör: {sector}<br>Meslek: {job_group}<br>Analiz: Adayın teknik terminolojisi ve Metropolitan envanter uyumu %92.</div>', unsafe_allow_html=True)
            st.success("**AI ÖNERİLEN SORULAR:**\n1. Sektörel kriz anlarında DISC profilinizdeki 'D' özelliğini nasıl kullanıyorsunuz?\n2. Makine öğretimi projelerinizdeki ölçekleme stratejiniz nedir?")
            st.progress(0.92, text="Genel Uyumluluk Puanı")
        else:
            st.info("Analiz için mülakatı başlatın.")

    with tab2:
        st.markdown("### 📋 Aday Değerlendirme Raporları")
        st.button("📄 Aday Uzun Rapor (Detaylı Analiz)", use_container_width=True)
        st.button("📄 Aday Kısa Rapor (Özet)", use_container_width=True)
        st.button("👤 İK Yetkilisi Raporu (Yönetici Özeti)", use_container_width=True)
        st.button("🏢 Şirket Yetkilisi Raporu (Stratejik Karar)", use_container_width=True)
        
        st.markdown("---")
        st.markdown("**📊 PUANLAMA & GÖRSELLER**")
        # Grafik simülasyonu
        st.image("https://via.placeholder.com/300x150?text=Yetenek+Radar+Grafigi", caption="Aday Yetkinlik Grafiği")
        st.write("Teknik: 9/10 | Uyum: 8/10 | Liderlik: 7/10")

# 5. Madde: Sunum Tuşu Aktifse
if presentation_mode:
    st.balloons()
    st.warning("SUNUM MODU AKTİF: Yapay zeka analizleri ve önerileri şu an ana ekrana yansıtılıyor.")

# --- 5. FOOTER ---
st.divider()
st.markdown("<div style='text-align: center; color: #94A3B8; font-size: 10px;'>Adaptive Hire OS v4.0 | 'Gazi SAĞLAM - Global Talent Intelligence'</div>", unsafe_allow_html=True)
