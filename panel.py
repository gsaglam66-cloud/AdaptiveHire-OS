import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components

# --- AI AYARI ---
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Sayfa Genişlik ve Tema Ayarı
st.set_page_config(page_title="NLC - Neo Limbic Cortex", layout="wide", initial_sidebar_state="expanded")

# --- GELİŞMİŞ KURUMSAL CSS (Görseldeki Tasarım) ---
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp { background-color: #f8f9fa; }
    
    /* Sol Sidebar Tasarımı */
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e0e0e0; min-width: 350px !important; }
    
    /* Kurumsal Kart Yapısı (Setup Card) */
    .setup-card {
        background: white;
        padding: 40px;
        border-radius: 12px;
        border: 1px solid #e6e9ef;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    }

    /* Sol Panel Görüşme Kartları */
    .interview-card {
        background-color: #fff9db; /* Görseldeki sarımtırak ton */
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #ffe066;
        margin-bottom: 10px;
        cursor: pointer;
    }
    
    /* Buton Tasarımları */
    .stButton>button { border-radius: 8px; border: 1px solid #dcdfe6; background: white; transition: 0.3s; }
    .stButton>button:hover { border-color: #409eff; color: #409eff; }
    
    /* Başlat Butonu (Mavi) */
    .main-btn button {
        background-color: #2563eb !important;
        color: white !important;
        width: 100%;
        font-weight: bold;
        height: 50px;
    }

    /* Transkript Kutusu (Siyah Ekran) */
    #transcript-display {
        background-color: #ffffff; color: #333; padding: 20px;
        border-radius: 12px; border: 1px solid #e0e0e0;
        height: 400px; overflow-y: auto; font-size: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SOL SIDEBAR (Görseldeki Navigasyon) ---
with st.sidebar:
    st.title("Danışan Görüşmeleri")
    
    # Profil Kartı
    st.markdown(f"""
    <div style="background: #f1f3f5; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <p style="margin:0; font-size: 12px; color: #666;">📁 IK Görüşmeleri Profili</p>
        <h4 style="margin:5px 0;">Örn: Şamil ALBAYRAK</h4>
        <p style="margin:0; font-size: 11px; color: #888;">Görüşme Sayısı: 8</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.text_input("🔍 Görüşme ara...", placeholder="Aday veya tarih yazın")
    
    col_btn1, col_btn2 = st.columns(2)
    col_btn1.button("Kayıt Tarihi", use_container_width=True)
    col_btn2.button("Son Güncelleme", use_container_width=True)
    
    st.button("➕ Yeni Görüşme Aç", use_container_width=True, type="primary")
    
    st.divider()
    
    # Geçmiş Görüşme Kartları (Görseldeki Sarı Kartlar)
    for i in range(9, 6, -1):
        st.markdown(f"""
        <div class="interview-card">
            <div style="display: flex; justify-content: space-between;">
                <strong>Görüşme {i}</strong>
                <span style="font-size: 10px; color: #888;">00:44</span>
            </div>
            <p style="font-size: 11px; color: #666; margin: 5px 0;">IK Görüşmeleri Profili<br>Alan Becerisi Uzmanı v8</p>
        </div>
        """, unsafe_allow_html=True)

# --- ANA EKRAN AKIŞI ---
if 'mulakat_aktif' not in st.session_state:
    st.session_state.mulakat_aktif = False

if not st.session_state.mulakat_aktif:
    # --- GÖRSELDEKİ SETUP EKRANI ---
    st.subheader("Görüşme 9")
    
    col_setup, col_preview = st.columns([1.2, 1])
    
    with col_setup:
        st.markdown('<div class="setup-card">', unsafe_allow_html=True)
        st.subheader("Oturum Ayarları")
        st.caption("Başlamadan önce tercihlerinizi seçin")
        
        st.write("**GÖRÜNÜM MODU**")
        m1, m2, m3 = st.columns(3)
        m1.button("💬 Chat", use_container_width=True)
        m2.button("♾️ Otonom", use_container_width=True)
        m3.button("🖥️ Sunum", use_container_width=True)
        
        st.write("**GİRİŞ KAYNAĞI**")
        g1, g2 = st.columns(2)
        g1.button("🎤 Sadece Mikrofon", use_container_width=True)
        g2.button("🖥️ Sistem Sesi", use_container_width=True)
        
        st.write("**⏱️ SEGMENT SÜRESİ**")
        seg_options = ["15 sn", "20 sn", "30 sn", "1 dk", "2 dk", "5 dk", "10 dk"]
        selected_seg = st.select_slider("", options=seg_options, value="30 sn", label_visibility="collapsed")
        
        st.divider()
        st.markdown('<div class="main-btn">', unsafe_allow_html=True)
        if st.button("Başla →"):
            st.session_state.mulakat_aktif = True
            st.session_state.seg = selected_seg
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_preview:
        st.write("**ÖNİZLEME**")
        st.image("https://cdn-icons-png.flaticon.com/512/2593/2593491.png", width=60)
        st.caption("Standart sohbet görünümü aktif.")
        st.info("Mülakat başladığında analizler burada akacaktır.")

else:
    # --- CANLI MÜLAKAT ODASI (SIRI VE TRANSKRIPT) ---
    st.header(f"🎙️ Görüşme Modu Aktif")
    
    c_side, c_mid, c_stat = st.columns([0.7, 2, 1])
    
    with c_side:
        st.button("🔙 Ayarlara Dön", on_click=lambda: st.session_state.update({"mulakat_aktif": False}))
        st.metric("Seçilen Segment", st.session_state.seg)

    with c_mid:
        # Siri Animasyonu
        st.markdown("""
        <div style="display: flex; justify-content: center; margin-bottom: 20px;">
            <div class="siri-sphere" style="width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(45deg, #00d2ff, #ff00c1); animation: pulse 2s infinite alternate;"></div>
        </div>
        <style>@keyframes pulse { from { transform: scale(1); opacity: 0.8; } to { transform: scale(1.2); opacity: 1; } }</style>
        """, unsafe_allow_html=True)
        
        # ANLIK TRANSKRIPT (JavaScript)
        components.html("""
            <div id="transcript-display" style="background:#fff; border:1px solid #eee; padding:20px; border-radius:12px; height:350px; overflow-y:auto; font-family:sans-serif;">Dinleme bekleniyor...</div>
            <script>
                const display = document.getElementById('transcript-display');
                const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (Recognition) {
                    const rec = new Recognition();
                    rec.lang = 'tr-TR'; rec.continuous = true; rec.interimResults = true;
                    rec.onresult = (e) => {
                        let t = '';
                        for (let i = 0; i < e.results.length; i++) { t += e.results[i][0].transcript + ' '; }
                        display.innerText = t;
                    };
                    rec.start();
                }
            </script>
        """, height=400)

    with c_stat:
        st.write("**🤖 AI Önerileri**")
        st.warning("💡 Adayın akıcılığı %85. Teknik sorulara geçebilirsiniz.")
        # Küçük Radar Grafiği
        fig = go.Figure(go.Scatterpolar(r=[80, 70, 90, 60], theta=['Hız','Güven','Teknik','Uyum'], fill='toself'))
        fig.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
