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

# --- CSS: LIGHT MODE & 11PX FONT (SABİT) ---
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
    .folder-box {
        background: #f1f5f9; border-radius: 5px; padding: 8px; margin-bottom: 5px;
        border-left: 3px solid #3b82f6; font-size: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE (KURUMSAL VERİ MERKEZİ) ---
if 'page' not in st.session_state: st.session_state.page = "setup"
if 'data_hub' not in st.session_state: st.session_state.data_hub = [] # Klasörleme burada tutulur
if 'current_folder' not in st.session_state: st.session_state.current_folder = None
if 'ik_name' not in st.session_state: st.session_state.ik_name = "İK Uzmanı"
if 'aday_name' not in st.session_state: st.session_state.aday_name = "Aday"

# --- ⬅️ SOL PANEL: KURUMSAL VERİ YÖNETİMİ ---
with st.sidebar:
    st.markdown("<h4>📂 Kurumsal Veri Yönetimi</h4>", unsafe_allow_html=True)
    
    # 1. Klasör / Firma Ekleme Alanı
    with st.expander("➕ Yeni Klasör / Firma Ekle", expanded=False):
        new_firm = st.text_input("Firma Adı")
        new_dept = st.text_input("Çalışılan Birim")
        new_assist = st.text_input("Mülakat Asistanı")
        if st.button("Klasör Oluştur", use_container_width=True):
            if new_firm:
                folder_data = {
                    "id": random.randint(1000, 9999),
                    "firma": new_firm,
                    "birim": new_dept,
                    "asistan": new_assist,
                    "mulakatlar": []
                }
                st.session_state.data_hub.append(folder_data)
                st.success(f"{new_firm} klasörü eklendi!")
            else:
                st.error("Firma adı gerekli.")

    st.divider()
    
    # 2. Mevcut Klasörleri Listeleme
    st.markdown("**Mevcut Klasörler / Projeler**")
    if not st.session_state.data_hub:
        st.info("Henüz klasör oluşturulmadı.")
    else:
        for folder in st.session_state.data_hub:
            with st.container():
                st.markdown(f"""
                <div class="folder-box">
                    <b>🏢 {folder['firma']}</b><br>
                    📍 {folder['birim']} | 🤖 {folder['asistan']}
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Seç: {folder['firma']}", key=f"sel_{folder['id']}", use_container_width=True):
                    st.session_state.current_folder = folder
                    st.session_state.ik_name = folder['asistan'] if folder['asistan'] else "İK Uzmanı"

    st.divider()
    if st.button("🏠 Ana Menü", use_container_width=True):
        st.session_state.page = "setup"
        st.rerun()

# --- APP LOGIC ---
if st.session_state.page == "setup":
    st.title("Mülakat Başlatma Merkezi")
    
    if st.session_state.current_folder:
        st.info(f"📂 Aktif Klasör: **{st.session_state.current_folder['firma']}** ({st.session_state.current_folder['birim']})")
    else:
        st.warning("Lütfen sol panelden bir klasör seçin veya yeni bir tane oluşturun.")

    col = st.columns([1, 2, 1])[1]
    with col:
        st.markdown('<div class="corporate-card">', unsafe_allow_html=True)
        st.write("**Mülakat Detayları**")
        st.session_state.aday_name = st.text_input("Adayın Adı Soyadı", st.session_state.aday_name)
        st.text_input("Pozisyon", "Kıdemli Yazılım Geliştirici")
        
        # Mülakat Başlatma (Klasör seçili değilse butonu deaktif edebiliriz ama esneklik için açık bırakıyorum)
        if st.button("🔴 CANLI MÜLAKATA GEÇ", type="primary", use_container_width=True):
            if st.session_state.current_folder:
                st.session_state.page = "live"
                st.rerun()
            else:
                st.error("Mülakatı başlatmak için önce bir KLASÖR seçmelisiniz!")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "live":
    c1, c2 = st.columns([2.2, 1])
    
    with c1:
        st.markdown(f"**OTURUM:** {st.session_state.ik_name} (İK) ↔ {st.session_state.aday_name} (Aday)")
        
        # JS Kodunu f-string hatasından korumak için (Önceki Çözümümüz)
        js_raw = """
        <div id="chat-box" style="height:450px; overflow-y:auto; display:flex; flex-direction:column; gap:8px; font-family:sans-serif; padding:10px;"></div>
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
                            d.style = "display:flex; width:100%; margin-bottom:10px; justify-content:" + (isIK ? 'flex-start' : 'flex-end');
                            
                            const b = document.createElement('div');
                            b.style = isIK ? "background:#fef2f2; color:#991b1b; padding:10px; border-radius:0 10px 10px 10px; border:1px solid #fee2e2; max-width:80%; font-size:11px;" : "background:#eff6ff; color:#1e40af; padding:10px; border-radius:10px 0 10px 10px; border:1px solid #dbeafe; max-width:80%; font-size:11px;";
                            b.innerHTML = '<b style="font-size:9px; display:block; margin-bottom:2px; opacity:0.6;">' + (isIK ? ik : aday) + '</b>' + t;
                            
                            d.appendChild(b);
                            box.appendChild(d);
                            box.scrollTop = box.scrollHeight;
                        }
                    }
                };
                r.start();
            }
        </script>
        """
        js_final = js_raw.replace("VAR_IK_NAME", st.session_state.ik_name).replace("VAR_ADAY_NAME", st.session_state.aday_name)
        components.html(js_final, height=480)

    with c2:
        st.markdown("#### 📊 Anlık Raporlama")
        st.markdown('<div class="corporate-card">', unsafe_allow_html=True)
        st.write(f"📂 Klasör: {st.session_state.current_folder['firma']}")
        st.progress(0.70, text="NLP Analiz")
        st.progress(0.40, text="Dürüstlük")
        st.divider()
        if st.button("Mülakatı Kaydet ve Bitir", type="primary", use_container_width=True):
            # Mülakat sonucunu klasöre kaydetme simülasyonu
            st.session_state.current_folder['mulakatlar'].append(st.session_state.aday_name)
            st.session_state.page = "report"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "report":
    st.success(f"Mülakat verileri '{st.session_state.current_folder['firma']}' klasörüne kaydedildi.")
    st.markdown(f"**Aday:** {st.session_state.aday_name}")
    if st.button("Yeni Mülakat Başlat", use_container_width=True):
        st.session_state.page = "setup"
        st.rerun()
