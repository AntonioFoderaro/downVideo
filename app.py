import streamlit as st
import os
import subprocess
import json

st.set_page_config(page_title="Downloader Assemblea Nazionale", page_icon="🎬")
st.title("Downloader Assemblea Nazionale - Futuro Nazionale")

PASSWORD_CORRETTA = "Futuro2026"
password_inserita = st.text_input("Inserisci la password per accedere:", type="password")

if password_inserita != PASSWORD_CORRETTA:
    st.warning("Accesso limitato. Inserisci la password corretta.")
    st.stop()

st.success("Accesso consentito!")
st.write("Scarica, taglia, comprimi o cerca automaticamente i video dell'Assemblea Costituente di Roma (13-14 Giugno).")

URL_YT_SABATO_INTEGRALE = "https://youtu.be/XRDS0ySvQNU"
URL_FB_EXTRA_SABATO = "https://www.facebook.com/watch/?v=1676283610284508"
URL_RR_CONFERENZA_VANNACCI = "https://www.radioradicale.it/scheda/792067/conferenza-stampa-di-roberto-vannacci-a-margine-della-prima-giornata-dellassemblea"
URL_YT_SABATO_CLIP1 = "https://www.youtube.com/watch?v=8pYxQ8Q2YpE"
URL_YT_SABATO_CLIP2 = "https://www.youtube.com/watch?v=1u8j8p2t0xA"
URL_RR_DOMENICA_INTEGRALE = "https://www.radioradicale.it/scheda/791851/assemblea-costituente-di-futuro-nazionale-2a-giornata"

elenco_completo = {
    "SABATO - Registrazione Integrale (YouTube)": {
        "url": URL_YT_SABATO_INTEGRALE, "start": None, "end": None
    },
    "SABATO - Conferenza Stampa Roberto Vannacci (Radio Radicale)": {
        "url": URL_RR_CONFERENZA_VANNACCI, "start": None, "end": None
    },
    "SABATO - Clip Extra (Facebook Watch)": {
        "url": URL_FB_EXTRA_SABATO, "start": None, "end": None
    },
    "SABATO - Clip YouTube 1": {
        "url": URL_YT_SABATO_CLIP1, "start": None, "end": None
    },
    "SABATO - Clip YouTube 2": {
        "url": URL_YT_SABATO_CLIP2, "start": None, "end": None
    },
    "DOMENICA - Registrazione Integrale (Radio Radicale)": {
        "url": URL_RR_DOMENICA_INTEGRALE, "start": None, "end": None
    },
    "DOMENICA - Roberto Vannacci (Conclusioni)": {
        "url": URL_RR_DOMENICA_INTEGRALE, "start": "03:41:20", "end": "03:51:47"
    },
    "DOMENICA - Laura Ravetto": {
        "url": URL_RR_DOMENICA_INTEGRALE, "start": "03:31:50", "end": "03:41:10"
    },
    "DOMENICA - Rossano Sasso": {
        "url": URL_RR_DOMENICA_INTEGRALE, "start": "03:31:50", "end": "03:41:10"
    },
    "DOMENICA - Massimo Arlecchino": {
        "url": URL_RR_DOMENICA_INTEGRALE, "start": "03:22:10", "end": "03:31:40"
    },
    "DOMENICA - Massimiliano Simoni": {
        "url": URL_RR_DOMENICA_INTEGRALE, "start": "00:01:10", "end": "00:26:40"
    },
    "DOMENICA - Lorenzo Gasperini": {
        "url": URL_RR_DOMENICA_INTEGRALE, "start": "03:10:10", "end": "03:22:00"
    },
    "DOMENICA - Emanuele Pozzolo": {
        "url": URL_RR_DOMENICA_INTEGRALE, "start": "03:31:50", "end": "03:41:10"
    },
    "DOMENICA - Stefano Valdegamberi": {
        "url": URL_RR_DOMENICA_INTEGRALE, "start": "03:31:50", "end": "03:41:10"
    }
}

def scarica_video(url, output):
    if "facebook.com" in url:
        cmd = f'yt-dlp --cookies-from-browser chrome --user-agent "Mozilla/5.0" "{url}" -o "{output}"'
    elif "radioradicale.it" in url:
        cmd = f'yt-dlp --allow-unplayable-formats --user-agent "Mozilla/5.0" "{url}" -o "{output}"'
    else:
        cmd = f'yt-dlp --user-agent "Mozilla/5.0" "{url}" -o "{output}"'
    return subprocess.run(cmd, shell=True)

st.header("Interventi ufficiali")
scelta = st.selectbox("Scegli l'intervento:", list(elenco_completo.keys()))
video_info = elenco_completo[scelta]

st.header("Ricerca automatica video")
query = st.text_input("Cerca un video:")

if st.button("Cerca video"):
    st.info("Ricerca in corso...")
    cmd_search = f'yt-dlp "ytsearch5:{query}" --dump-json'
    result = subprocess.run(cmd_search, shell
