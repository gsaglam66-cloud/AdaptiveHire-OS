import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components

# --- AI AYARI ---
API_KEY = "BURAYA_API_ANAHTARINI_YAZ" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="AdaptiveHire - AI Interview", layout="wide")

# --- TASARIM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e0e0e0; }
    .ah-card { background: white; padding: 25px; border-radius: 12px; border: 1px solid #eaedf2; margin-bottom: 20px; }
    #transcript-box { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; height: 400px; overflow-y: auto; color: #1e293b; }
    .main-blue-btn button { background-color: #2563eb !important; color: white !important; width: 100%; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'step' not in st.session_state: st.session_state.step = "setup"

# --- SIDEBAR ---
with st.sidebar:
    st.title("AdaptiveHire")
    st.text_input("🔍 Görüşme Ara...")
    if st.button("➕ Yeni Görüşme Aç", use_container_width=True):
        st.session_state.step = "setup"
        st.rerun()
    st.divider()
    st.info("Görüşme #9 - Şamil ALBAYRAK")

# --- ANA EKRAN ---
if st.session_state.step == "setup":
    st.subheader("Oturum Ayarları")
    col_l, col_r = st.columns([1.5, 1])
    
    with col_l:
        st.markdown('<div class="ah-card">', unsafe_allow_html=True)
        st.write("**GÖRÜNÜM MODU**")
        st.columns(3)[0].button("💬 Chat", use_container_width=True)
        
        st.write("<br>**SEGMENT SÜRESİ**", unsafe_allow_html=True)
        seg = st.select_slider("", options=["15 sn", "30 sn", "1 dk", "2 dk", "5 dk"], value="30 sn")
        
        st.divider()
        if st.button("Mülakatı Başlat →", type="primary", use_container_width=True):
            st.session_state.step = "live"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        # İŞTE HATANIN OLDUĞU YER BURASIYDI, ŞİMDİ DOLU VE GİRİNTİLİ:
        st.markdown('<div class="ah-card">', unsafe_allow_html=True)
        st.write("**ÖNİZLEME**")
        st.image("https://cdn-icons-png.flaticon.com/512/2593/2593491.png", width=80)
        st.caption("Seçilen mod aktif edilecek.")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.step == "live":
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown('<div id="transcript-box">', unsafe_allow_html=True)
        components.html("""
            <div id="out" style="font-family:sans-serif; color:#334155;">🎙️ Ses bekleniyor...</div>
            <script>
                const out = document.getElementById('out');
                const Rec = window.SpeechRecognition || window.webkitSpeechRecognition;
                if(Rec){
                    const r = new Rec(); r.lang='tr-TR'; r.continuous=true; r.interimResults=true;
                    r.onresult = (e) => {
                        let t = ''; for(let i=0; i<e.results.length; i++) t += e.results[i][0].transcript + ' ';
                        out.innerHTML = '<b>Aday:</b> ' + t;
                    };
                    r.start();
                }
            </script>
        """, height=350)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.write("**⚙️ Kontrol Paneli**")
        st.button("📄 Rapor 5a - Aday Profili")
        st.button("📊 Rapor 5b - Teknik")
        if st.button("🛑 Bitir", use_container_width=True):
            st.session_state.step = "setup"
            st.rerun()
