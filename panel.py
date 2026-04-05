import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components

# --- AI AYARI ---
API_KEY = "BURAYA_API_ANAHTARINI_YAZ" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="NLC - Control Panel", layout="wide", initial_sidebar_state="expanded")

# --- GELİŞMİŞ KURUMSAL CSS (Kontrol Paneli Detayları) ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    
    /* Sağ Panel - Kontrol Kartları */
    .control-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin-bottom: 10px;
        font-size: 13px;
    }
    .report-badge {
        background-color: #eef2ff;
        color: #4338ca;
        padding: 4px 8px;
        border-radius: 5px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    
    /* Mesaj Giriş Alanı */
    .input-container {
        position: fixed;
        bottom: 20px;
        width: 50%;
        left: 25%;
        background: white;
        padding: 10px;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
    }
    
    /* Siri Halkası Küçültüldü */
    .siri-mini {
        width: 40px; height: 40px; border-radius: 50%;
        background: linear-gradient(45deg, #00d2ff, #ff00c1);
        animation: pulse 2s infinite alternate;
    }
    @keyframes pulse { from { transform: scale(1); opacity: 0.8; } to { transform: scale(1.1); opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# --- SOL SIDEBAR (Görüşme Listesi) ---
with st.sidebar:
    st.title("Danışan Görüşmeleri")
    st.info("👤 Sorumlu: Şamil ALBAYRAK\n\n📌 Görüşme 9")
    st.divider()
    st.button("📄 Aday Profil Raporu")
    st.button("📊 Potansiyel Riskler")
    st.button("⚙️ Teknik Yetkinlikler")
    st.button("🧠 Psikososyal Analiz")

# --- ANA EKRAN AKIŞI ---
if 'mulakat_aktif' not in st.session_state:
    st.session_state.mulakat_aktif = False

if not st.session_state.mulakat_aktif:
    # --- AYAR EKRANI ---
    st.subheader("Oturum Ayarları")
    if st.button("MÜLAKATI BAŞLAT →"):
        st.session_state.mulakat_aktif = True
        st.rerun()
else:
    # --- CANLI MÜLAKAT VE KONTROL PANELİ ---
    col_chat, col_ctrl = st.columns([2, 1])
    
    with col_chat:
        st.markdown("### 🎙️ Görüşme Akışı")
        
        # Siri Mini Görseli
        st.markdown("<div class='siri-mini'></div>", unsafe_allow_html=True)
        
        # Canlı Transkript Kutusu
        components.html("""
            <div id="display" style="background:white; border:1px solid #eee; padding:20px; border-radius:15px; height:450px; overflow-y:auto;">
                <i>Sistem dinliyor... Konuşmalar burada anlık olarak belirecek.</i>
            </div>
            <script>
                const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (Recognition) {
                    const rec = new Recognition();
                    rec.lang = 'tr-TR'; rec.continuous = true; rec.interimResults = true;
                    rec.onresult = (e) => {
                        let t = '';
                        for (let i = 0; i < e.results.length; i++) { t += e.results[i][0].transcript + ' '; }
                        document.getElementById('display').innerText = t;
                    };
                    rec.start();
                }
            </script>
        """, height=480)
        
        # --- MANUEL ANALİZ VE MESAJ GİRİŞİ ---
        st.divider()
        c_msg, c_send = st.columns([5, 1])
        with c_msg:
            user_msg = st.text_input("Yapay zekaya talimat verin veya aday cevabını manuel gönderin...", placeholder="Mesajınızı yazın...")
        with c_send:
            if st.button("🚀 GÖNDER"):
                st.toast("Analiz periyodu beklenmeden veri AI'ya iletildi!")

    with col_ctrl:
        st.markdown("### 🛠️ Kontrol Paneli")
        
        with st.expander("📝 Dinamik Promptlar", expanded=True):
            st.markdown("<div class='report-badge'>Rapor 5a - Aday Profili</div>", unsafe_allow_html=True)
            st.write("Adayın genel profilini ve kronolojik iş geçmişini özetler.")
            
            st.markdown("<div class='report-badge'>Rapor 5b - Potansiyel Riskler</div>", unsafe_allow_html=True)
            st.write("Cevaplardaki tutarsızlıkları ve riskli alanları tarar.")
            
            st.markdown("<div class='report-badge'>Rapor 5c - Teknik Yetkinlik</div>", unsafe_allow_html=True)
            st.write("Belirlenen görev tanımına göre teknik puanlama yapar.")

        st.divider()
        st.write("**🧠 Model Seçimi**")
        st.selectbox("Kullanılan Zeka:", ["Gemini 1.5 Pro (Adaptive)", "NLC Cortex v2", "GPT-4 Turbo Hybrid"])
        
        st.divider()
        if st.button("🛑 Görüşmeyi Bitir ve Rapor Oluştur"):
            st.session_state.mulakat_aktif = False
            st.rerun()
