import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components

# --- AI CONFIGURATION ---
# API anahtarınızı buraya ekleyin
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="AdaptiveHire - AI Interview", layout="wide", initial_sidebar_state="expanded")

# --- KURUMSAL CSS (NLC STANDARTLARI) ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #eef0f2; min-width: 320px !important; }
    
    /* Kart Tasarımları */
    .ah-card { background: white; padding: 25px; border-radius: 12px; border: 1px solid #e6e9ef; box-shadow: 0 2px 10px rgba(0,0,0,0.02); margin-bottom: 20px; }
    
    /* Sol Panel Sarı Görüşme Kartları (Görsel 1 & 3) */
    .side-card { background-color: #fffbe6; border: 1px solid #ffe58f; padding: 12px; border-radius: 8px; margin-bottom: 10px; font-size: 0.85rem; }
    .side-card-white { background-color: white; border: 1px solid #eee; padding: 12px; border-radius: 8px; margin-bottom: 10px; font-size: 0.85rem; }

    /* Rapor Modül Butonları (Görsel 4) */
    .report-btn { background: #ffffff; border: 1px solid #dbeafe; padding: 10px; border-radius: 6px; font-size: 0.75rem; color: #1e40af; text-align: left; }
    
    /* Transkript Ekranı */
    #transcript-area { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; height: 420px; overflow-y: auto; font-size: 1rem; color: #334155; line-height: 1.6; }
    
    /* Buton Renkleri */
    .stButton>button { border-radius: 8px; font-weight: 500; }
    div[data-testid="stFormSubmitButton"] > button { background-color: #2563eb !important; color: white !important; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE YÖNETİMİ ---
if 'page' not in st.session_state: st.session_state.page = "dashboard"

# --- SOL NAVİGASYON (Görsel 1 & 3 esintili) ---
with st.sidebar:
    st.markdown("<h2 style='color:#1e293b; margin-bottom:0;'>AdaptiveHire</h2>", unsafe_allow_html=True)
    st.caption("Profil Yönetimi")
    
    with st.expander("👤 Kullanıcı Profili", expanded=True):
        st.write("**Şamil ALBAYRAK**")
        st.caption("Görüşme Sayısı: 8")
    
    st.text_input("🔍 Görüşme ara...", label_visibility="collapsed")
    
    if st.button("➕ Yeni Görüşme Aç", use_container_width=True, type="primary"):
        st.session_state.page = "setup"
        st.rerun()
    
    st.divider()
    st.markdown("**Danışan Görüşmeleri**")
    st.markdown('<div class="side-card"><b>Görüşme 9</b><br>IK Görüşmeleri Profili<br><small>00:44</small></div>', unsafe_allow_html=True)
    st.markdown('<div class="side-card-white"><b>Görüşme 8</b><br>Teknik Değerlendirme</div>', unsafe_allow_html=True)

# --- ANA İÇERİK ---

# 1. EKRAN: SETUP (Görsel 3 Modeli)
if st.session_state.page == "setup":
    st.subheader("Görüşme 9")
    col_setup, col_preview = st.columns([1.2, 1])
    
    with col_setup:
        st.markdown('<div class="ah-card">', unsafe_allow_html=True)
        st.write("### Oturum Ayarları")
        st.caption("Başlamadan önce tercihlerinizi seçin")
        
        st.write("**GÖRÜNÜM MODU**")
        c1, c2, c3 = st.columns(3)
        c1.button("💬 Chat", use_container_width=True)
        c2.button("♾️ Otonom", use_container_width=True)
        c3.button("🖥️ Sunum", use_container_width=True)
        
        st.write("<br>**SEGMENT SÜRESİ**", unsafe_allow_html=True)
        seg = st.select_slider("", options=["15 saniye", "20 saniye", "30 saniye", "1 dakika", "2 dakika", "5 dakika", "10 dakika"], value="30 saniye")
        
        st.divider()
        if st.button("Başla →", type="primary", use_container_width=True):
            st.session_state.page = "live"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_preview:
        st.write("**ÖNİZLEME**")
        st.markdown('<div class="ah-card" style="height:300px; display:flex; align-items:center; justify-content:center; color:#94a3b8;">Standart sohbet görünümü aktif.</div>', unsafe_allow_html=True)

# 2. EKRAN: CANLI MÜLAKAT (Görsel 4 Modeli)
elif st.session_state.page == "live":
    col_main, col_ctrl = st.columns([2.2, 1])
    
    with col_main:
        st.markdown("### Görüşme 9")
        
        # Transkript Kutusu
        st.markdown('<div id="transcript-area">', unsafe_allow_html=True)
        components.html("""
            <div id="display" style="font-family:sans-serif; color:#334155;">🎙️ Ses kaydı bekleniyor...</div>
            <script>
                const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if(Recognition){
                    const r = new Recognition(); r.lang='tr-TR'; r.continuous=true; r.interimResults=true;
                    r.onresult = (e) => {
                        let t = ''; for(let i=0; i<e.results.length; i++) t += e.results[i][0].transcript + ' ';
                        document.getElementById('display').innerHTML = '<b>Aday:</b> ' + t;
                    };
                    r.start();
                }
            </script>
        """, height=380)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Manuel Mesaj Girişi (Görsel 4 alt bar)
        st.markdown("<br>", unsafe_allow_html=True)
        m_col1, m_col2 = st.columns([6, 1])
        m_col1.text_input("Mesajınızı yazın...", label_visibility="collapsed", placeholder="AI'ya talimat gönderin...")
        m_col2.button("🚀", use_container_width=True)

    with col_ctrl:
        st.markdown("### 🎛️ Kontrol Paneli")
        
        with st.expander("📝 Dinamik Promptlar", expanded=True):
            st.caption("Sürücü Seçin: Mülakat Uzmanı v2")
            
            p_cols = st.columns(2)
            prompts = ["Rapor 5a: Profil", "Rapor 5b: Riskler", "Rapor 5c: Teknik", "Rapor 5d: Soft Skills", "Rapor 5e: Psikososyal", "Rapor 5f: Özet"]
            for i, p in enumerate(prompts):
                p_cols[i%2].button(p
