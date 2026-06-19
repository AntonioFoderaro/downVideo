import streamlit as st
import os
import subprocess
import requests
import time
import hashlib
from urllib.parse import urlparse

st.set_page_config(page_title="Downloader Assemblea", page_icon="🎬")
st.title("Downloader Assemblea – Versione 18000")

PASSWORD = "Futuro2026"
pwd = st.text_input("Password:", type="password")
if pwd != PASSWORD:
    st.stop()

st.success("Accesso consentito.")

# -----------------------------
# 1) Estrae playlist via yt-dlp
# -----------------------------
def estrai_playlist(url):
    cmd = ["yt-dlp", "-J", url]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _ = proc.communicate()
    import json
    data = json.loads(out)

    # HLS
    for f in data.get("formats", []):
        if f.get("protocol") == "m3u8_native" or ".m3u8" in f.get("url", ""):
            return "HLS", f["url"]

    # DASH
    for f in data.get("formats", []):
        if f.get("protocol") == "http_dash_segments" or ".mpd" in f.get("url", ""):
            return "DASH", f["url"]

    return None, None

# -----------------------------
# 2) Scarica frammenti in append
# -----------------------------
def scarica_in_append(url_playlist, tipo, output_file, progress, status):
    # crea file se non esiste
    if not os.path.exists(output_file):
        open(output_file, "wb").close()

    # hash per identificare la sessione
    h = hashlib.md5(url_playlist.encode()).hexdigest()
    idx_file = f"{h}.index"

    # riprende indice
    if os.path.exists(idx_file):
        with open(idx_file, "r") as f:
            start_index = int(f.read().strip())
    else:
        start_index = 0

    status.write("🔍 Recupero lista frammenti...")

    # scarica playlist
    r = requests.get(url_playlist)
    lines = r.text.splitlines()

    # estrai frammenti
    segments = [l for l in lines if l.endswith(".ts") or l.endswith(".m4s")]

    total = len(segments)
    if total == 0:
        status.write("❌ Nessun frammento trovato.")
        return False

    status.write(f"📦 Trovati {total} frammenti.")

    # download frammenti
    for i in range(start_index, total):
        seg = segments[i]
        seg_url = seg if seg.startswith("http") else url_playlist.rsplit("/", 1)[0] + "/" + seg

        ok = False
        tentativi = 0

        while not ok and tentativi < 50:
            tentativi += 1
            try:
                r = requests.get(seg_url, timeout=10)
                if r.status_code == 200 and len(r.content) > 0:
                    with open(output_file, "ab") as f:
                        f.write(r.content)
                    ok = True
                else:
                    time.sleep(1)
            except:
                time.sleep(1)

        if not ok:
            status.write(f"❌ Impossibile scaricare frammento {i}.")
            return False

        # salva indice
        with open(idx_file, "w") as f:
            f.write(str(i + 1))

        progress.progress(int((i + 1) / total * 80))

    return True

# -----------------------------
# 3) Conversione finale
# -----------------------------
def converti(input_file, output_file, ff):
    cmd = f'ffmpeg -y -i "{input_file}" {ff} "{output_file}"'
    subprocess.call(cmd, shell=True)

# -----------------------------
# UI
# -----------------------------
url = st.text_input("URL video:")
mode = st.selectbox("Qualità:", ["CRF18", "CRF28", "CRF33", "720p", "480p", "360p", "MP3"])

if st.button("Scarica"):

    progress = st.progress(0)
    status = st.empty()

    raw = "stream.ts"
    final = "video.mp4"

    # reset
    for f in [raw, final]:
        if os.path.exists(f):
            os.remove(f)

    status.write("🔍 Analisi URL...")
    tipo, playlist = estrai_playlist(url)
    if not playlist:
        status.write("❌ Impossibile estrarre playlist.")
        st.stop()

    progress.progress(10)

    status.write("⬇️ Download frammenti (flusso unico + ripresa)...")
    ok = scarica_in_append(playlist, tipo, raw, progress, status)

    if not ok:
        status.write("❌ Errore durante il download.")
        st.stop()

    progress.progress(90)

    # parametri ffmpeg
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

    status.write("🎞️ Conversione finale...")
    converti(raw, final, ff)

    progress.progress(100)
    status.write("✅ Pronto!")

    with open(final, "rb") as f:
        st.download_button("Scarica il video", f, file_name="video.mp4")
