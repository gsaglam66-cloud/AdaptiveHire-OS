import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import streamlit.components.v1 as components
import random

# --- AI CONFIG ---
API_KEY = "AIzaSyAv-jTe5J2Bogn4C1EZoVILclEAvReaDcY" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="AdaptiveHire | Enterprise", layout="wide", initial_sidebar_state="expanded")

# --- LIGHT & MINIMALIST CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600&display=swap');
    
    /* Genel Arka Plan ve Font */
    html, body, [class*="st-"] { 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
        background-color: #f8fafc; 
        color: #334155;
        font-size: 11px !important; /* Tüm metinler 11px */
    }

    /* Başlıklar İstisna (Daha belirgin) */
    h1, h2, h3, h4 { color: #1e293b !important; font-weight: 600 !important; }
    h4 { font-size: 14px !important; margin-bottom: 10px !important; }

    /* Kurumsal Kart Yapısı */
    .corporate-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* Transkript Alanı */
    #chat-scroll {
        height: 500px; overflow-y: auto; padding: 15px;
        background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px;
        display: flex; flex-direction: column; gap: 10px;
    }

    /* Mesaj Balonları (Sadeleştirilmiş) */
    .ik-bubble { 
        background: #fef2f2; color: #991b1b; 
        padding: 10px; border-radius: 0 10px 10px 10px;
        max-width: 85%; align-self: flex-start; border: 1px solid #fee2e2;
        font-size: 11px !important;
    }
    .aday-bubble { 
        background: #eff6ff; color: #1e40af; 
        padding: 10px; border-radius: 10px 0 10px 10px;
        max-width: 85%; align-self: flex-end; border: 1px solid #dbeafe;
        font-size: 11px !important; text-align: left;
    }

    /* Küçük Bilgi Etiketleri */
    .meta-label { font-size: 9px; font-weight: bold; text-transform: uppercase; margin-bottom: 3px; display: block; opacity: 0.7; }

    /* Sidebar Düzenleme */
    .stSidebar { background-color: #ffffff !important; border-right: 1px solid #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = "setup"
if 'ik_name' not in st.session_state: st.session_state.ik_name = "İK Uzmanı"
if 'aday_name' not in st.session_state: st.session_state.aday_name = "Aday
