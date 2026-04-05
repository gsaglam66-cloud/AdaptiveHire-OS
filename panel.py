import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components

# --- AI AYARI ---
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Sayfa Yapılandırması
st.set_page_config(page_title="AdaptiveHire - AI Interview OS", layout="wide", initial_sidebar_state="expanded")

# --- KURUMSAL CSS (AdaptiveHire Teması) ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #eef0f2; min-width: 320px !important; }
    
    /* Kart Tasarımları */
    .ah-card { background: white; padding: 25px; border-radius: 12px; border: 1px solid #e6e9ef; box-shadow: 0 2px 10px rgba(0,0,0,0.02); margin-bottom: 20px; }
    
    /* Sol Panel Görüşme Listesi (Görsel 1 & 3) */
    .side-item-active { background-color: #fffbe6; border: 1px solid #ffe58f; padding: 12px; border-radius: 8px; margin-bottom: 10px; font-size: 0.85rem; }
    .side-item { background-color: white; border: 1px solid #eee; padding: 12px; border-radius: 8px; margin-bottom: 10px; font-size: 0.85rem; }

    /* Transkript Alanı */
    #transcript-box { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; height: 450px; overflow-y: auto; font-size: 1rem; color: #334155; line-height: 1.6; }
    
    /* Segment Butonları */
    .stButton>button { border-radius: 8px; font-weight: 500; transition: 0.2s; }
    .main-btn button { background-color: #2563eb !important; color: white !important; width: 100%; border: none; height: 45px; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE YÖNETİMİ ---
if 'page' not in st.session_state: st.session_state.page = "dashboard"

# --- SIDEBAR: PROFİL VE GÖRÜŞME YÖNETİMİ (Görsel 1 & 3) ---
with st.sidebar:
    st.markdown("<h2 style='color:#1e293b;'>AdaptiveHire</h2>", unsafe_allow_html=True)
    
    st.markdown("### 📁 Profil Yönetimi")
    with st.expander("Klasörler", expanded=True):
        st.write("📂 IK Görüşmeleri Profili")
        st.write("📂 Teknik Değerlendirme")
    
    st.text_input("🔍 Görüşme ara...", placeholder="Aday veya başlık...")
    
    if st.button("➕ Yeni Görüşme Aç", use_container_width=True, type="primary"):
        st.session_state.page = "setup"
        st.rerun()
    
    st.divider()
    st.markdown("**Son Görüşmeler**")
    st.markdown('<div class="side-item-active"><b>Görüşme 9</b><br><small>Şamil ALBAYRAK - Aktif</small></div>', unsafe_allow_html=True)
    st.markdown('<div class="side-item"><b>Görüşme 8</b><br><small>Teknik Uzman Analizi</small></div>', unsafe_allow_html=True)

# --- ANA PANEL AKIŞI ---

# 1. EKRAN: KURULUM VE AYARLAR (Görsel 3)
if st.session_state.page == "setup":
    st.subheader("Görüşme Yapılandırması")
    col_config, col_view = st.columns([1.5, 1])
    
    with col_config:
        st.markdown('<div class="ah-card">', unsafe_allow_html=True)
        st.write("### Oturum Ayarları")
        
        st.write("**GÖRÜNÜM MODU**")
        m1, m2, m3 = st.columns(3)
        m1.button("💬 Chat", use_container_width=True)
        m2.button("♾️ Otonom", use_container_width=True)
        m3.button("🖥️ Sunum", use_container_width=True)
        
        st.write("<br>**GİRİŞ KAYNAĞI**", unsafe_allow_html=True)
        g1, g2 = st.columns(2)
        g1.button("🎤 Sadece Mikrofon", use_container_width=True)
        g2.button("🖥️ Sistem Sesi", use_container_width=True)
        
        st.write("<br>**⏱️ SEGMENT SÜRESİ**", unsafe_allow_html=True)
        # Çizgi hatasını önlemek için net yazılı slider
        seg_time = st.select_slider("", options=["15 sn", "20 sn", "30 sn", "1 dk", "2 dk", "5 dk", "10 dk"], value="30 sn")
        
        st.divider()
        st.markdown('<div class="main-btn">', unsafe_allow_html=True)
        if st.button("Mülakatı Başlat →"):
            st.session_state.page = "live"
            st.rerun()
        st.markdown('</div></div>', unsafe_allow_html=True)

    with col_view:
        st.write("**ÖNİZLEME**")
        st.markdown('<div class="ah-card" style="height:350px; display:flex; flex-direction:column; align-items:center; justify-content:center;">'
                    '<img src="https://cdn-icons-png.flaticon.com/512/2593/2593491.png" width="60"><br>'
                    '<p style="color:#64748b;">Standart Sohbet Görünümü</p></div>', unsafe_allow_html=True)

# 2. EKRAN: CANLI MÜLAKAT VE KONTROL PANELİ (Görsel 4)
elif st.session_state.page == "live":
    col_chat, col_ctrl = st.columns([2.2, 1])
    
    with col_chat:
        st.markdown("### 🎙️ Canlı Mülakat Akışı")
        
        # Transkript Alanı (JS destekli anlık akış)
        st.markdown('<div id="transcript-box">', unsafe_allow_html=True)
        components.html("""
            <div id="log" style="font-family:sans-serif; color:#334155;">🎙️ Sistem hazır, ses bekleniyor...</div>
            <script>
                const log = document.getElementById('log');
                const Speech = window.SpeechRecognition || window.webkitSpeechRecognition;
                if(Speech){
                    const r = new Recognition(); r.lang='tr-TR'; r.continuous=true; r.interimResults=true;
                    r.onresult = (e) => {
                        let t = ''; for(let i=0; i<e.results.length; i++) t += e.results[i][0].transcript + ' ';
                        log.innerHTML = '<b style="color:#2563eb;">Aday:</b> ' + t;
                    };
                    r.start();
                }
            </script>
        """, height=400)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Manuel Müdahale ve Mesaj Girişi
        st.markdown("<br>", unsafe_allow_html=True)
        msg_col, btn_col = st.columns([6, 1])
        with msg_col:
            st.text_input("AI'ya talimat verin...", label_visibility="collapsed", placeholder="Soru sormasını isteyin veya not ekleyin...")
        with btn_col:
            st.button("🚀", use_container_width=True)

    with col_ctrl:
        st.markdown("### 🎛️ Kontrol Paneli")
        
        # Dinamik Rapor Promptları (Görsel 4'teki 2'li yapı)
        with st.expander("📝 Dinamik Promptlar", expanded=True):
            st.caption("Sürücü: Mülakat Uzmanı v2")
            p_cols = st.columns(2)
            prompts = ["Rapor 5a: Profil", "Rapor 5b: Riskler", "Rapor 5c: Teknik", "Rapor 5d: Sosyal", "Rapor 5e: Psikoloji", "Rapor 5f: Özet"]
            for i, p in enumerate(prompts):
                p_cols[i%2].button(p, use_container_width=True, key=f"p_{i}")
        
        st.divider()
        st.write("**🤖 Model Seçimi**")
        st.selectbox("Adaptive-LLM Engine", ["Gemini 1.5 Pro (Adaptif)", "GPT-4 Turbo"], label_visibility="collapsed")
        
        if st.button("🛑 Görüşmeyi Bitir ve Raporla", use_container_width=True, type="secondary"):
            st.session_state.page = "report"
            st.rerun()

# 3. EKRAN: RAPORLAMA (Yönetici Özeti)
elif st.session_state.page == "report":
    st.title("📑 Değerlendirme Raporu")
    
    col_rep, col_stat = st.columns([2, 1])
    with col_rep:
        st.markdown('<div class="ah-card"><h3>1 Sayfalık Yönetici Özeti</h3>'
                    '<p>Adayın <b>teknik yetkinliği</b> %85 oranında pozisyonla uyumludur. '
                    '<b>Kritik Risk:</b> Ekip yönetiminde daha önce sınırlı tecrübe belirtilmiştir.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="ah-card"><h4>Yetkinlik Analizi</h4>'
                    '<ul><li>Problem Çözme: 9/10</li><li>İletişim: 7/10</li><li>Teknik Bilgi: 8/10</li></ul></div>', unsafe_allow_html=True)
    
    with col_stat:
        st.markdown('<div class="ah-card">', unsafe_allow_html=True)
        fig = go.Figure(go.Scatterpolar(r=[9, 7, 8, 8.5], theta=['Analitik','Sosyal','Teknik','Uyum'], fill='toself'))
        st.plotly_chart(fig, use_container_width=True)
        st.button("📥 PDF Olarak İndir", use_container_width=True)
        if st.button("🏠 Ana Sayfaya Dön", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
