import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components
import random

# --- AI CONFIG ---
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AdaptiveHire | OS", layout="wide", initial_sidebar_state="expanded")

# --- CSS: LIGHT MODE & 11PX FONT ---
st.markdown("""
<style>
    html, body, [class*="st-"] { 
        font-family: 'Segoe UI', sans-serif; 
        background-color: #f8fafc; 
        color: #334155;
        font-size: 11px !important;
    }
    h1, h2, h3, h4 { color: #1e293b !important; font-weight: 600 !important; }
    h4 { font-size: 13px !important; margin-bottom: 8px !important; }
    .corporate-card {
        background: white; border: 1px solid #e2e8f0;
        border-radius: 8px; padding: 12px; margin-bottom: 12px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    #chat-scroll {
        height: 480px; overflow-y: auto; padding: 15px;
        background: white; border: 1px solid #e2e8f0; border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "setup"
if 'ik_name' not in st.session_state: st.session_state.ik_name = "İK Uzmanı"
if 'aday_name' not in st.session_state: st.session_state.aday_name = "Aday"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h4>🏢 Kurumsal Panel</h4>", unsafe_allow_html=True)
    st.text_input("Şirket", "AdaptiveHire Global", disabled=True)
    st.divider()
    st.session_state.ik_name = st.text_input("Görüşmeci", st.session_state.ik_name)
    st.session_state.aday_name = st.text_input("Aday", st.session_state.aday_name)
    if st.button("🏠 Ana Menü", use_container_width=True):
        st.session_state.page = "setup"
        st.rerun()

# --- APP LOGIC ---
if st.session_state.page == "setup":
    st.title("Mülakat Yönetimi")
    col = st.columns([1, 2, 1])[1]
    with col:
        st.markdown('<div class="corporate-card">', unsafe_allow_html=True)
        st.write("**Oturum Başlat**")
        if st.button("MÜLAKATI BAŞLAT", type="primary", use_container_width=True):
            st.session_state.page = "live"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "live":
    c1, c2 = st.columns([2.2, 1])
    
    with c1:
        st.markdown(f"**OTURUM:** {st.session_state.ik_name} & {st.session_state.aday_name}")
        
        # JS Kodunu f-string hatasından korumak için değişkenleri ayırıyoruz
        js_code = """
        <div id="chat-box" style="height:450px; overflow-y:auto; display:flex; flex-direction:column; gap:10px; font-family:sans-serif; padding:10px;"></div>
        <script>
            const ik = "VAR_IK_NAME";
            const aday = "VAR_ADAY_NAME";
            const box = document.getElementById('chat-box');
            const Rec = window.webkitSpeechRecognition || window.SpeechRecognition;
            
            if(Rec) {
                const r = new Rec();
                r.lang = 'tr-TR'; r.continuous = true; r.interimResults = true;
                let lastT = "";

                r.onresult = (e) => {
                    for (let i = e.resultIndex; i < e.results.length; i++) {
                        if (e.results[i].isFinal) {
                            let t = e.results[i][0].transcript.trim();
                            if(t === lastT) return;
                            lastT = t;
                            
                            let isIK = t.toLowerCase().includes('?') || t.toLowerCase().includes('mi');
                            const d = document.createElement('div');
                            d.style = "display:flex; width:100%; justify-content:" + (isIK ? 'flex-start' : 'flex-end');
                            
                            const b = document.createElement('div');
                            b.style = isIK ? "background:#fef2f2; color:#991b1b; padding:10px; border-radius:0 10px 10px 10px; border:1px solid #fee2e2; max-width:80%; font-size:11px;" : "background:#eff6ff; color:#1e40af; padding:10px; border-radius:10px 0 10px 10px; border:1px solid #dbeafe; max-width:80%; font-size:11px;";
                            b.innerHTML = '<b style="font-size:9px; display:block; margin-bottom:3px; opacity:0.6;">' + (isIK ? ik : aday) + '</b>' + t;
                            
                            d.appendChild(b);
                            box.appendChild(d);
                            box.scrollTop = box.scrollHeight;
                        }
                    }
                };
                r.start();
            }
        </script>
        """.replace("VAR_IK_NAME", st.session_state.ik_name).replace("VAR_ADAY_NAME", st.session_state.aday_name)
        
        components.html(js_code, height=480)

    with c2:
        st.markdown("#### 📊 Analiz")
        st.markdown('<div class="corporate-card">', unsafe_allow_html=True)
        st.progress(0.70, text="NLP Analiz: %70")
        st.progress(0.45, text="Stres: %45")
        st.divider()
        if st.button("Bitir", type="primary", use_container_width=True):
            st.session_state.page = "report"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "report":
    st.success("Mülakat Tamamlandı.")
    st.button("Başa Dön", on_click=lambda: st.session_state.update({"page":"setup"}))
