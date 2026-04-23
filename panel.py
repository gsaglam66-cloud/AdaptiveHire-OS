import streamlit as st
import os
import time

# --- 1. GÜVENLİK & API YAPILANDIRMASI ---
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    st.warning("Lütfen Secrets alanına 'OPENAI_API_KEY' anahtarını ekleyin.")
    st.stop()

# --- 2. SAYFA AYARLARI & ÖZEL TASARIM ---
st.set_page_config(page_title="Adaptive Hire OS", page_icon="🎯", layout="wide")

# 11px font, modern buton tasarımları ve canlı akış arayüzü
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 11px !important; background-color: #F8FAFC; }
    .main-header { font-size: 22px !important; font-weight: 800; color: #1E293B; border-bottom: 3px solid #3B82F6; padding-bottom: 12px; margin-bottom: 25px; }
    .transcript-box { background-color: #0F172A; color: #10B981; border: 1px solid #1E293B; padding: 15px; height: 300px; overflow-y: auto; font-family: 'Fira Code', monospace; border-radius: 10px; line-height: 1.6; }
    .ai-card { background-color: #FFFFFF; border-left: 6px solid #6366F1; padding: 18px; border-radius: 10px; shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }
    .stButton>button { font-size: 11px !important; border-radius: 8px; transition: all 0.3s; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    /* Segment butonları için özel hizalama */
    div[data-testid="stHorizontalBlock"] > div { display: flex; align-items: center; justify-content: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: KURUMSAL YÖNETİM ---
with st.sidebar:
    st.image("https://via.placeholder.com/250x80?text=ADAPTIVE+HIRE+OS", use_container_width=True)
    st.markdown("### 🏢 KURUMSAL DATA ALANI")
    
    with st.expander("📁 HİYERARŞİ YÖNETİMİ", expanded=True):
        st.text_input("KLASÖR", value="2026 Üst Düzey Yönetim")
        st.text_input("FİRMA", value="Karaaslan Grup")
        st.text_input("BİRİM", value="Teknoloji Merkezi")
        st.button("YAPIYI GÜNCELLE")

    st.divider()
    st.markdown("### 🤖 ASİSTAN MODU")
    st.radio("Analiz Derinliği", ["Standart", "Derin Analiz", "Yetenek Puanlama"])
    st.info(f"Yetkili: gazisaglam1@gmail.com")

# --- 4. ANA PANEL: CANLI MÜLAKAT VE SEGMENT KONTROLÜ ---
st.markdown('<p class="main-header">ADAPTIVE HIRE: TALENT INTELLIGENCE OS</p>', unsafe_allow_html=True)

col_live, col_ai = st.columns([1.8, 1.2])

with col_live:
    st.subheader("🎙️ Canlı Mülakat ve Transkript Yönetimi")
    
    # Aday Bilgileri
    with st.container(border=True):
        c1, c2 = st.columns(2)
        candidate = c1.text_input("ADAY ADI SOYADI", value="Ahmet Anıl")
        position = c2.text_input("BAŞVURULAN POZİSYON", value="AI Geliştirme Lideri")
        
        # 3. Madde: Ses Kayıt Tuşu
        st.markdown("---")
        start_rec = st.button("🎤 SES KAYDINI BAŞLAT VE ANALİZE HAZIRLAN", type="primary", use_container_width=True)
        
        # 2. Madde: Yan Yana Segment Butonları
        st.markdown("**ANALİZ SEGMENT SÜRESİ SEÇİN:**")
        seg_cols = st.columns(6)
        times = ["15s", "30s", "60s", "2dk", "5dk", "10dk"]
        selected_seg = ""
        
        # Her sütun için bir buton oluşturma
        for idx, t in enumerate(times):
            if seg_cols[idx].button(t, use_container_width=True):
                st.session_state['current_seg'] = t
                st.toast(f"Analiz süresi {t} olarak güncellendi!")

        # 4. Madde: Bağımsız Gönder Tuşu (Ok simgesi niyetine)
        manual_send = st.button("➡️ ŞİMDİ ANALİZ ET (ZAMAN SINIRI OLMADAN GÖNDER)", use_container_width=True)

    # Transkript Alanı
    st.markdown(f"**Anlık Transkript Akışı** (Segment: {st.session_state.get('current_seg', '15s')})")
    trans_placeholder = st.empty()
    
    if start_rec:
        st.error("🔴 CANLI KAYIT VE YAPAY ZEKA DİNLEMESİ AKTİF")
        # Simülasyon
        sim_text = ">> [00:01] Sistem: Mikrofon erişimi sağlandı.\n"
        sim_text += f">> [00:05] Aday: Merhaba, ben {candidate}. Adaptive Hire projesindeki vizyonunuzu çok değerli buluyorum.\n"
        sim_text += ">> [00:12] Aday: Özellikle büyük dil modellerinin İK süreçlerine adaptasyonu üzerine uzmanlaştım.\n"
        trans_placeholder.markdown(f'<div class="transcript-box">{sim_text}</div>', unsafe_allow_html=True)

with col_ai:
    st.subheader("🤖 AI Zeka Paneli")
    
    if start_rec or manual_send:
        with st.container():
            st.markdown(f"""
            <div class="ai-card">
                <b>🔍 ANLIK ANALİZ RAPORU</b><br>
                <b>Segment:</b> {st.session_state.get('current_seg', 'Manuel')}<br>
                <b>Özet:</b> Adayın sektörel vizyonu ve adaptasyon yeteneği yüksek. 
                Özellikle 'LLM' ve 'Adaptasyon' kelimeleri üzerinden teknik derinlik sergiliyor.
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("**💡 AI ÖNERİLEN SORULAR (STRATEJİK):**")
            st.success("1. LLM mimarilerini kurumsal veri güvenliğiyle nasıl entegre ediyorsunuz?")
            st.success("2. Karşılaştığınız en büyük teknik engelde 'adaptif' çözümünüz ne oldu?")
            
            st.markdown("**📊 YETENEK SKORLARI**")
            st.progress(0.88, text="Teknik Derinlik: %88")
            st.progress(0.75, text="Stratejik Düşünme: %75")
            
            if st.button("💾 ANALİZİ KLASÖRE ARŞİVLE"):
                st.success(f"{candidate} verileri 'Karaaslan Grup' klasörüne kaydedildi.")
    else:
        st.info("Mülakat başladığında AI analizleri ve soru önerileri burada belirecektir.")

# --- 5. FOOTER ---
st.divider()
st.markdown("<div style='text-align: center; color: gray;'>Adaptive Hire OS v3.0 | Gazi SAĞLAM - Talent Intelligence OS</div>", unsafe_allow_html=True)
