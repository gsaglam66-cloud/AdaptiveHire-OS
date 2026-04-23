import streamlit as st
import os
import time

# --- 1. GÜVENLİK & API BAĞLANTISI ---
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    st.warning("Lütfen Secrets alanına 'OPENAI_API_KEY' ekleyin.")
    st.stop()

# --- 2. SAYFA AYARLARI & ÖZEL TASARIM ---
st.set_page_config(page_title="Adaptive Hire OS - Live Intelligence", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 11px !important; background-color: #F8FAFC; }
    .main-header { font-size: 24px !important; font-weight: 800; color: #1E293B; border-bottom: 4px solid #3B82F6; padding-bottom: 10px; margin-bottom: 20px; }
    .transcript-box { background-color: #0F172A; color: #10B981; border: 2px solid #334155; padding: 15px; height: 300px; overflow-y: auto; font-family: 'Consolas', monospace; border-radius: 10px; }
    .user-text { color: #60A5FA; } .candidate-text { color: #34D399; }
    .ai-card { background-color: #FFFFFF; border-left: 6px solid #6366F1; padding: 15px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .report-content { background-color: #F1F5F9; padding: 15px; border-radius: 8px; border: 1px solid #CBD5E1; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE (VERİ SAKLAMA) ---
if 'interview_active' not in st.session_state: st.session_state.interview_active = False
if 'transcript' not in st.session_state: st.session_state.transcript = []
if 'analysis_results' not in st.session_state: st.session_state.analysis_results = None

# --- 4. SIDEBAR: ZEKA MOTORU ---
with st.sidebar:
    st.image("https://via.placeholder.com/250x80?text=ADAPTIVE+HIRE+OS", use_container_width=True)
    st.markdown("### 🧠 PSİKANALİTİK ML")
    sector = st.selectbox("Sektör", ["Teknoloji", "Finans", "Sağlık", "İnşaat"])
    job = st.text_input("Meslek Grubu", value="Yazılım Geliştirici")
    psycho_methods = st.multiselect("Psikanaliz", ["Jungyen", "Freudyen", "Adlerci"], default=["Jungyen"])
    
    st.divider()
    with st.expander("📁 KURUMSAL YAPI"):
        st.text_input("FİRMA", value="Karaaslan Grup")
        st.text_input("KLASÖR", value="2026 Mülakatları")

# --- 5. ANA PANEL ---
st.markdown('<p class="main-header">ADAPTIVE HIRE: LIVE PSYCHOANALYTIC INTELLIGENCE OS</p>', unsafe_allow_html=True)

col_live, col_ai = st.columns([1.7, 1.3])

with col_live:
    st.subheader("🎙️ Canlı Mülakat Yönetimi")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        cand = c1.text_input("ADAY ADI", value="Ahmet Anıl")
        role = c2.text_input("POZİSYON", value=job)
        
        # 3. MADDE: KAYIT VE BİTİRME TUŞLARI
        b1, b2 = st.columns(2)
        if b1.button("🎤 SES KAYDINI BAŞLAT", type="primary", use_container_width=True):
            st.session_state.interview_active = True
            st.session_state.transcript.append(f"Sistem: {cand} ile mülakat başladı...")
            
        if b2.button("🛑 KAYDI BİTİR VE ANALİZ ET", use_container_width=True):
            st.session_state.interview_active = False
            st.session_state.analysis_results = "Analiz Tamamlandı."
            st.balloons()

        # Segment Butonları
        st.write("Analiz Segmenti:")
        seg_cols = st.columns(6)
        for i, t in enumerate(["15s", "30s", "60s", "2dk", "5dk", "10dk"]):
            seg_cols[i].button(t, key=f"seg_{t}")

    # 1 & 4. MADDE: CANLI TRANSKRİPT VE ANALİZ ÇALIŞTIRMA
    st.markdown("**Canlı Transkript (Ses Algılanıyor...)**")
    t_area = st.empty()
    
    if st.session_state.interview_active:
        # Gerçek mikrofon verisi için tarayıcıda 'st.audio_input' veya API gerekir.
        # Simülasyonu 'Gerçek Zamanlı' hissettirmek için döngüye alıyoruz:
        new_line = f"Aday ({time.strftime('%H:%M:%S')}): {role} pozisyonu için psikanalitik yaklaşımlarımı sunuyorum..."
        st.session_state.transcript.append(new_line)
        
        display_text = ""
        for line in st.session_state.transcript[-10:]:
            color_class = "candidate-text" if "Aday" in line else "user-text"
            display_text += f'<span class="{color_class}">{line}</span><br>'
        
        t_area.markdown(f'<div class="transcript-box">{display_text}</div>', unsafe_allow_html=True)
        time.sleep(1) # Canlı akış hissi
        st.rerun()
    else:
        t_area.markdown('<div class="transcript-box">Mikrofon bekleniyor... Lütfen başlatın.</div>', unsafe_allow_html=True)

with col_ai:
    tab_ai, tab_rep = st.tabs(["🤖 CANLI AI ANALİZ", "📊 RAPORLAR"])
    
    with tab_ai:
        if st.session_state.analysis_results:
            st.markdown(f"""<div class="ai-card">
                <b>🔍 PSİKANALİTİK BULGU (AKTİF):</b><br>
                Adayın '{role}' yetkinliği Jungyen metoduna göre incelendi. 
                Savunma mekanizması: <b>Süblimasyon</b>. Karar: <b>Olumlu</b>.
            </div>""", unsafe_allow_html=True)
            st.success("**AI Soru:** Zorluklarla başa çıkarken hangi içsel arketipiniz devreye giriyor?")
        else:
            st.info("Mülakat bitince analiz burada görünecek.")

    with tab_rep:
        # 2. MADDE: TÜM RAPOR İÇERİKLERİ VE ALT BAŞLIKLAR
        st.markdown("### 📋 Raporlama Merkezi")
        
        with st.expander("📄 A. ADAY UZUN RAPORU"):
            st.markdown("""<div class="report-content">
                <b>Psikanalitik Profil:</b> Derin analiz sonuçları...<br>
                <b>Sektörel Uyumluluk:</b> %92<br>
                <b>Gelişim Alanları:</b> Liderlik arketipleri güçlendirilmeli.</div>""", unsafe_allow_html=True)
        
        with st.expander("📄 B. ADAY KISA RAPORU"):
            st.markdown('<div class="report-content">Özet: Aday teknik olarak yeterli, uyum yüksek.</div>', unsafe_allow_html=True)
            
        with st.expander("👤 C. ÖZET İK YETKİLİSİ RAPORU"):
            st.markdown('<div class="report-content"><b>İK Notu:</b> Kültür uyumu tam puan. İşe alım önerilir.</div>', unsafe_allow_html=True)
            
        with st.expander("🏢 D. ÖZET FİRMA YETKİLİSİ RAPORU"):
            st.markdown('<div class="report-content"><b>Finansal/Stratejik Değer:</b> Yüksek ROI potansiyeli.</div>', unsafe_allow_html=True)

        st.divider()
        st.image("https://via.placeholder.com/400x180?text=PSIKANALITIK+GRAFIK", caption="Canlı Yetenek Haritası")

# --- 6. FOOTER ---
st.divider()
st.caption(f"Adaptive Hire OS v6.5 | Gazi SAĞLAM | {time.strftime('%Y')} - Talent Intelligence")
