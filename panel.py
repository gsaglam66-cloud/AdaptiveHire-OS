import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components

# --- AI AYARI ---
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="AdaptiveHire - Control Panel", layout="wide")

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "live"

# --- CANLI MÜLAKAT EKRANI ---
if st.session_state.page == "live":
    col_main, col_ctrl = st.columns([2.2, 1])
    
    with col_main:
        st.markdown("### 🎙️ Görüşme Akışı")
        # Transkript alanı
        st.markdown('<div style="background:white; border:1px solid #eee; padding:20px; border-radius:12px; height:450px;">', unsafe_allow_html=True)
        components.html("""
            <div id="trans" style="font-family:sans-serif; color:#334155;">Ses bekleniyor...</div>
            <script>
                const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if(Recognition){
                    const r = new Recognition(); r.lang='tr-TR'; r.continuous=true; r.interimResults=true;
                    r.onresult = (e) => {
                        let t = ''; for(let i=0; i<e.results.length; i++) t += e.results[i][0].transcript + ' ';
                        document.getElementById('trans').innerHTML = '<b>Aday:</b> ' + t;
                    };
                    r.start();
                }
            </script>
        """, height=400)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_ctrl:
        st.markdown("### 🎛️ Kontrol Paneli")
        
        # GÖRSEL 4'TEKİ DİNAMİK PROMPTLAR (Hatasız Döngü)
        with st.expander("📝 Dinamik Promptlar", expanded=True):
            p_cols = st.columns(2)
            prompts = [
                "Rapor 5a: Profil", "Rapor 5b: Riskler", 
                "Rapor 5c: Teknik", "Rapor 5d: Soft Skills", 
                "Rapor 5e: Psikososyal", "Rapor 5f: Özet"
            ]
            
            for i, p in enumerate(prompts):
                # Hataya neden olan kısım burada düzeltildi:
                p_cols[i % 2].button(p, key=f"btn_{i}", use_container_width=True)
        
        st.divider()
        if st.button("🛑 Görüşmeyi Bitir", use_container_width=True, type="primary"):
            st.success("Mülakat tamamlandı, rapor oluşturuluyor...")
