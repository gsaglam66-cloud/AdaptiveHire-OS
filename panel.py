import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components
import random

# --- AI AYARI ---
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AdaptiveHire - Enterprise OS", layout="wide", initial_sidebar_state="expanded")

# --- KURUMSAL DARK THEME CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #f8fafc; }
    
    /* Sol Panel (İşletme Bilgileri) */
    .company-section { background: #1e293b; padding: 15px; border-radius: 10px; border-bottom: 2px solid #3b82f6; margin-bottom: 20px; }
    
    /* Sağ Panel (Raporlama) */
    .report-card { background: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #334155; margin-top: 10px; }
    
    /* Chat Konteynırı */
    #chat-container { 
        height: 500px; overflow-y: auto; padding: 20px; 
        background: #020617; border-radius: 15px; border: 1px solid #1e293b;
        display: flex; flex-direction: column; gap: 15px;
    }
    
    /* Mesaj Balonları (Kırmızı & Mavi Sabit) */
    .ik-row { display: flex; justify-content: flex-start; width: 100%; }
    .ik-bubble { background: #450a0a; border-left: 4px solid #ef4444; color: #fecaca; padding: 12px; border-radius: 0 12px 12px 12px; max-width: 80%; }
    
    .aday-row { display: flex; justify-content: flex-end; width: 100%; }
    .aday-bubble { background: #1e3a8a; border-right: 4px solid #3b82f6; color: #dbeafe; padding: 12px; border-radius: 12px 0 12px 12px; max-width: 80%; text-align: right; }
    
    .label { font-size: 0.7rem; font-weight: bold; margin-bottom: 4px; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "setup"
if 'ik_name' not in st.session_state: st.session_state.ik_name = "İK Uzmanı"
if 'aday_name' not in st.session_state: st.session_state.aday_name = "Aday"

# --- ⬅️ SOL PANEL: İŞLETME BİLGİLERİ ---
with st.sidebar:
    st.markdown("<div class='company-section'>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2800/2800187.png", width=50) # Temsili Logo
    st.subheader("Kurumsal Bilgiler")
    st.text_input("Firma Adı", "Global Tech Solutions")
    st.text_input("Departman", "İnsan Kaynakları")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.info("📊 Mülakat Durumu: Aktif")
    st.session_state.ik_name = st.text_input("Görüşmeci", st.session_state.ik_name)
    st.session_state.aday_name = st.text_input("Aday İsmi", st.session_state.aday_name)
    
    st.divider()
    if st.button("🏠 Ana Dashboard", use_container_width=True):
        st.session_state.page = "setup"
        st.rerun()

# --- ANA AKIŞ ---
if st.session_state.page == "setup":
    st.title("Mülakat Başlatma Merkezi")
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    st.write("Mülakat tipini ve segment süresini belirleyerek canlı yayına geçebilirsiniz.")
    st.radio("Segment Süresi", ["30 sn", "1 dk", "2 dk"], horizontal=True)
    if st.button("🔴 CANLI MÜLAKATI BAŞLAT", type="primary", use_container_width=True):
        st.session_state.page = "live"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "live":
    # Ekranı 2 ana bölüme ayırıyoruz (Orta: Chat, Sağ: Raporlama)
    col_chat, col_report = st.columns([2, 1])

    # 🎙️ ORTA PANEL: CANLI TRANSKRİPT
    with col_chat:
        st.markdown(f"#### 🎙️ {st.session_state.ik_name} vs {st.session_state.aday_name}")
        components.html(f"""
            <div id="chat-container" style="background:#020617; height:500px; overflow-y:auto; padding:20px; display:flex; flex-direction:column; gap:15px; font-family:sans-serif;">
            </div>
            <script>
                const ik_name = "{st.session_state.ik_name}";
                const aday_name = "{st.session_state.aday_name}";
                const chatContainer = document.getElementById('chat-container');
                const Rec = window.webkitSpeechRecognition || window.Recognition;
                
                if(Rec) {{
                    const r = new Rec();
                    r.lang = 'tr-TR'; r.continuous = true; r.interimResults = true;
                    let lastText = "";

                    r.onresult = (event) => {{
                        for (let i = event.resultIndex; i < event.results.length; i++) {{
                            if (event.results[i].isFinal) {{
                                let text = event.results[i][0].transcript.trim();
                                if(text === lastText) return;
                                lastText = text;

                                let isIK = text.toLowerCase().includes('?') || text.toLowerCase().includes('neden') || text.toLowerCase().includes('hoş');
                                createBubble(text, isIK);
                            }}
                        }}
                    }};

                    function createBubble(text, isIK) {{
                        const row = document.createElement('div');
                        row.className = isIK ? 'ik-row' : 'aday-row';
                        row.style = "display:flex; width:100%; margin-bottom:10px; justify-content:" + (isIK ? 'flex-start' : 'flex-end');
                        
                        const bubble = document.createElement('div');
                        const color = isIK ? '#450a0a' : '#1e3a8a';
                        const label = isIK ? ik_name : aday_name;
                        const labelColor = isIK ? '#ef4444' : '#3b82f6';
                        const align = isIK ? 'left' : 'right';

                        bubble.style = `background:${{color}}; padding:12px; border-radius:12px; max-width:80%; text-align:${{align}}; color:white; border-${{isIK?'left':'right'}}:4px solid ${{labelColor}};`;
                        bubble.innerHTML = `<div style="color:${{labelColor}}; font-size:0.7rem; font-weight:bold; margin-bottom:4px;">${{label}}</div>` + text;
                        
                        row.appendChild(bubble);
                        chatContainer.appendChild(row);
                        chatContainer.scrollTop = chatContainer.scrollHeight;
                    }}
                    r.start();
                }}
            </script>
        """, height=530)

    # ➡️ SAĞ PANEL: YÖNETİCİ RAPORLAMA EKRANI
    with col_report:
        st.markdown("#### 📑 Yönetici Özet Raporu")
        
        with st.container():
            st.markdown('<div class="report-card">', unsafe_allow_html=True)
            st.write("**Anlık Yetkinlik Analizi**")
            
            # Dinamik Puanlama (Yöneticiler için)
            st.progress(75, text="Teknik Uyumluluk: %75")
            st.progress(60, text="Kültürel Adaptasyon: %60")
            st.progress(90, text="İletişim Becerisi: %90")
            
            st.divider()
            st.write("**Yönetici Notları**")
            st.text_area("Mülakat devam ederken not al...", height=100, label_visibility="collapsed")
            
            if st.button("PDF Raporu Oluştur", use_container_width=True):
                st.toast("Rapor hazırlanıyor...")
            
            st.divider()
            if st.button("🛑 MÜLAKATI BİTİR VE KAYDET", type="primary", use_container_width=True):
                st.session_state.page = "report"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# --- RAPOR SAYFASI ---
elif st.session_state.page == "report":
    st.balloons()
    st.header("🏁 Mülakat Değerlendirme Raporu")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="report-card"><h3>Aday Künyesi</h3><p>İsim: <b>'+st.session_state.aday_name+'</b></p><p>Pozisyon: Kıdemli Yazılım Geliştirici</p></div>', unsafe_allow_html=True)
    with col2:
        fig = go.Figure(go.Scatterpolar(r=[80, 70, 90, 85, 75], theta=['Teknik','Ekip','DISC','Metropolitan','EQ'], fill='toself'))
        st.plotly_chart(fig, use_container_width=True)
    st.button("Yeni Mülakat Başlat", on_click=lambda: st.session_state.update({"page":"setup"}))
