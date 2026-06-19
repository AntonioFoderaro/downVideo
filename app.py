import streamlit as st
import os
import subprocess

st.set_page_config(page_title="Downloader Assemblea", page_icon="🎬")
st.write("VERSIONE 10000")
st.title("Downloader Assemblea Nazionale")

PASSWORD = "Futuro2026"
pwd = st.text_input("Password:", type="password")

if pwd != PASSWORD:
    st.warning("Password errata.")
    st.stop()

st.success("Accesso consentito.")

URL_YT_SAB = "https://youtu.be/XRDS0ySvQNU"
URL_FB_SAB = "https://www.facebook.com/watch/?v=1676283610284508"
URL_RR_SAB = "https://www.radioradicale.it/scheda/792067/conferenza-stampa-di-roberto-vannacci-a-margine-della-prima-giornata-dellassemblea"
URL_YT_SAB1 = "https://www.youtube.com/watch?v=8pYxQ8Q2YpE"
URL_YT_SAB2 = "https://www.youtube.com/watch?v=1u8j8p2t0xA"
URL_RR_DOM = "https://www.radioradicale.it/scheda/791851/assemblea-costituente-di-futuro-nazionale-2a-giornata"

elenco = {
    "Sabato - Integrale YouTube": {"url": URL_YT_SAB, "start": None, "end": None},
    "Sabato - Conferenza Vannacci RR": {"url": URL_RR_SAB, "start": None, "end": None},
    "Sabato - Clip Facebook": {"url": URL_FB_SAB, "start": None, "end": None},
    "Sabato - Clip YouTube 1": {"url": URL_YT_SAB1, "start": None, "end": None},
    "Sabato - Clip YouTube 2": {"url": URL_YT_SAB2, "start": None, "end": None},
    "Domenica - Integrale RR": {"url": URL_RR_DOM, "start": None, "end": None},
    "Domenica - Vannacci": {"url": URL_RR_DOM, "start": "03:41:20", "end": "03:51:47"},
    "Domenica - Ravetto": {"url": URL_RR_DOM, "start": "03:31:50", "end": "03:41:10"},
    "Domenica - Sasso": {"url": URL_RR_DOM, "start": "03:31:50", "end": "03:41:10"},
    "Domenica - Arlecchino": {"url": URL_RR_DOM, "start": "03:22:10", "end": "03:31:40"},
    "Domenica - Simoni": {"url": URL_RR_DOM, "start": "00:01:10", "end": "00:26:40"},
    "Domenica - Gasperini": {"url": URL_RR_DOM, "start": "03:10:10", "end": "03:22:00"},
    "Domenica - Pozzolo": {"url": URL_RR_DOM, "start": "03:31:50", "end": "03:41:10"},
    "Domenica - Valdegamberi": {"url": URL_RR_DOM, "start": "03:31:50", "end": "03:41:10"}
}

def scarica(url, out, log):
    log.write("Esecuzione yt-dlp...")

    cmd = 'yt-dlp --user-agent "Mozilla/5.0"'

    if "facebook.com" in url:
        cmd += " --cookies-from-browser chrome"

    if "radioradicale.it" in url:
        cmd += " --allow-unplayable-formats"

    cmd = f'{cmd} "{url}" -o "{out}"'
    log.write(cmd)

    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

st.header("Interventi")
scelta = st.selectbox("Scegli:", list(elenco.keys()))
info = elenco[scelta]

st.header("Conversione")
mode = st.selectbox("Modalita:", ["CRF18", "CRF28", "CRF33", "720p", "480p", "360p", "MP3"])

if mode == "CRF18":
    ff = "-vcodec libx264 -crf 18 -acodec aac"
elif mode == "CRF28":
    ff = "-vcodec libx264 -crf 28 -acodec aac"
elif mode == "CRF33":
    ff = "-vcodec libx264 -crf 33 -acodec aac"
elif mode == "720p":
    ff = "-vf scale='trunc(oh*a/2)*2:720' -vcodec libx264 -crf 23 -acodec aac"
elif mode == "480p":
    ff = "-vf scale='trunc(oh*a/2)*2:480' -vcodec libx264 -crf 23 -acodec aac"
elif mode == "360p":
    ff = "-vf scale='trunc(oh*a/2)*2:360' -vcodec libx264 -crf 23 -acodec aac"
elif mode == "MP3":
    ff = "-vn -acodec libmp3lame -b:a 128k"

if st.button("Elabora"):
    log = st.empty()
    log.write("Preparazione...")

    raw = "raw.mp4"
    out = "finale.mp4"

    for f in [raw, out]:
        if os.path.exists(f):
            os.remove(f)

    r = scarica(info["url"], raw, log)

    if r.returncode != 0:
        st.error("Errore download. Possibile blocco firewall.")
        st.code(r.stderr)
        st.stop()

    if not os.path.exists(raw):
        st.error("File non scaricato. Probabile blocco firewall.")
        st.stop()

    log.write("Download completato.")

    t = ""
    if info["start"] and info["end"]:
        t = f'-ss {info["start"]} -to {info["end"]}'

    cmd = f'ffmpeg -y {t} -i "{raw}" {ff} "{out}"'
    log.write("Esecuzione ffmpeg:")
    log.write(cmd)

    conv = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if conv.returncode != 0:
        st.error("Errore conversione.")
        st.code(conv.stderr)
        st.stop()

    if not os.path.exists(out):
        st.error("File non generato.")
        st.stop()

    st.success("Pronto!")

    with open(out, "rb") as f:
        st.download_button("Scarica", f, file_name="video.mp4")
