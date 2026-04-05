import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components

# --- AI AYARI ---
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Sayfa Konfigürasyonu
st.set_page_config(page_title="AdaptiveHire - AI Recruitment OS", layout="wide", initial_sidebar_state="expanded")

# --- KURUMSAL CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #fcfdfe; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #f1f5f9; }
    
    /* Segment Süreleri - Çoktan Seçmeli Tasarımı */
    .stRadio > div { flex-direction: row !important; gap: 10px; }
    .stRadio label {
        background: white !important;
        border: 1px solid #cbd5e1 !important;
        padding: 8px 20px !important;
        border-radius: 8px !important;
        cursor: pointer;
        transition: 0.2s;
    }
    .stRadio label:hover { border-color: #2563eb !important; background: #eff6ff !important; }
    
    .ah-card { background: white; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 20px; }
    #transcript-box { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; height: 400px; overflow-y: auto; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "setup"

# --- SIDEBAR (Görsel 1: Profil Yönetimi) ---
with st.sidebar:
    st.markdown("<h2 style='color:#2563eb;'>AdaptiveHire</h2>", unsafe_allow_html=True)
    st.markdown("### 👤 Profil Yönetimi")
    with st.expander("📁 Klasörlerim", expanded=True):
        st.info("📂 IK Görüşmeleri Profili")
        st.write("📂 Teknik Değerlendirme")
    
    if st.button("➕ Yeni Görüşme Oluştur", use_container_width=True, type="primary"):
        st.session_state.page = "setup"
        st.rerun()

# --- SAYFA AKIŞLARI ---

# 1. EKRAN: KURULUM (Görsel 3: Segmentler Çoktan Seçmeli)
if st.session_state.page == "setup":
    st.subheader("Oturum Ayarları")
    col_l, col_r = st.columns([1.5, 1])

    with col_l:
        st.markdown('<div class="ah-card">', unsafe_allow_html=True)
        st.write("**GÖRÜNÜM MODU**")
        m1, m2, m3 = st.columns(3)
        m1.button("💬 Chat", use_container_width=True)
        m2.button("♾️ Otonom", use_container_width=True)
        m3.button("🖥️ Sunum", use_container_width=True)
        
        st.write("<br>**SEGMENT SÜRESİ** (Çoktan Seçmeli)", unsafe_allow_html=True)
        selected_seg = st.radio(
            "Süre Seçin",
            options=["15 sn", "20 sn", "30 sn", "1 dk", "2 dk", "5 dk", "10 dk"],
            index=2, horizontal=True, label_visibility="collapsed"
        )
        
        st.write("<br>**GİRİŞ KAYNAĞI**", unsafe_allow_html=True)
        g1, g2 = st.columns(2)
        g1.button("🎤 Sadece Mikrofon", use_container_width=True)
        g2.button("🖥️ Sistem Sesi", use_container_width=True)
        
        st.divider()
        if st.button("Mülakatı Başlat →", type="primary", use_container_width=True):
            st.session_state.page = "live"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.write("**ÖNİZLEME**")
        st.markdown(f'<div class="ah-card" style="height:320px; text-align:center; color:#64748b; border:2px dashed #cbd5e1;"><br><br><b>{selected_seg}</b> segment süresi aktif.<br>Aday analizi hazır.</div>', unsafe_allow_html=True)

# 2. EKRAN: CANLI MÜLAKAT (Görsel 4: Transkript)
elif st.session_state.page == "live":
    c1, c2 = st.columns([2.5, 1])
    with c1:
        st.markdown("### 🎙️ AdaptiveHire Canlı Görüşme")
        st.markdown('<div id="transcript-box">', unsafe_allow_html=True)
        components.html("""
            <div id="status" style="color:#2563eb; font-weight:bold; margin-bottom:10px;">🔴 CANLI - Ses Analiz Ediliyor...</div>
            <div id="output" style="font-family:sans-serif; font-size:1.1rem; color:#1e293b;">🎙️ Adayın konuşması bekleniyor...</div>
            <script>
                const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (Recognition) {
                    const rec = new Recognition(); rec.lang = 'tr-TR'; rec.continuous = true; rec.interimResults = true;
                    rec.onresult = (e) => {
                        let text = '';
                        for (let i = 0; i < e.results.length; i++) text += (e.results[i][0].transcript + ' ');
                        document.getElementById('output').innerHTML = '<b>Aday:</b> ' + text;
                    };
                    rec.start();
                }
            </script>
        """, height=350)
        st.markdown('</div>', unsafe_allow_html=True)
        st.text_input("Adaya soru gönder veya not al...", placeholder="Mesajınızı yazın...")

    with c2:
        st.write("**🎛️ Kontrol Paneli**")
        with st.expander("📊 Dinamik Analiz Raporları", expanded=True):
            for r in ["Rapor 5a: Profil", "Rapor 5b: Teknik", "Rapor 5c: Sosyal", "Rapor 5d: Risk"]:
                st.button(r, use_container_width=True)
        
        st.divider()
        if st.button("🛑 Mülakatı Bitir", type="primary", use_container_width=True):
            st.session_state.page = "final_report"
            st.rerun()

# 3. EKRAN: YÖNETİCİ ÖZETİ (Hatalı 137. satır burada düzeltildi)
elif st.session_state.page == "final_report":
    st.markdown("# 📑 Mülakat Sonuç Raporu")
    res_l, res_r = st.columns([2, 1])
    with res_l:
        # Görsel 17'deki hata burada kapatılan parantez ile giderildi
        st.markdown('<div class="ah-card"><h4>Genel Değerlendirme</h4><p>Adayın uyumluluk puanı: <b>%87</b></p><hr><p>Teknik yetkinlik beklentileri karşılıyor. AdaptiveHire AI analizi, adayın problem çözme yeteneğinin yüksek olduğunu saptamıştır.</p></div>', unsafe_allow_html=True)
        
    with res_r:
        fig = go.Figure(go.Scatterpolar(r=[90, 80, 70, 85, 95], theta=['Teknik','İletişim','Zeka','Uyum','Liderlik'], fill='toself'))
        st.plotly_chart(fig, use_container_width=True)
    
    if st.button("🏠 Ana Sayfaya Dön", use_container_width=True):
        st.session_state.page = "setup"
        st.rerun()
