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

URL_YT_SABATO_INTEGRALE = "https://youtu.be/XRDS0ySvQNU"
URL_FB_EXTRA_SABATO = "https://www.facebook.com/watch/?v=1676283610284508"
URL_RR_CONFERENZA_VANNACCI = "https://www.radioradicale.it/scheda/792067/conferenza-stampa-di-roberto-vannacci-a-margine-della-prima-giornata-dellassemblea"

URL_YT_SABATO_CLIP1 = "https://www.youtube.com/watch?v=8pYxQ8Q2YpE"
URL_YT_SABATO_CLIP2 = "https://www.youtube.com/watch?v=1u8j8p2t0xA"

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
    "SABATO – Clip YouTube #1 (Correlata)": {
        "url": URL_YT_SABATO_CLIP1,
        "start": None,
        "end": None
    },
    "SABATO – Clip YouTube #2 (Correlata)": {
        "url": URL_YT_SABATO_CLIP2,
        "start": None,
        "end": None
    },

    # --- DOMENICA (2ª giornata) ---
    "DOMENICA – Registrazione Integrale (Radio Radicale)": {
        "url": URL_RR_DOMENICA_INTEGRALE,
        "start": None,
        "end": None
    },
    "DOMENICA – Roberto Vannacci (Conclusioni)": {
        "url": URL_RR_DOMENICA_INTEGRALE,
        "start": "03:41:20",
        "end": "03:51:47"
    },
    "DOMENICA – Laura Ravetto": {
        "url": URL_RR_DOMENICA_INTEGRALE,
        "start": "03:31:50",
        "end": "03:41:10"
    },
    "DOMENICA – Rossano Sasso": {
        "url": URL_RR_DOMENICA_INTEGRALE,
        "start": "03:31:50",
        "end": "03:41:10"
    },
    "DOMENICA – Massimo Arlecchino": {
        "url": URL_RR_DOMENICA_INTEGRALE,
        "start": "03:22:10",
        "end": "03:31:40"
    },
    "DOMENICA – Massimiliano Simoni": {
        "url": URL_RR_DOMENICA_INTEGRALE,
        "start": "00:01:10",
        "end": "00:26:40"
    },
    "DOMENICA – Lorenzo Gasperini": {
        "url": URL_RR_DOMENICA_INTEGRALE,
        "start": "03:10:10",
        "end": "03:22:00"
    },
    "DOMENICA – Emanuele Pozzolo": {
        "url": URL_RR_DOMENICA_INTEGRALE,
        "start": "03:31:50",
        "end": "03:41:10"
    },
    "DOMENICA – Stefano Valdegamberi": {
        "url": URL_RR_DOMENICA_INTEGRALE,
        "start": "03:31:50",
        "end": "03:41:10"
    }
}

# ==========================================
# SEZIONE 1 — DOWNLOAD DAGLI INTERVENTI UFFICIALI
# ==========================================
st.header("📌 Interventi ufficiali")

scelta = st.selectbox("Scegli l'intervento:", list(elenco_completo.keys()))
video_info = elenco_completo[scelta]

# ==========================================
# SEZIONE 2 — RICERCA AUTOMATICA
# ==========================================
st.header("🔎 Ricerca automatica video")

query = st.text_input("Cerca un video (nome, titolo, oratore, link YouTube/Facebook/Radio Radicale):")

if st.button("Cerca video"):
    st.info("Ricerca in corso…")

    cmd_search = f'yt-dlp "ytsearch5:{query}" --dump-json'
    result = subprocess.run(cmd_search, shell=True, capture_output=True, text=True)

    risultati = []
    for line in result.stdout.splitlines():
        try:
            risultati.append(json.loads(line))
        except:
            pass

    if risultati:
        st.success("Risultati trovati:")
        for r in risultati:
            st.write(f"🎥 **{r.get('title','(senza titolo)')}**")
            st.write(r.get("webpage_url"))
            st.write("---")
    else:
        st.error("Nessun risultato trovato.")

# ==========================================
# MODALITÀ DI CONVERSIONE
# ==========================================
st.header("🎚️ Modalità di conversione")

conversione = st.selectbox(
    "Scegli la modalità:",
    [
        "Qualità massima (CRF 18)",
        "Qualità bilanciata (CRF 28)",
        "Qualità leggera (CRF 33)",
        "Converti a 720p",
        "Converti a 480p",
        "Converti a 360p",
        "Solo audio MP3"
    ]
)

# Parametri conversione
if conversione == "Qualità massima (CRF 18)":
    ffmpeg_params = "-vcodec libx264 -crf 18 -acodec aac -b:a 192k"
elif conversione == "Qualità bilanciata (CRF 28)":
    ffmpeg_params = "-vcodec libx264 -crf 28 -acodec aac -b:a 128k"
elif conversione == "Qualità leggera (CRF 33)":
    ffmpeg_params = "-vcodec libx264 -crf 33 -acodec aac -b:a 96k"
elif conversione == "Converti a 720p":
    ffmpeg_params = "-vf scale=-1:720 -vcodec libx264 -crf 23 -acodec aac -b:a 128k"
elif conversione == "Converti a 480p":
    ffmpeg_params = "-vf scale=-1:480 -vcodec libx264 -crf 23 -acodec aac -b:a 128k"
elif conversione == "Converti a 360p":
    ffmpeg_params = "-vf scale=-1:360 -vcodec libx264 -crf 23 -acodec aac -b:a 96k"
elif conversione == "Solo audio MP3":
    ffmpeg_params = "-vn -acodec libmp3lame -b:a 128k"

# ==========================================
# ESECUZIONE
# ==========================================
if st.button("Elabora Video 🚀"):
    st.warning("Download in corso...")

    raw_file = "raw_video.mp4"
    final_file = "output_finale.mp4"

    # Pulizia
    for f in [raw_file, final_file]:
        if os.path.exists(f):
            os.remove(f)

    # Download video
    cmd_dl = f'yt-dlp --user-agent "Mozilla/5.0" "{video_info["url"]}" -o "{raw_file}"'
    dl_res = subprocess.run(cmd_dl, shell=True)

    if dl_res.returncode != 0 or not os.path.exists(raw_file):
        st.error("❌ Errore nel download.")
        st.stop()

    st.warning("Conversione in corso
