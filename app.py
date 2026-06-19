import streamlit as st
import os
import subprocess

st.set_page_config(page_title="Universal Video Downloader & Compressor", page_icon="🎬")
st.title("🎬 Downloader Assemblea Nazionale")

# ==========================================
# BLOCCO DI SICUREZZA CON PASSWORD
# ==========================================
PASSWORD_CORRETTA = "Futuro2026"

password_inserita = st.text_input("Inserisci la password di sicurezza per accedere al pannello:", type="password")

if password_inserita != PASSWORD_CORRETTA:
    st.warning("🔒 Accesso limitato. Inserisci la password corretta per sbloccare le funzioni di download.")
    st.stop()

# ==========================================
# APPLICAZIONE REALE
# ==========================================
st.success("🔓 Accesso consentito!")
st.write("Scarica, taglia e comprime qualsiasi intervento dell'Assemblea Costituente di Roma (13-14 Giugno).")

# ==========================================
# URL REALI (DA SOSTITUIRE)
# ==========================================
URL_RADIO_SABATO = "INSERISCI_URL_RADIO_RADICALE_SABATO"
URL_RADIO_DOMENICA = "INSERISCI_URL_RADIO_RADICALE_DOMENICA"

URL_YT_SABATO = "INSERISCI_URL_YOUTUBE_SABATO"
URL_YT_DOMENICA = "INSERISCI_URL_YOUTUBE_DOMENICA"

# ==========================================
# MAPPATURA COMPLETA INTERVENTI
# ==========================================
elenco_completo = {
    "SABATO - Registrazione Integrale": {
        "url": URL_RADIO_SABATO, "start": None, "end": None
    },
    "SABATO - Roberto Vannacci (Conferenza Stampa)": {
        "url": URL_YT_SABATO, "start": "00:26:50", "end": "01:12:15"
    },
    "DOMENICA - Registrazione Integrale": {
        "url": URL_RADIO_DOMENICA, "start": None, "end": None
    },
    "DOMENICA - Roberto Vannacci (Conclusioni)": {
        "url": URL_RADIO_DOMENICA, "start": "03:41:20", "end": "03:51:47"
    },
    # Aggiungi qui altri interventi se vuoi
}

# ==========================================
# SELEZIONE INTERVENTO
# ==========================================
scelta = st.selectbox("1. Scegli l'intervento:", list(elenco_completo.keys()))
video_info = elenco_completo[scelta]

# ==========================================
# CONTROLLO URL VALIDO
# ==========================================
if ("watch?v=" not in video_info["url"]) and ("scheda" not in video_info["url"]):
    st.error("❌ L'URL selezionato non è valido. Inserisci un link completo di Radio Radicale o YouTube.")
    st.stop()

# ==========================================
# COMPRESSIONE
# ==========================================
compression = st.radio(
    "2. Scegli il livello di compressione:",
    ('Bilanciata (Consigliata)', 'Massima (Super leggera)', 'Nessuna (Qualità originale)')
)

crf_val = 28
if compression == 'Massima (Super leggera)':
    crf_val = 33
elif compression == 'Nessuna (Qualità originale)':
    crf_val = 23

output_placeholder = st.empty()

# ==========================================
# ESECUZIONE
# ==========================================
if st.button("Elabora Video e Genera Download 🚀"):
    output_placeholder.warning("Download del video in corso...")

    raw_file = "raw_video.mp4"
    final_file = "output_finale.mp4"

    for f in [raw_file, final_file]:
        if os.path.exists(f):
            os.remove(f)

    # Download video
    cmd_dl = f'yt-dlp --user-agent "Mozilla/5.0" "{video_info["url"]}" -o "{raw_file}"'
    dl_res = subprocess.run(cmd_dl, shell=True)

    if dl_res.returncode != 0 or not os.path.exists(raw_file):
        output_placeholder.error("❌ Errore nel recupero del video. Controlla l'URL o riprova più tardi.")
        st.stop()

    output_placeholder.warning("Taglio e compressione in corso...")

    # Taglio
    time_args = ""
    if video_info["start"] and video_info["end"]:
        time_args = f'-ss {video_info["start"]} -to {video_info["end"]}'

    # FFmpeg
    cmd_ffmpeg = f'ffmpeg -y {time_args} -i "{raw_file}" -vcodec libx264 -crf {crf_val} -acodec aac -b:a 128k "{final_file}"'
    subprocess.run(cmd_ffmpeg, shell=True)

    if not os.path.exists(final_file):
        output_placeholder.error("❌ Errore durante la compressione.")
        st.stop()

    output_placeholder.success("✅ Video pronto!")

    nome_salvataggio = f"{scelta.replace(' ', '_').replace('-', '').replace('(', '').replace(')', '')}.mp4"

    with open(final_file, "rb") as file:
        st.download_button(
            label="⬇️ Scarica il Video",
            data=file,
            file_name=nome_salvataggio,
            mime="video/mp4"
        )

    # Pulizia finale
    for f in [raw_file, final_file]:
        if os.path.exists(f):
            try:
                os.remove(f)
            except:
                pass

