import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components
import random
import string

# --- AI AYARLARI ---
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AdaptiveHire - AI Panel & Autonomous OS", layout="wide", initial_sidebar_state="expanded")

# --- KURUMSAL CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #fcfdfe; }
    .ah-card { background: white; padding: 25px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
    
    /* Segment Süreleri - Ayrı Ayrı Kutucuk Tasarımı */
    div[data-testid="stHorizontalBlock"] .stRadio > div { gap: 10px; }
    .stRadio label {
        background: white !important;
        border: 1px solid #cbd5e1 !important;
        padding: 8px 18px !important;
        border-radius: 8px !important;
        font-weight: 500;
        transition: 0.3s;
    }
    .stRadio label:hover { border-color: #2563eb !important; background: #eff6ff !important; }

    /* Sunum Modu Slaytı */
    .presentation-slide {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: white; padding: 80px; border-radius: 20px; text-align: center;
        min-height: 450px; display: flex; flex-direction: column; justify-content: center;
        border: 4px solid #3b82f6; margin-top: 20px;
    }
    
    /* Panelist Kutuları */
    .panelist-box { background: #f1f5f9; padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #2563eb; font-size: 0.9rem; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "setup"
if 'view_mode' not in st.session_state: st.session_state.view_mode = "Chat"
if 'panelists' not in st.session_state: st.session_state.panelists = ["Ana IK Uzmanı (Siz)"]
if 'is_paused' not in st.session_state: st.session_state.is_paused = False
if 'current_q' not in st.session_state: st.session_state.current_q = "Hoş geldiniz. Kendinizden biraz bahseder misiniz?"

# --- SIDEBAR: YÖNETİM ---
with st.sidebar:
    st.markdown("<h2 style='color:#2563eb;'>AdaptiveHire</h2>", unsafe_allow_html=True)
    st.markdown("### 👥 Görüşme Paneli")
    for p in st.session_state.panelists:
        st.markdown(f'<div class="panelist-box">👤 {p}</div>', unsafe_allow_html=True)
    
    p_invite = st.text_input("➕ Uzman Davet Et")
    if st.button("Davet Gönder") and p_invite:
        st.session_state.panelists.append(p_invite)
        st.rerun()
    
    st.divider()
    if st.button("🏠 Ana Menü", use_container_width=True):
        st.session_state.page = "setup"
        st.rerun()

# --- ANA EKRANLAR ---

# 1. SETUP EKRANI (Panel & Otonom Seçimi)
if st.session_state.page == "setup":
    st.subheader("Mülakat Yapılandırma Merkezi")
    c1, c2 = st.columns([1.5, 1])
    
    with c1:
        st.markdown('<div class="ah-card">', unsafe_allow_html=True)
        st.write("**GÖRÜNÜM VE ÇALIŞMA MODU**")
        st.session_state.view_mode = st.radio("Seçin", ["Chat", "Sunum", "Otonom Link"], horizontal=True, label_visibility="collapsed")
        
        st.write("<br>**SEGMENT SÜRESİ** (Çoktan Seçmeli)", unsafe_allow_html=True)
        st.radio("Süre", ["15 sn", "30 sn", "1 dk", "2 dk", "5 dk"], index=1, horizontal=True, label_visibility="collapsed")
        
        st.write("<br>**PSİKOMETRİK KATMANLAR**", unsafe_allow_html=True)
        st.multiselect("Envanterler", ["DISC", "Metropolitan", "Big Five", "Star Uyumu"], default=["DISC"])
        
        st.divider()
        if st.session_state.view_mode == "Otonom Link":
            if st.button("🔗 Aday İçin Link Oluştur", type="primary", use_container_width=True):
                st.code(f"https://adaptivehire.ai/interview/{''.join(random.choices(string.ascii_lowercase, k=10))}")
                st.info("Bu linki adaya ileterek mülakatı başlatmasını isteyebilirsiniz.")
        else:
            if st.button("Mülakatı Başlat →", type="primary", use_container_width=True):
                st.session_state.page = "live"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# 2. CANLI MÜLAKAT (Sunum ve Chat Hibrit)
elif st.session_state.page == "live":
    # Header & Durum
    st.markdown(f"### 🎙️ Canlı Yayın | Mod: {st.session_state.view_mode}")
    
    if st.session_state.view_mode == "Sunum":
        st.markdown(f'<div class="presentation-slide"><div style="font-size:1rem; opacity:0.6;">SORU</div><div style="font-size:2.5rem; font-weight:bold; margin:20px 0;">{st.session_state.current_q}</div><div style="font-size:0.9rem; color:#3b82f6;">ADAPTIVEHIRE AI ANALİZİ AKTİF</div></div>', unsafe_allow_html=True)
        if st.button("✨ AI'dan Yeni Soru İste", use_container_width=True):
            st.session_state.current_q = random.choice(["Gelecek planlarınız neler?", "En büyük başarınız nedir?", "Neden biz?"])
            st.rerun()
        if st.button("⬅️ Chat Moduna Dön"):
            st.session_state.view_mode = "Chat"
            st.rerun()
    else:
        col_m, col_a = st.columns([2.2, 1])
        with col_m:
            st.markdown('<div style="background:white; border:1px solid #e2e8f0; border-radius:12px; padding:20px; height:400px; overflow-y:auto;">', unsafe_allow_html=True)
            if not st.session_state.is_paused:
                components.html("""
                    <div id="o" style="font-family:sans-serif; color:#1e293b;">🎙️ Aday konuşuyor, analiz ediliyor...</div>
                    <script>
                        const R = window.webkitSpeechRecognition || window.Recognition;
                        if(R){ 
                            const r = new R(); r.lang='tr-TR'; r.continuous=true; r.interimResults=true;
                            r.onresult = (e) => {
                                let t = ''; for(let i=0; i<e.results.length; i++) t += e.results[i][0].transcript + ' ';
                                document.getElementById('o').innerHTML = '<b>Aday:</b> ' + t;
                            }; r.start();
                        }
                    </script>
                """, height=350)
            else:
                st.warning("⏸️ Mülakat şu an duraklatıldı.")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_a:
            st.markdown("### 🛠️ Müdahale")
            if st.button("⏸️/▶️ Duraklat/Devam", use_container_width=True):
                st.session_state.is_paused = not st.session_state.is_paused
                st.rerun()
            st.slider("Canlı Puanlama (Teknik)", 0, 100, 70)
            if st.button("🖥️ Sunum Moduna Geç", use_container_width=True):
                st.session_state.view_mode = "Sunum"
                st.rerun()
            st.divider()
            if st.button("🛑 Bitir", type="primary", use_container_width=True):
                st.session_state.page = "report"
                st.rerun()

# 3. RAPOR
elif st.session_state.page == "report":
    st.markdown("# 📑 Final Değerlendirme Raporu")
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.markdown('<div class="ah-card"><h4>IK ve AI Ortak Kararı</h4><p>Genel Uyum: <b>%84</b></p><hr><p>Adayın Metropolitan olgunluk seviyesi kıdemli pozisyonlar için yeterli görülmüştür.</p></div>', unsafe_allow_html=True)
    with col_r:
        fig = go.Figure(go.Scatterpolar(r=[85, 90, 70, 80], theta=['DISC-D','Teknik','EQ','Uyum'], fill='toself'))
        st.plotly_chart(fig, use_container_width=True)
    if st.button("Yeni Görüşme"):
        st.session_state.page = "setup"
        st.rerun()
