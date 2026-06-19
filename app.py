import streamlit as st
import os
import subprocess
import json

st.set_page_config(page_title="Downloader Assemblea", page_icon="🎬")
st.title("Downloader Assemblea Nazionale")

PASSWORD = "Futuro2026"
pwd = st.text_input("Password:", type="password")

if pwd != PASSWORD:
    st.warning("Password errata.")
    st.stop()

st.success("Accesso consentito.")

# URL
URL_YT_SAB = "https://youtu.be/XRDS0ySvQNU"
URL_FB_SAB = "https://www.facebook.com/watch/?v=1676283610284508"
URL_RR_SAB = "https://www.radioradicale.it/scheda/792067/conferenza-stampa-di-roberto-vannacci-a-margine-della-prima-giornata-dellassemblea"
URL_YT_SAB1 = "https://www.youtube.com/watch?v=8pYxQ8Q2YpE"
URL_YT_SAB2 = "https://www.youtube.com/watch?v=1u8j8p2t0xA"
URL_RR_DOM = "https://www.radioradicale.it/scheda/791851/assemblea-costituente-di-futuro-nazionale-2a-giornata"

# Dizionario interventi
elenco = {
    "Sabato - Integrale YouTube": {
        "url": URL_YT_SAB, "start": None, "end": None
    },
    "Sabato - Conferenza Vannacci RR": {
        "url": URL_RR_SAB, "start": None, "end": None
    },
    "Sabato - Clip Facebook": {
        "url": URL_FB_SAB, "start": None, "end": None
    },
    "Sab
