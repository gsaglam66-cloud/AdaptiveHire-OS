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

# --- KURUMSAL CSS (AdaptiveHire Branding) ---
st.markdown("""
    <style>
    /* Genel Arka Plan ve Yazı Tipleri */
    .stApp { background-color: #fcfdfe; }
    .main-header { color: #1e293b; font-weight: 700; margin-bottom: 1.5rem; }
    
    /* Sidebar Tasarımı (Görsel 1 Referanslı) */
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #f1f5f9; }
    .sidebar-card { background: #f8fafc; padding: 15px; border-radius: 10px; border: 1px solid #e2e8f0; margin-bottom: 10px; }
    
    /* Segment Süreleri - Çoktan Seçmeli Kutucuklar (Görsel 3 & 10 Referanslı) */
    div[data-testid="stHorizontalBlock"] > div:has(div.stButton) {
        flex: 1 1 auto !important;
    }
    .stRadio > div { flex-direction: row !important; gap: 10px; }
    .stRadio label {
        background: white !important;
        border: 1px solid #cbd5e1 !important;
        padding: 10px 20px !important;
        border-radius: 8px !important;
        cursor: pointer;
        transition: 0.2s;
    }
    .stRadio label:hover { border-color: #3b82f6 !important; background: #eff6ff !important; }
    div[data-testid="stWidgetLabel"] { font-weight: 600; color: #475569; margin-bottom: 10px; }

    /* Canlı Transkript Kutusu (Görsel 4 Referanslı) */
    #transcript-box { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 25px; height: 480px; overflow-y: auto; color: #334155; line-height: 1.8; }
    
    /* Rapor Butonları */
    .report-btn button { background: #ffffff !important; border: 1px solid #e2e8f0 !important; color: #1e293b !important; text-align: left !important; justify-content: flex-start !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE YÖNETİMİ ---
if 'page' not in st.session_state: st.session_state.page = "dashboard"
if 'selected_segment' not in st.session_state: st.session_state.selected_segment = "30 saniye"

# --- SIDEBAR (Görsel 1: Profil Yönetimi) ---
with st.sidebar:
    st.markdown("<h2 style='color:#2563eb;'>AdaptiveHire</h2>", unsafe_allow_html=True)
    st.markdown("### 👤 Profil Yönetimi")
    
    with st.expander("📁 Klasörlerim", expanded=True):
        st.markdown('<div class="sidebar-card"><b>IK Görüşmeleri</b><br><small>4 Aktif Görüşme</small></div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-card"><b>Teknik Değerlendirme</b><br><small>2 Aktif Görüşme</small></div>', unsafe_allow_html=True)
    
    st.text_input("🔍 Görüşme ara...", placeholder="Aday ismi yazın")
    
    if st.button("➕ Yeni Görüşme Oluştur", use_container_width=True, type="primary"):
        st.session_state.page = "setup"
        st.rerun()
    
    st.divider()
    st.caption("© 2026 AdaptiveHire AI")

# --- SAYFA AKIŞLARI ---

# 1. EKRAN: DASHBOARD (Hoş Geldiniz)
if st.session_state.page == "dashboard":
    st.markdown("<h1 class='main-header'>Hoş Geldiniz! 👋</h1>", unsafe_allow_html=True)
    st.write("Platformumuza katıldığınız için teşekkür ederiz. Aşağıdan bir işlem seçin.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("📊 **Son Mülakat Özetleri**\n\nŞamil ALBAYRAK - %88 Uyumluluk")
    with col2:
        st.success("🤖 **AI Durumu**\n\nAdaptive-LLM v2 aktif ve hazır.")

# 2. EKRAN: OTURUM AYARLARI (Görsel 3 - Segmentler Kutucuk Halinde)
elif st.session_state.page == "setup":
    st.subheader("Oturum Ayarları")
    col_l, col_r = st.columns([1.5, 1])

    with col_l:
        st.markdown('<div style="background:white; padding:30px; border-radius:15px; border:1px solid #edf2f7;">', unsafe_allow_html=True)
        
        st.write("**GÖRÜNÜM MODU**")
        m1, m2, m3 = st.columns(3)
        m1.button("💬 Chat", use_container_width=True)
        m2.button("♾️ Otonom", use_container_width=True)
        m3.button("🖥️ Sunum", use_container_width=True)
        
        st.write("<br>**SEGMENT SÜRESİ** (Çoktan Seçmeli)", unsafe_allow_html=True)
        # Çizgi yerine kutucuklar (Radio butonu yatay ve CSS ile butonlaştırıldı)
        st.session_state.selected_segment = st.radio(
            "Süre Seçin",
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

    with col_r:
        st.write("**ÖNİZLEME**")
        st.markdown('<div style="background:#f1f5f9; height:300px; border-radius:15px; display:flex; align-items:center; justify-content:center; color:#64748b; border:2px dashed #cbd5e1;">'
                    'Seçilen Mod: Chat<br>Segment: ' + st.session_state.selected_segment + '</div>', unsafe_allow_html=True)

# 3. EKRAN: CANLI MÜLAKAT (Görsel 4: Transkript ve Analiz)
elif st.session_state.page == "live":
    c1, c2 = st.columns([2.5, 1])
    
    with c1:
        st.markdown("### 🎙️ AdaptiveHire Canlı Görüşme")
        # Transkript kutusu
        st.markdown('<div id="transcript-box">', unsafe_allow_html=True)
        components.html("""
            <div id="status" style="color:#2563eb; font-weight:bold; margin-bottom:10px;">🔴 CANLI - Ses Analiz Ediliyor...</div>
            <div id="output" style="font-family:sans-serif; font-size:1.1rem; color:#1e293b;"></div>
            <script>
                const output = document.getElementById('output');
                const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (Recognition) {
                    const rec = new Recognition(); rec.lang = 'tr-TR'; rec.continuous = true; rec.interimResults = true;
                    rec.onresult = (e) => {
                        let text = '';
                        for (let i = 0; i < e.results.length; i++) {
                            text += (e.results[i][0].transcript + ' ');
                        }
                        output.innerHTML = '<b>Aday:</b> ' + text;
                    };
                    rec.start();
                }
            </script>
        """, height=400)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Manuel Giriş
        st.markdown("<br>", unsafe_allow_html=True)
        st.text_input("Adaya soru gönder veya not al...", placeholder="Mesajınızı yazın...")

    with c2:
        st.write("**🎛️ Kontrol Paneli**")
        with st.expander("Dinamik Anal
