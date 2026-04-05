import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# --- AI AYARI ---
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="AdaptiveHire - AI Interview OS", layout="wide")

# --- GELİŞMİŞ CSS (Segment Butonları ve Kurumsal Arayüz) ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    /* Segment Süresi Kutucuk Tasarımı */
    div[data-testid="stMarkdownContainer"] > p { font-weight: 600; color: #475569; }
    
    /* Radyo butonlarını yan yana diz ve kutu görünümü ver */
    div[data-row-widget="true"] > div {
        flex-direction: row !important;
        gap: 10px;
    }
    div[data-testid="stWidgetLabel"] { display: none; } /* Etiketi gizle */
    
    .stRadio > div { gap: 10px; }
    .stRadio label {
        background: white;
        border: 1px solid #e2e8f0;
        padding: 8px 15px !important;
        border-radius: 8px !important;
        min-width: 80px;
        text-align: center;
        transition: 0.3s;
    }
    .stRadio label:hover { border-color: #2563eb; background: #eff6ff; }
    
    /* Kart ve Sidebar */
    .ah-card { background: white; padding: 25px; border-radius: 12px; border: 1px solid #e6e9ef; box-shadow: 0 2px 10px rgba(0,0,0,0.02); }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = "setup"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## AdaptiveHire")
    st.caption("Profil: IK Görüşmeleri")
    st.divider()
    if st.button("➕ Yeni Görüşme Aç", use_container_width=True, type="primary"):
        st.session_state.page = "setup"
        st.rerun()

# --- KURULUM EKRANI (Görsel 3 & 10 Referanslı) ---
if st.session_state.page == "setup":
    st.subheader("Oturum Ayarları")
    col_l, col_r = st.columns([1.5, 1])

    with col_l:
        st.markdown('<div class="ah-card">', unsafe_allow_html=True)
        st.write("⏱️ **SEGMENT SÜRESİ**")
        st.caption("Ses kaydı bu süre dolduğunda otomatik olarak kesilip AI'ya gönderilir.")
        
        # Çizgi yerine Çoktan Seçmeli (Ayrı Ayrı Kutular)
        # Horizontal (Yatay) radyo butonu kullanarak referans sitedeki görünümü sağladık
        segment_options = ["15 saniye", "20 saniye", "30 saniye", "1 dakika", "2 dakika", "3 dakika", "5 dakika", "10 dakika"]
        selected_seg = st.radio(
            "Segment Seçimi",
            options=segment_options,
            index=2, # Varsayılan 30 saniye
            horizontal=True,
            label_visibility="collapsed"
        )
        
        st.write("<br>**GÖRÜNÜM MODU**", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        m1.button("💬 Chat", use_container_width=True)
        m2.button("♾️ Otonom", use_container_width=True)
        m3.button("🖥️ Sunum", use_container_width=True)
        
        st.divider()
        if st.button("Başla →", type="primary", use_container_width=True):
            st.session_state.page = "live"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.write("**ÖNİZLEME**")
        st.markdown(f'<div class="ah-card" style="text-align:center; color:#64748b; height:250px;"><br><br>Seçilen Segment: <b>{selected_seg}</b><br>Standart Sohbet Görünümü Aktif</div>', unsafe_allow_html=True)

# --- CANLI EKRAN ---
elif st.session_state.page == "live":
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("### 🎙️ Canlı Transkript")
        st.markdown('<div style="background:white; border:1px solid #eee; padding:20px; border-radius:12px; height:400px;">', unsafe_allow_html=True)
        components.html("""
            <div id="out" style="font-family:sans-serif; color:#334155;">Ses bekleniyor...</div>
            <script>
                const Rec = window.SpeechRecognition || window.webkitSpeechRecognition;
                if(Rec){
                    const r = new Rec(); r.lang='tr-TR'; r.continuous=true; r.interimResults=true;
                    r.onresult = (e) => {
                        let t = ''; for(let i=0; i<e.results.length; i++) t += e.results[i][0].transcript + ' ';
                        document.getElementById('out').innerHTML = '<b>Aday:</b> ' + t;
                    };
                    r.start();
                }
            </script>
        """, height=380)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.write("**🎛️ Kontrol Paneli**")
        #
