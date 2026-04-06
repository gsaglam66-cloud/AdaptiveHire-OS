import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components
import random
import string

# --- AI AYARI ---
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AdaptiveHire - AI Presentation Mode", layout="wide")

# --- GELİŞMİŞ CSS (Sunum Modu İçin Özel) ---
st.markdown("""
    <style>
    .stApp { background-color: #fcfdfe; }
    .ah-card { background: white; padding: 25px; border-radius: 15px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    
    /* Sunum Modu Slayt Tasarımı */
    .presentation-slide {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: white;
        padding: 60px;
        border-radius: 20px;
        text-align: center;
        min-height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
        border: 4px solid #3b82f6;
    }
    .slide-question { font-size: 2.5rem; font-weight: 700; line-height: 1.2; margin-bottom: 30px; }
    .slide-footer { font-size: 1rem; color: #94a3b8; letter-spacing: 2px; }
    
    /* Segment Butonları */
    .stRadio > div { flex-direction: row !important; gap: 10px; }
    .stRadio label { background: white !important; border: 1px solid #cbd5e1 !important; padding: 8px 16px !important; border-radius: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "setup"
if 'view_mode' not in st.session_state: st.session_state.view_mode = "Chat" # Chat veya Sunum
if 'current_question' not in st.session_state: st.session_state.current_question = "Mülakata hoş geldiniz. Hazırsanız başlayalım mı?"

# --- ANA AKIŞ ---

# 1. KURULUM EKRANI
if st.session_state.page == "setup":
    st.markdown("## ⚙️ Mülakat Yapılandırması")
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown('<div class="ah-card">', unsafe_allow_html=True)
        st.write("**GÖRÜNÜM MODU SEÇİMİ**")
        # Sunum butonunu burada aktif ediyoruz
        v_mode = st.radio("Mod Seçin", ["Chat", "Sunum", "Otonom"], horizontal=True, label_visibility="collapsed")
        st.session_state.view_mode = v_mode
        
        st.write("<br>**SEGMENT SÜRESİ**", unsafe_allow_html=True)
        st.radio("Süre", ["15 sn", "30 sn", "1 dk", "5 dk"], horizontal=True, label_visibility="collapsed")
        
        st.divider()
        if st.button("Mülakatı Başlat →", type="primary", use_container_width=True):
            st.session_state.page = "live"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# 2. CANLI MÜLAKAT EKRANI
elif st.session_state.page == "live":
    
    # --- SUNUM MODU GÖRÜNÜMÜ ---
    if st.session_state.view_mode == "Sunum":
        st.markdown(f"""
            <div class="presentation-slide">
                <div class="slide-footer">ADAPTIVEHIRE AI QUESTION</div>
                <div class="slide-question">{st.session_state.current_question}</div>
                <div class="slide-footer">LÜTFEN CEVAPLAYINIZ...</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("✨ AI'dan Yeni Soru Üret", use_container_width=True, type="primary"):
                # Burada normalde AI modeline istek atılır, şimdilik simüle ediyoruz
                questions = [
                    "Bize kriz anında aldığınız bir karardan bahseder misiniz?",
                    "Teknik yetkinliklerinizi bu pozisyona nasıl entegre edeceksiniz?",
                    "5 yıl sonraki kariyer hedeflerinizde bu şirketin yeri nedir?",
                    "Takım çalışmasında çatışma yaşadığınız bir anıyı anlatır mısınız?"
                ]
                st.session_state.current_question = random.choice(questions)
                st.rerun()
            if st.button("❌ Sunumdan Çık / Chat Moduna Dön", use_container_width=True):
                st.session_state.view_mode = "Chat"
                st.rerun()

    # --- STANDART CHAT MODU GÖRÜNÜMÜ ---
    else:
        col_main, col_ctrl = st.columns([2.5, 1])
        with col_main:
            st.markdown("### 🎙️ Canlı Görüşme (Chat Modu)")
            st.info(f"AI Sorusu: {st.session_state.current_question}")
            st.markdown('<div style="background:white; border:1px solid #e2e8f0; border-radius:12px; padding:20px; height:300px;">', unsafe_allow_html=True)
            components.html("""
                <div id="log" style="font-family:sans-serif; color:#334155;">🎙️ Ses analizi aktif...</div>
                <script>
                    const Rec = window.webkitSpeechRecognition || window.SpeechRecognition;
                    if(Rec){
                        const r = new Rec(); r.lang='tr-TR'; r.continuous=true; r.interimResults=true;
                        r.onresult = (e) => {
                            let t = ''; for(let i=0; i<e.results.length; i++) t += e.results[i][0].transcript + ' ';
                            document.getElementById('log').innerHTML = '<b>Aday:</b> ' + t;
                        };
                        r.start();
                    }
                </script>
            """, height=250)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_ctrl:
            st.write("**🎛️ Kontrol**")
            if st.button("🖥️ Sunum Moduna Geç", use_container_width=True):
                st.session_state.view_mode = "Sunum"
                st.rerun()
            st.divider()
            if st.button("🛑 Bitir", type="primary", use_container_width=True):
                st.session_state.page = "report"
                st.rerun()

# 3. RAPOR EKRANI
elif st.session_state.page == "report":
    st.markdown("# 📑 Analiz Raporu")
    st.write("Mülakat başarıyla tamamlandı.")
    if st.button("Yeni Mülakat"):
        st.session_state.page = "setup"
        st.rerun()
