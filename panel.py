import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components

# --- AI CONFIG ---
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AdaptiveHire - Panel Interview OS", layout="wide", initial_sidebar_state="expanded")

# --- KURUMSAL CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #fcfdfe; }
    .ah-card { background: white; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 20px; }
    
    /* Canlı Durum Göstergeleri */
    .status-badge { padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }
    .status-online { background: #dcfce7; color: #166534; }
    .status-paused { background: #fef3c7; color: #92400e; }
    
    /* Panelist Kartları */
    .panelist-box { background: #f1f5f9; padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #2563eb; }
    
    /* Segment Butonları */
    .stRadio > div { flex-direction: row !important; gap: 8px; }
    .stRadio label { background: white !important; border: 1px solid #cbd5e1 !important; padding: 6px 12px !important; border-radius: 6px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE YÖNETİMİ ---
if 'page' not in st.session_state: st.session_state.page = "setup"
if 'is_paused' not in st.session_state: st.session_state.is_paused = False
if 'panelists' not in st.session_state: st.session_state.panelists = ["Ana IK Uzmanı (Siz)"]

# --- SIDEBAR: PANEL YÖNETİMİ ---
with st.sidebar:
    st.markdown("<h2 style='color:#2563eb;'>AdaptiveHire</h2>", unsafe_allow_html=True)
    
    st.markdown("### 👥 Görüşme Paneli")
    for p in st.session_state.panelists:
        st.markdown(f'<div class="panelist-box">👤 {p}</div>', unsafe_allow_html=True)
    
    new_panelist = st.text_input("➕ Yeni Uzman Davet Et", placeholder="E-posta veya İsim...")
    if st.button("Davet Gönder"):
        if new_panelist:
            st.session_state.panelists.append(new_panelist)
            st.success(f"{new_panelist} mülakata dahil edildi.")
            st.rerun()

    st.divider()
    if st.button("🏠 Dashboard", use_container_width=True):
        st.session_state.page = "setup"
        st.rerun()

# --- ANA AKIŞ ---

if st.session_state.page == "setup":
    st.subheader("Yeni Panel Mülakatı Yapılandırması")
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown('<div class="ah-card">', unsafe_allow_html=True)
        st.write("**MÜLAKAT PARAMETRELERİ**")
        st.multiselect("Değerlendirme Kriterleri", ["DISC", "Metropolitan", "Teknik Yetkinlik", "Kültürel Uyum"], default=["DISC", "Teknik Yetkinlik"])
        
        st.write("<br>**SEGMENT SÜRESİ**", unsafe_allow_html=True)
        st.radio("Süre", options=["15 sn", "30 sn", "1 dk", "2 dk", "5 dk"], index=1, horizontal=True, label_visibility="collapsed")
        
        st.divider()
        if st.button("Panel Mülakatını Başlat →", type="primary", use_container_width=True):
            st.session_state.page = "live"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "live":
    # CANLI KONTROLÜ (Müdahale Paneli)
    c_header, c_status = st.columns([3, 1])
    with c_header:
        st.markdown("### 🎙️ Panel Mülakatı: Canlı Yayın")
    with c_status:
        if st.session_state.is_paused:
            st.markdown('<span class="status-badge status-paused">⏸️ MÜLAKAT DURDURULDU</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-badge status-online">🔴 CANLI ANALİZ AKTİF</span>', unsafe_allow_html=True)

    col_main, col_admin = st.columns([2.2, 1])

    with col_main:
        # Transkript Alanı
        st.markdown('<div id="transcript-box" style="background:white; border:1px solid #e2e8f0; border-radius:12px; padding:20px; height:450px; overflow-y:auto;">', unsafe_allow_html=True)
        if not st.session_state.is_paused:
            components.html("""
                <div id="out" style="font-family:sans-serif; color:#1e293b; font-size:1.1rem;">🎙️ Adayın konuşması analiz ediliyor...</div>
                <script>
                    const Rec = window.webkitSpeechRecognition || window.SpeechRecognition;
                    if(Rec){
                        const r = new Rec(); r.lang='tr-TR'; r.continuous=true; r.interimResults=true;
                        r.onresult = (e) => {
                            let t = ''; for(let i=0; i<e.results.length; i++) t += e.results[i][0].transcript + ' ';
                            document.getElementById('out').innerHTML = '<b>Aday:</b> ' + t;
                        };
                        r.start();
                    }
                </script>
            """, height=400)
        else:
            st.warning("Mülakat şu anda IK Uzmanı tarafından duraklatıldı. Ses kaydı alınmıyor.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_admin:
        st.markdown("### 🛠️ Uzman Müdahale Paneli")
        
        # 1. ARA VERME / DEVAM ETME
        if st.session_state.is_paused:
            if st.button("▶️ Mülakata Devam Et", use_container_width=True):
                st.session_state.is_paused = False
                st.rerun()
        else:
            if st.button("⏸️ Mülakata Ara Ver", use_container_width=True):
                st.session_state.is_paused = True
                st.rerun()
        
        st.divider()
        
        # 2. VERİLERE MÜDAHALE (Canlı Puanlama)
        st.write("**Anlık Veri Müdahalesi**")
        st.slider("AI Teknik Uyum Puanı (Manuel Müdahale)", 0, 100, 75)
        st.text_area("Özel Not Ekle (Diğer panelistler görebilir)", placeholder="Adayın bu cevabı yetersizdi...")
        
        # 3. DİNAMİK PROMPTLAR
        with st.expander("📝 Envanter Tetikleyiciler", expanded=True):
            st.button("🎯 DISC Analizi Yap", use_container_width=True)
            st.button("📊 Metropolitan Raporla", use_container_width=True)
        
        st.divider()
        if st.button("🛑 Mülakatı Bitir", type="primary", use_container_width=True):
            st.session_state.page = "report"
            st.rerun()

elif st.session_state.page == "report":
    st.markdown("# 📑 Panel Değerlendirme Raporu")
    l, r = st.columns([2, 1])
    with l:
        st.markdown('<div class="ah-card"><h4>Ortak Panel Kararı</h4><p>Tüm IK uzmanlarının ve AI analizinin ortak puanı: <b>%82</b></p><hr><p><b>Not:</b> Mülakat sırasında IK uzmanı tarafından teknik puan manuel olarak revize edilmiştir.</p></div>', unsafe_allow_html=True)
    with r:
        fig = go.Figure(go.Scatterpolar(r=[80, 70, 90, 85], theta=['Teknik','Uyum','DISC-D','Bilişsel'], fill='toself'))
        st.plotly_chart(fig, use_container_width=True)
    
    if st.button("🏠 Dashboard'a Dön"):
        st.session_state.page = "setup"
        st.rerun()
