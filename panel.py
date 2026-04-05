import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
from streamlit_components_lowlevel import components # Gizli bileşenler için

# --- AI AYARI ---
API_KEY = "SENİN_API_KEYİN" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Adaptive Hire OS", layout="wide", initial_sidebar_state="expanded")

# --- GELİŞMİŞ TASARIM VE SIRI ANIMASYONU ---
st.markdown("""
    <style>
    .stSidebar { background-color: #f0f2f6; }
    .setup-card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    
    /* Siri Halkası */
    .siri-container { display: flex; justify-content: center; height: 100px; margin: 10px 0; }
    .siri-sphere {
        width: 70px; height: 70px; border-radius: 50%;
        background: linear-gradient(45deg, #00d2ff, #3a7bd5, #ff00c1, #9d50bb);
        background-size: 400% 400%;
        animation: siri-pulse 2s infinite ease-in-out alternate;
    }
    @keyframes siri-pulse { from { transform: scale(1); box-shadow: 0 0 20px #3a7bd5; } to { transform: scale(1.2); box-shadow: 0 0 40px #ff00c1; } }
    
    /* Transkript Kutusu */
    #transcript-display {
        background-color: #1e1e1e; color: #00ff00; padding: 15px;
        border-radius: 10px; font-family: 'Courier New', monospace;
        height: 200px; overflow-y: auto; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SOL PANEL (HİYERARŞİK ARŞİV) ---
with st.sidebar:
    st.markdown("### 📂 Kayıt Arşivi")
    with st.expander("🏢 Kurum Seçin...", expanded=True):
        uzman = st.text_input("Sorumlu Uzman:", placeholder="Örn: Şamil Albayrak")
        aday = st.text_input("Aday İsmi:", placeholder="Örn: Mehmet Can")
    st.divider()
    st.info("💡 İpucu: Segment süresi sonunda AI otomatik soru üretecektir.")

# --- ANA AKIŞ ---
if 'mulakat_aktif' not in st.session_state:
    st.session_state.mulakat_aktif = False

if not st.session_state.mulakat_aktif:
    # 1. EKRAN: KURULUM
    st.title("🚀 Oturum Yapılandırması")
    col_l, col_r = st.columns([1.5, 1])
    
    with col_l:
        st.markdown('<div class="setup-card">', unsafe_allow_html=True)
        st.write("**⏱️ ADAPTİF ANALİZ SEGMENTİ**")
        segment_sure = st.select_slider("Saniye cinsinden seçin:", options=[15, 30, 60, 300, 600])
        
        st.divider()
        if st.button("CANLI MÜLAKATI BAŞLAT →", use_container_width=True):
            st.session_state.mulakat_aktif = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # 2. EKRAN: CANLI MÜLAKAT ODASI
    st.header(f"🎙️ Canlı Görüşme: {aday if aday else 'Yeni Aday'}")
    
    c1, c2, c3 = st.columns([1, 2, 1])
    
    with c1:
        st.write("**Oturum Verileri**")
        st.metric("Segment", f"{segment_sure} sn")
        if st.button("🛑 Oturumu Bitir"):
            st.session_state.mulakat_aktif = False
            st.rerun()

    with c2:
        # SIRI HALKASI
        st.markdown("<div class='siri-container'><div class='siri-sphere'></div></div>", unsafe_allow_html=True)
        
        # --- JAVASCRIPT TABANLI ANLIK TRANSKRIPT ---
        st.write("**🗨️ Anlık Transkript (Live)**")
        
        # Bu kısım tarayıcının mikrofonunu kullanır ve anında ekrana yazar
        st.components.v1.html("""
            <div id="transcript-display">Ses bekleniyor... Dinlemeye başlamak için tarayıcı izni verin.</div>
            <script>
                const display = document.getElementById('transcript-display');
                const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (Recognition) {
                    const rec = new Recognition();
                    rec.lang = 'tr-TR';
                    rec.continuous = True;
                    rec.interimResults = True;
                    
                    rec.onresult = (event) => {
                        let text = '';
                        for (let i = event.resultIndex; i < event.results.length; i++) {
                            text += event.results[i][0].transcript;
                        }
                        display.innerText = text;
                    };
                    rec.start();
                } else {
                    display.innerText = "Tarayıcı desteklenmiyor.";
                }
            </script>
        """, height=250)

    with c3:
        st.write("**🤖 AI Analiz Paneli**")
        # Burada AI'nın periyodik önerileri belirecek
        st.warning("⚠️ Adaptif Öneri: Adayın son cümlesindeki liderlik vurgusunu derinleştirin.")
        
        # Radar Grafik
        fig = go.Figure(go.Scatterpolar(r=[70, 80, 60, 90], theta=['Hız','Güven','Teknik','Akıcılık'], fill='toself'))
        fig.update_layout(height=200, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
