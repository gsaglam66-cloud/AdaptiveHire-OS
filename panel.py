import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components
import time

# --- AI CONFIGURATION ---
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="AdaptiveHire - Real-Time AI Interview", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS (KURUMSAL ARABİRİM) ---
st.markdown("""
    <style>
    /* Genel Arka Plan ve Font */
    .stApp { background-color: #f4f7f9; font-family: 'Inter', sans-serif; }
    
    /* Sidebar Tasarımı */
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #dee2e6; min-width: 320px !important; }
    
    /* Kurumsal Kartlar (Görsel 1 & 4 esintili) */
    .ah-card {
        background: white; padding: 25px; border-radius: 12px;
        border: 1px solid #e9ecef; box-shadow: 0 4px 12px rgba(0,0,0,0.03); margin-bottom: 20px;
    }
    
    /* Sarı Aktif Görüşme Kartları (Görsel 1 esintili) */
    .active-interview-item {
        background-color: #fffbe6; border: 1px solid #ffe58f;
        padding: 12px; border-radius: 8px; margin-bottom: 10px; font-size: 13px;
    }

    /* Kontrol Paneli Rapor Butonları (Görsel 4 esintili) */
    .report-grid-item {
        background: #ffffff; border: 1px solid #dbeafe; padding: 12px;
        border-radius: 8px; text-align: left; font-size: 12px; transition: 0.2s;
    }
    .report-grid-item:hover { border-color: #2563eb; background: #f0f7ff; }

    /* Siri Efekti (Adaptive Pulse) */
    .siri-pulse {
        width: 50px; height: 50px; border-radius: 50%;
        background: linear-gradient(45deg, #2563eb, #7c3aed);
        animation: pulse-ring 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    @keyframes pulse-ring { 0% { transform: scale(0.95); opacity: 0.8; } 50% { transform: scale(1.1); opacity: 1; } 100% { transform: scale(0.95); opacity: 0.8; } }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE YÖNETİMİ ---
if 'step' not in st.session_state: st.session_state.step = "dashboard" # dashboard, setup, interview, report

# --- SOL NAVİGASYON (Görsel 1 & 3) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1063/1063376.png", width=50) # Logo Placeholder
    st.title("AdaptiveHire")
    
    st.markdown("### 📁 Profil Yönetimi")
    with st.expander("Aktif Klasörler", expanded=True):
        st.write("📂 IK Teknik Mülakatlar")
        st.write("📂 Üst Düzey Yönetici Seçimi")
        st.write("📂 Kampüs Yeni Mezun")
    
    st.divider()
    if st.button("➕ Yeni Görüşme Oluştur", use_container_width=True, type="primary"):
        st.session_state.step = "setup"
        st.rerun()
    
    st.divider()
    st.caption("Geçmiş Görüşmeler")
    st.markdown('<div class="active-interview-item"><b>Görüşme #09</b><br>Kıdemli Yazılım Müh.</div>', unsafe_allow_html=True)
    st.markdown('<div class="active-interview-item" style="background:#fff;"><b>Görüşme #08</b><br>Ürün Müdürü</div>', unsafe_allow_html=True)

# --- ANA EKRAN MANTIĞI ---

# 1. EKRAN: DASHBOARD (Görsel 3)
if st.session_state.step == "dashboard":
    st.title("Hoş Geldiniz! 👋")
    st.write("AdaptiveHire platformu ile mülakat süreçlerinizi yapay zeka ile optimize edin.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="ah-card"><h3>🚀 Yeni Görüşme</h3><p>Anlık transkript ve adaptif analiz ile mülakatı başlatın.</p></div>', unsafe_allow_html=True)
        if st.button("Hemen Başlat"): 
            st.session_state.step = "setup"
            st.rerun()
    with col2:
        st.markdown('<div class="ah-card"><h3>📊 Organizasyon</h3><p>Ekiplerinizi ve yetki tanımlarını buradan yönetin.</p></div>', unsafe_allow_html=True)

# 2. EKRAN: AYARLAR (Görsel 1 & 3 Modal)
elif st.session_state.step == "setup":
    st.subheader("Yeni Görüşme Yapılandırması")
    col_s, col_p = st.columns([1.5, 1])
    
    with col_s:
        st.markdown('<div class="ah-card">', unsafe_allow_html=True)
        aday_ad = st.text_input("Aday Adı Soyadı", placeholder="Örn: Ahmet Yılmaz")
        pozisyon = st.selectbox("Pozisyon Profili", ["Teknik Uzman", "Yönetici", "Satış Temsilcisi", "Psikometrik Tarama"])
        
        st.write("**SEGMENT SÜRESİ (ANALİZ ARALIĞI)**")
        seg = st.select_slider("", options=["15 sn", "30 sn", "1 dk", "2 dk", "5 dk"], value="30 sn")
        
        if st.button("Görüşmeyi Başlat →", type="primary", use_container_width=True):
            st.session_state.step = "interview"
            st.session_state.aday = aday_ad
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# 3. EKRAN: MÜLAKAT VE KONTROL PANELİ (Görsel 4)
elif st.session_state.step == "interview":
    st.header(f"🎙️ Canlı Mülakat: {st.session_state.aday}")
    
    col_trans, col_ctrl = st.columns([2, 1])
    
    with col_trans:
        # Transkript Alanı
        st.markdown('<div class="ah-card" style="height:550px; position:relative;">', unsafe_allow_html=True)
        st.markdown("<div style='display:flex; align-items:center; gap:15px; margin-bottom:20px;'><div class='siri-pulse'></div><b>Sistem Anlık Dinliyor...</b></div>", unsafe_allow_html=True)
        
        # Real-time Speech API
        components.html("""
            <div id="t-box" style="font-size:16px; color:#333; line-height:1.6; height:350px; overflow-y:auto; border-bottom:1px solid #eee; padding-bottom:10px;">
                <i>Lütfen konuşmaya başlayın...</i>
            </div>
            <script>
                const box = document.getElementById('t-box');
                const Rec = window.SpeechRecognition || window.webkitSpeechRecognition;
                if(Rec){
                    const r = new Rec(); r.lang='tr-TR'; r.continuous=true; r.interimResults=true;
                    r.onresult = (e) => { 
                        let txt = ''; for(let i=0; i<e.results.length; i++){ txt += e.results[i][0].transcript + ' '; }
                        box.innerText = txt;
                    };
                    r.start();
                }
            </script>
        """, height=400)
        
        # Manuel Giriş (Görsel 4 alt bar)
        msg = st.text_input("AI'ya komut verin veya manuel not ekleyin...", placeholder="Örn: 'Bu cevabı teknik açıdan derinleştir'")
        if st.button("Gönder 🚀"): st.toast("AI talimatı aldı.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_ctrl:
        st.markdown("### 📋 Kontrol Paneli")
        with st.expander("🎯 Dinamik Rapor Modülleri", expanded=True):
            cols = st.columns(2)
            moduller = ["Aday Profili", "Potansiyel Riskler", "Teknik Yetkinlik", "Soft Skills", "Psikososyal", "Holistik Değ."]
            for i, m in enumerate(moduller):
                cols[i%2].markdown(f'<div class="report-grid-item">📄 {m}</div>', unsafe_allow_html=True)
        
        st.divider()
        st.write("**🤖 Adaptif Soru Önerisi**")
        st.info("💡 Adayın önceki tecrübesindeki kriz yönetimini anlamak için 'En zorlandığınız projeyi anlatır mısınız?' sorusunu yöneltin.")
        
        if st.button("🛑 Görüşmeyi Bitir ve Raporla", use_container_width=True, type="secondary"):
            st.session_state.step = "report"
            st.rerun()

# 4. EKRAN: RAPORLAMA
elif st.session_state.step == "report":
    st.title("📑 Mülakat Değerlendirme Raporu")
    st.subheader(f"Aday: {st.session_state.aday}")
    
    col_r1, col_r2 = st.columns([2, 1])
    with col_r1:
        st.markdown('<div class="ah-card"><h4>Yönetici Özeti (1 Sayfa)</h4><p>Adayın teknik yeterliliği yüksek ancak ekip uyumu konusunda çekinceler mevcut. Adaptif sorgulama sırasında liderlik potansiyeli %75 olarak ölçüldü.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="ah-card"><h4>Detaylı Analiz</h4><ul><li>Teknik Bilgi: 8.5/10</li><li>İletişim: 7.0/10</li><li>Problem Çözme: 9.0/10</li></ul></div>', unsafe_allow_html=True)
    with col_r2:
        # Radar Grafik
        fig = go.Figure(go.Scatterpolar(r=[8.5, 7, 9, 8], theta=['Teknik','Sosyal','Analitik','Uyum'], fill='toself'))
        st.plotly_chart(fig, use_container_width=True)
        st.button("📥 PDF Olarak İndir")
        if st.button("🏠 Ana Sayfaya Dön"):
            st.session_state.step = "dashboard"
            st.rerun()
