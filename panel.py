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

st.set_page_config(page_title="AdaptiveHire - Autonomous AI Interview", layout="wide")

# --- GELİŞMİŞ CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #fcfdfe; }
    .ah-card { background: white; padding: 25px; border-radius: 15px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    .status-online { background: #dcfce7; color: #166534; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; }
    .link-box { background: #f1f5f9; padding: 15px; border-radius: 8px; border: 1px dashed #2563eb; font-family: monospace; margin: 10px 0; }
    /* Segment Seçim Kutuları */
    .stRadio > div { flex-direction: row !important; gap: 10px; }
    .stRadio label { background: white !important; border: 1px solid #cbd5e1 !important; padding: 8px 16px !important; border-radius: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'mode' not in st.session_state: st.session_state.mode = "admin" # admin veya candidate
if 'page' not in st.session_state: st.session_state.page = "dashboard"
if 'interview_link' not in st.session_state: st.session_state.interview_link = ""

def generate_link():
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"https://adaptivehire.ai/interview/{suffix}"

# --- SIDEBAR ---
with st.sidebar:
    st.title("AdaptiveHire")
    if st.session_state.mode == "admin":
        st.subheader("👨‍💼 IK Yönetim Paneli")
        if st.button("📊 Dashboard'a Dön", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
    else:
        st.subheader("👤 Aday Girişi")
        st.info("Otonom Mülakat Sistemi Aktif")

# --- ANA AKIŞ ---

# 1. ADMIN DASHBOARD: Link Oluşturma Ekranı
if st.session_state.page == "dashboard" and st.session_state.mode == "admin":
    st.markdown("## Mülakat Yönetimi")
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown('<div class="ah-card">', unsafe_allow_html=True)
        st.write("### 🔗 Otonom Mülakat Linki Oluştur")
        st.write("Adaya gönderilecek link ile mülakatı AI'nın yönetmesini sağlayın.")
        
        target_role = st.text_input("Pozisyon Adı", "Kıdemli Yazılım Geliştirici")
        test_type = st.multiselect("Uygulanacak Envanterler", ["DISC", "Metropolitan", "Big Five", "Teknik Case"], default=["DISC"])
        
        if st.button("Özel Mülakat Linki Oluştur", type="primary"):
            st.session_state.interview_link = generate_link()
            
        if st.session_state.interview_link:
            st.markdown(f'<div class="link-box">{st.session_state.interview_link}</div>', unsafe_allow_html=True)
            st.success("Link oluşturuldu! Bu linki adaya e-posta ile gönderebilirsiniz.")
            
            if st.button("Aday Ekranını Simüle Et (Önizleme)"):
                st.session_state.mode = "candidate"
                st.session_state.page = "candidate_welcome"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# 2. ADAY KARŞILAMA EKRANI (Linke tıkladığında gelen yer)
elif st.session_state.page == "candidate_welcome" and st.session_state.mode == "candidate":
    st.markdown("<h1 style='text-align: center;'>AdaptiveHire Mülakat Platformu</h1>", unsafe_allow_html=True)
    st.markdown('<div class="ah-card" style="max-width: 700px; margin: auto; text-align: center;">', unsafe_allow_html=True)
    st.write("### Hoş Geldiniz!")
    st.write("Bu mülakat Yapay Zeka (AI) tarafından yönetilecektir. Lütfen sessiz bir ortamda olduğunuzdan ve mikrofonunuzun çalıştığından emin olun.")
    st.write("**Pozisyon:** Kıdemli Yazılım Geliştirici")
    st.write("**Tahmini Süre:** 15 Dakika")
    
    if st.button("Sistemi Kontrol Et ve Başla →", type="primary", use_container_width=True):
        st.session_state.page = "candidate_live"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 3. OTONOM CANLI MÜLAKAT (AI Soru Sorar - Aday Cevaplar)
elif st.session_state.page == "candidate_live":
    st.markdown('<span class="status-online">🔴 OTONOM MÜLAKAT AKTİF</span>', unsafe_allow_html=True)
    
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown('<div class="ah-card">', unsafe_allow_html=True)
        st.write("### 🤖 AI Mülakatçı")
        st.info("AI: 'Hoş geldiniz. Öncelikle bize son projenizde karşılaştığınız en büyük teknik zorluktan bahseder misiniz?'")
        
        st.markdown('<div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:20px; height:300px; margin-top:20px;">', unsafe_allow_html=True)
        components.html("""
            <div id="log" style="font-family:sans-serif; color:#334155;">🎙️ Sizi dinliyorum, lütfen konuşun...</div>
            <script>
                const Rec = window.webkitSpeechRecognition || window.SpeechRecognition;
                if(Rec){
                    const r = new Rec(); r.lang='tr-TR'; r.continuous=true; r.interimResults=true;
                    r.onresult = (e) => {
                        let t = ''; for(let i=0; i<e.results.length; i++) t += e.results[i][0].transcript + ' ';
                        document.getElementById('log').innerHTML = '<b style="color:#2563eb;">Siz:</b> ' + t;
                    };
                    r.start();
                }
            </script>
        """, height=250)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.write("**İlerleme**")
        st.progress(25)
        st.write("Soru 1 / 4")
        st.divider()
        st.warning("Mülakat sırasında sayfayı kapatmayın. AI konuşmanızı anlık analiz ederek DISC profilinizi oluşturuyor.")
        if st.button("Mülakatı Tamamla ve Gönder", use_container_width=True):
            st.session_state.page = "finish"
            st.rerun()

# 4. BİTİŞ EKRANI
elif st.session_state.page == "finish":
    st.balloons()
    st.markdown('<div class="ah-card" style="max-width: 600px; margin: auto; text-align: center;">', unsafe_allow_html=True)
    st.write("## Teşekkürler!")
    st.write("Mülakatınız başarıyla tamamlandı ve analiz edilmek üzere IK birimine iletildi.")
    st.write("Sonuçlar hakkında tarafınıza e-posta gönderilecektir.")
    if st.button("Admin Paneline Dön (Simülasyon Sonu)"):
        st.session_state.mode = "admin"
        st.session_state.page = "dashboard"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
