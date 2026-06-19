import streamlit as st
import os
import subprocess
import json

st.set_page_config(page_title="Downloader Assemblea Nazionale", page_icon="🎬")
st.title("🎬 Downloader Assemblea Nazionale – Futuro Nazionale")

# ==========================================
# BLOCCO DI SICUREZZA
# ==========================================
PASSWORD_CORRETTA = "Futuro2026"

password_inserita = st.text_input("Inserisci la password per accedere:", type="password")

if password_inserita != PASSWORD_CORRETTA:
    st.warning("🔒 Accesso limitato. Inserisci la password corretta.")
    st.stop()

st.success("🔓 Accesso consentito!")
st.write("Scarica, taglia, comprimi o cerca automaticamente i video dell'Assemblea Costituente di Roma (13–14 Giugno).")

# ==========================================
# URL REALI (YouTube, Radio Radicale, Facebook)
# ==========================================

# --- 1ª GIORNATA (SABATO) ---
URL_YT_SABATO_INTEGRALE = "https://youtu.be/XRDS0ySvQNU"
URL_FB_EXTRA_SABATO = "https://www.facebook.com/watch/?v=1676283610284508"
URL_RR_CONFERENZA_V
