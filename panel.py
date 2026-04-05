import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components

# --- AI YAPILANDIRMASI ---
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Sayfa Ayarları
st.set_page_config(page_title="AdaptiveHire - AI Recruitment OS", layout="wide", initial_sidebar_state="expanded")

# --- KURUMSAL TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #fcfdfe; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #f1f5f9; }
    
    /* Segment Süreleri - Özel Çoktan Seçmeli Tasarımı (Görsel 3 & 10) */
    .stRadio > div { flex-direction: row !important; gap: 10px; }
    .stRadio label {
        background: white !important;
        border: 1px solid #cbd5e1 !important;
        padding: 8px 16px !important;
        border-radius: 8px !important;
        cursor: pointer;
        transition: 0.2s;
        font-size: 0.9rem;
    }
    .stRadio label:hover { border-color: #2563eb !important; background: #eff6ff !important; }
    
    /* Kart Yapıları */
    .ah-card { background: white; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 20px; }
    #transcript-box { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; height: 450px; overflow-y: auto; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "setup"

# --- SIDEBAR: PROFİL YÖNETİMİ (Görsel 1 & 11) ---
with st.sidebar:
    st.markdown("<h2 style='color:#2563eb;'>AdaptiveHire</h2>", unsafe_allow_html=True)
    st.markdown("### 👤 Profil Yönetimi")
    
    with st.expander("📁 Klasörlerim", expanded=True):
        st.info("📂 IK Görüşmeleri")
        st.write("📂 Teknik Değerlendirme")
    
    if st.button("➕ Yeni Görüşme Oluştur", use_container_width=True, type="primary"):
        st.session_state.page = "setup"
        st.rerun()

# --- ANA AKIŞ ---

# 1. EKRAN: OTURUM AYARLARI (Görsel 3 & Çoktan Seçmeli Segmentler)
if st.session_state.page == "setup":
    st.subheader("Oturum Ayarları")
    col_config, col_preview = st.columns([1.5, 1])

    with col_config:
        st.markdown('<div class="ah-card">', unsafe_allow_html=True)
        
        st.write("**GÖRÜNÜM MODU**")
        m1, m2, m3 = st.columns(3)
        m1.button("💬 Chat", use_container_width=True)
        m2.button("♾️ Otonom", use_container_width=True)
        m3.button("🖥️ Sunum", use_container_width=True)
        
        st.write("<br>**SEGMENT SÜRESİ** (Çoktan Seçmeli)", unsafe_allow_html=True)
        # Çizgi slider yerine ayrı buton-kutucuk yapısı
        selected_seg = st.radio(
            "Süre Seçimi",
            options=["15 sn", "20 sn", "30 sn", "1 dk", "2 dk", "5 dk", "10 dk"],
            index=2,
            horizontal=True,
            label_visibility="collapsed"
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

    with col_preview:
        st.write("**ÖNİZLEME**")
        # Hatalı f-string satırı düzeltildi (Satır 95 civarı)
        preview_text = f"Seçilen Segment: {selected_seg}"
        st.markdown(f'<div class="ah-card" style="height:320px; text-align:center; color:#64748b; border:2px dashed #cbd5e1;"><br><br><b>{preview_text}</b><br>Adaptive mülakat modu aktif.</div>', unsafe_allow_html=True)

# 2. EKRAN: CANLI MÜLAKAT (Transkript ve Analiz)
elif st.session_state.page == "live":
    col_main, col_ctrl = st.columns([2.5, 1])
    
    with col_main:
        st.markdown("### 🎙️ Canlı Görüşme Akışı (AdaptiveHire)")
        st.markdown('<div id="transcript-box">', unsafe_allow_html=True)
        components.html("""
            <div id="log" style="font-family:sans-serif; color:#334155; font-size:1.1rem;">🎙️ Ses tanıma aktif, aday konuşması bekleniyor...</div>
            <script>
                const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if(Recognition){
                    const r = new Recognition(); r.lang='tr-TR'; r.continuous=true; r.interimResults=true;
                    r.onresult = (e) => {
                        let t = ''; for(let i=0; i<e.results.length; i++) t += e.results[i][0].transcript + ' ';
                        document.getElementById('log').innerHTML = '<b style="color:#2563eb;">Aday:</b> ' + t;
                    };
                    r.start();
                }
            </script>
        """, height=400)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_ctrl:
        st.markdown("### 🎛️ Kontrol Paneli")
        with st.expander("📊 Dinamik Analiz Raporları", expanded=True):
            for p in ["Rapor 5a: Profil", "Rapor 5b: Riskler", "Rapor 5c: Teknik", "Rapor 5d: Sosyal"]:
                st.button(p, use_container_width=True)
        
        st.divider()
        if st.button("🛑 Mülakatı Bitir", type="primary", use_container_width=True):
            st.session_state.page = "report"
            st.rerun()

# 3. EKRAN: YÖNETİCİ ÖZETİ (1 Sayfa Rapor)
elif st.session_state.page == "report":
    st.markdown("# 📑 Yönetici Özet Raporu")
    l, r = st.columns([2, 1])
    with l:
        st.markdown('<div class="ah-card"><h4>Genel Değerlendirme</h4><p>Adayın uyumluluk puanı: <b>%87</b></p><hr><p>Teknik yetkinlik yüksek, iletişim becerileri gelişmiş.</p></div>',
