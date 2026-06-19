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
URL_RR_CONFERENZA_VANNACCI = "https://www.radioradicale.it/scheda/792067/conferenza-stampa-di-roberto-vannacci-a-margine-della-prima-giornata-dellassemblea"

# Link aggiuntivi trovati automaticamente (YouTube correlati)
URL_YT_SABATO_CLIP1 = "https://www.youtube.com/watch?v=8pYxQ8Q2YpE"
URL_YT_SABATO_CLIP2 = "https://www.youtube.com/watch?v=1u8j8p2t0xA"

# --- 2ª GIORNATA (DOMENICA) ---
URL_RR_DOMENICA_INTEGRALE = "https://www.radioradicale.it/scheda/791851/assemblea-costituente-di-futuro-nazionale-2a-giornata"

# ==========================================
# MAPPATURA INTERVENTI COMPLETA
# ==========================================
elenco_completo = {

    # --- SABATO (1ª giornata) ---
    "SABATO – Registrazione Integrale (YouTube)": {
        "url": URL_YT_SABATO_INTEGRALE,
        "start": None,
        "end": None
    },

    "SABATO – Conferenza Stampa Roberto Vannacci (Radio Radicale)": {
        "url": URL_RR_CONFERENZA_VANNACCI,
        "start": None,
        "end": None
    },

    "SABATO – Clip Extra (Facebook Watch)": {
        "url": URL_FB_EXTRA_SABATO,
        "start": None,
        "end": None
    },

    "SABATO – Clip YouTube
