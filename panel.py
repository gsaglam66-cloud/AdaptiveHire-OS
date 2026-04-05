import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components

# --- AI AYARI ---
API_KEY = "BURAYA_API_ANAHTARINI_YAZ" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Adaptive Hire OS", layout="wide", initial_sidebar_state="expanded")

# --- TASARIM VE SIRI ANIMASYONU ---
st.markdown("""
    <style>
    .stSidebar { background-color: #f0f2f6; }
    .setup-card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .siri-container { display: flex; justify-content: center; height: 100px; margin: 10px 0; }
    .siri-sphere {
        width: 70px; height: 70px; border-radius: 50%;
        background: linear-gradient(45deg, #00d2ff, #3a7bd5, #ff00c1, #9d50bb);
        background-size: 400% 400%;
        animation: siri-pulse 2s infinite ease-in-out alternate;
    }
    @keyframes siri-pulse { from { transform: scale(1); box-shadow: 0 0 20px #3a7bd5; } to { transform: scale(1.2); box-shadow: 0 0 40px #ff00c1; } }
    #transcript-display {
        background-color: #1e1e1e; color: #00ff00; padding: 15px;
        border-radius: 10px; font-family: 'Courier New', monospace;
        height: 250px; overflow-y: auto; margin-top: 10px;
    }
    .folder-label { color: #6b7280; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SOL PANEL ---
with st.sidebar:
    st.markdown("### 📂 Kayıt Arşivi")
    with st.expander("🏢 Kurum Seçin...", expanded=True):
        st.markdown("<p class='folder-label'>Sorumlu Uzman:</p>", unsafe_allow_html=True)
        uzman = st.text_input("uzman_id", placeholder="Örn: Şamil Albayrak", label_visibility="collapsed")
        st.markdown("<p class='folder-label'>Aday İsmi:</p>", unsafe_allow_html=True)
        aday = st.text_input("aday_id", placeholder="Örn: Mehmet Can", label_visibility="collapsed")
    st.divider()
    st.button("➕ Yeni Klasör Oluştur", use_container_width=True)

# --- ANA AKIŞ ---
if 'mulakat_aktif' not in st.session_state:
    st.session_state.mulakat_aktif = False

if not st.session_state.mulakat_aktif:
    st.title("🚀 Oturum Yapılandırması")
    col_l, col_r = st.columns([1.5, 1])
    with col_l:
        st.markdown('<div class="setup-card">', unsafe_allow_html=True)
        st.write("**⏱️ ADAPTİF ANALİZ SEGMENTİ**")
        segment_sure = st.select_slider("Periyot seçin:", options=["15 sn", "30 sn", "1 dk", "2 dk", "5 dk", "10 dk"])
        st.divider()
        if st.button("CANLI MÜLAKATI BAŞLAT →", use_container_width=True):
            st.session_state.mulakat_aktif = True
            st.session_state.current_segment = segment_sure
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.header(f"🎙️ Görüşme: {aday if aday else 'Yeni Aday'}")
    
    # İŞTE BURASI DÜZELTİLDİ (89. SATIR)
    c1, c2, c3 = st.columns([0.8, 2, 1])
    
    with c1:
        st.metric("Sorumlu", uzman if uzman else "Belirtilmedi")
        st.metric("Aralık", st.session_state.current_segment)
        if st.button("🛑 Oturumu Bitir"):
            st.session_state.mulakat_aktif = False
            st.rerun()

    with c2:
        st.markdown("<div class='siri-container'><div class='siri-sphere'></div></div>", unsafe_allow_html=True)
        st.write("**🗨️ Canlı Transkript**")
        components.html("""
            <div id="transcript-display">Dinleme bekleniyor...</div>
            <script>
                const display = document.getElementById('transcript-display');
                const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (Recognition) {
                    const rec = new Recognition();
                    rec.lang = 'tr-TR';
                    rec.continuous = true;
                    rec.interimResults = true;
                    rec.onresult = (event) => {
                        let text = '';
                        for (let i = 0; i < event.results.length; i++) {
                            text += event.results[i][0].transcript + ' ';
                        }
                        display.innerText = text;
                    };
                    rec.start();
                    rec.onend = () => rec.start();
                } else {
                    display.innerText = "Desteklenmiyor.";
                }
            </script>
        """, height=280)

    with c3:
        st.write("**🤖 AI Analiz**")
        st.warning("💡 Öneri: Adayın son cevabını analiz edin.")
        fig = go.Figure(go.Scatterpolar(r=[75, 85, 70, 90], theta=['Hız','Güven','Teknik','Uyum'], fill='toself'))
        fig.update_layout(height=250, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
