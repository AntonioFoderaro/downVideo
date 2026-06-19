import streamlit as st
import os
import subprocess
import time

st.set_page_config(page_title="Downloader Assemblea", page_icon="🎬")
st.write("Made by Antonio Foderaro")
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

def build_yt_dlp_cmd(url, out):
    cmd = [
        "yt-dlp",
        "--user-agent", "Mozilla/5.0",
        "--retry-sleep", "2",
        "--retries", "50",
        "--fragment-retries", "50",
        "--concurrent-fragments", "1",
        "--buffer-size", "1M",
        "--http-chunk-size", "1M",
        "-o", out,
        url
    ]

    if "facebook.com" in url:
        cmd += ["--cookies-from-browser", "chrome"]

    if "radioradicale.it" in url:
        cmd += ["--allow-unplayable-formats"]

    return cmd

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

    progress = st.progress(0)
    status = st.empty()

    raw = "raw.mp4"
    out = "finale.mp4"

    for f in [raw, out, raw + ".part"]:
        if os.path.exists(f):
            os.remove(f)

    # 0–10% Preparazione
    status.write("🔧 Preparazione...")
    progress.progress(10)
    time.sleep(0.3)

    # 10–70% Download con retry intelligente
    status.write("⬇️ Download in corso (con recupero frammenti)...")

    max_attempts = 5
    attempt = 0
    download_ok = False

    while attempt < max_attempts and not download_ok:
        attempt += 1

        status.write(f"⬇️ Download (tentativo {attempt}/{max_attempts})...")
        cmd = build_yt_dlp_cmd(info["url"], raw)

        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # barra fake durante il download
        for i in range(10 + (attempt - 1) * 10, 10 + attempt * 10):
            if i > 70:
                break
            progress.progress(i)
            time.sleep(0.5)
            if proc.poll() is not None:
                break

        # se ancora vivo dopo il ciclo, aspettiamo un po' e poi lo terminiamo
        if proc.poll() is None:
            time.sleep(5)
            proc.terminate()

        # controllo file
        if os.path.exists(raw):
            download_ok = True
        else:
            # se esiste .part, significa frammenti persi ma in corso → aspetta e riprova
            if os.path.exists(raw + ".part"):
                status.write("⏳ Radio Radicale sta perdendo frammenti, attendo e riprovo...")
                time.sleep(5)
            else:
                status.write("⚠️ Nessun file creato, possibile blocco firewall. Riprovo...")
                time.sleep(3)

    if not download_ok:
        progress.progress(100)
        status.error("❌ Impossibile completare il download dopo vari tentativi. Server o firewall troppo instabili.")
        st.stop()

    progress.progress(70)

    # 70–95% Conversione
    status.write("🎞️ Conversione in corso...")

    t = ""
    if info["start"] and info["end"]:
        t = f'-ss {info["start"]} -to {info["end"]}'

    cmd_ff = f'ffmpeg -y {t} -i "{raw}" {ff} "{out}"'
    conv = subprocess.Popen(cmd_ff, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for i in range(70, 95):
        progress.progress(i)
        time.sleep(0.4)
        if conv.poll() is not None:
            break

    if conv.poll() is None:
        conv.terminate()

    if not os.path.exists(out):
        progress.progress(100)
        status.error("❌ Errore conversione. File finale non creato.")
        st.stop()

    # 95–100% Finalizzazione
    status.write("📦 Preparazione download...")
    time.sleep(0.5)
    progress.progress(100)

    st.success("✅ Pronto!")

    with open(out, "rb") as f:
        st.download_button("Scarica", f, file_name="video.mp4")
