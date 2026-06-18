import streamlit as st
import os
import subprocess
import uuid

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Universal Video Downloader", page_icon="🎬", layout="wide")
st.title("🎬 Downloader Integrale Assemblea Nazionale")

# ==========================================
# BLOCCO DI SICUREZZA CON PASSWORD
# ==========================================
PASSWORD_CORRETTA = "Futuro2026"
password_inserita = st.text_input("Inserisci la password di sicurezza per accedere al pannello:", type="password")

if password_inserita != PASSWORD_CORRETTA:
    st.warning("🔒 Accesso limitato. Inserisci la password corretta per sbloccare le funzioni di download.")
    st.stop()

# ==========================================
# APPLICAZIONE (ACCESSIBILE DOPO LOGIN)
# ==========================================
st.success("🔓 Accesso consentito!")
st.write("Seleziona l'oratore e decidi la risoluzione del video prima di avviare il download.")

# L'unico URL reale e supportato da yt-dlp per l'evento di Radio Radicale
URL_UFFICIALE = "https://radioradicale.it"
URL_YOUTUBE_VANNACCI = "https://youtube.com"

# Mappatura reale: ogni oratore punta alla sorgente corretta con il suo blocco temporale nativo completo
elenco_completo = {
    "SESSIONE COMPLETA - Sabato 13 Giugno (Registrazione Integrale)": {"url": URL_UFFICIALE, "start": None, "end": None},
    
    # --- ORATORI ED INTERVENTI SABATO 13 GIUGNO ---
    "SABATO - Massimiliano Simoni (Relazione d'apertura completa)": {"url": URL_UFFICIALE, "start": "00:02:00", "end": "00:28:00"}, 
    "SABATO - Roberto Vannacci (Conferenza Stampa ed Apertura dei Lavori)": {"url": URL_YOUTUBE_VANNACCI, "start": None, "end": None},
    "SABATO - Gianni Alemanno (Intervento integrale Movimento Indipendenza)": {"url": URL_UFFICIALE, "start": "01:16:00", "end": "01:45:00"},
    "SABATO - Nicola Procaccini (Discorso integrale ospite FDI)": {"url": URL_UFFICIALE, "start": "01:46:15", "end": "02:10:00"},
    "SABATO - Chicco Costini (Intervento e dibattito territoriale completo)": {"url": URL_UFFICIALE, "start": "02:11:00", "end": "02:35:00"},
    "SABATO - Federica Guaiardo (Intervento delegazione Catania completo)": {"url": URL_UFFICIALE, "start": "02:36:00", "end": "02:55:00"},
    "SABATO - Spazio Integrale Dibattiti Liberi (Tutti i Delegati del Pomeriggio)": {"url": URL_UFFICIALE, "start": "03:00:00", "end": "09:00:00"}, # Esteso fino alla fine dei lavori
    
    # --- ORATORI ED INTERVENTI DOMENICA 14 GIUGNO ---
    "DOMENICA - Roberto Vannacci (Discorso Politico Conclusivo del Presidente)": {"url": URL_YOUTUBE_VANNACCI, "start": None, "end": None},
    "DOMENICA - Lorenzo Gasperini (Presentazione Programma e Mozione Nazionale)": {"url": URL_UFFICIALE, "start": "09:01:00", "end": "09:40:00"},
    "DOMENICA - Massimo Arlecchino (Relazione Presidenza Nazionale)": {"url": URL_UFFICIALE, "start": "09:41:15", "end": "10:10:00"},
    "DOMENICA - Laura Ravetto (Saluti Istituzionali completi)": {"url": URL_UFFICIALE, "start": "10:11:00", "end": "10:35:00"},
    "DOMENICA - Rossano Sasso (Intervento integrale Scuola e Cultura)": {"url": URL_UFFICIALE, "start": "10:36:00", "end": "11:00:00"},
    "DOMENICA - Emanuele Pozzolo (Intervento Politico completo)": {"url": URL_UFFICIALE, "start": "11:01:10", "end": "11:25:00"},
    "DOMENICA - Stefano Valdegamberi (Discorso Autonomie e Territorio Veneto)": {"url": URL_UFFICIALE, "start": "11:26:00", "end": "11:50:00"},
    "DOMENICA - Sessione Integrale Approvazione Statuto e Votazione Organi": {"url": URL_UFFICIALE, "start": "11:51:00", "end": "12:30:00"},
}

# 1. Interfaccia di Selezione del video
scelta = st.selectbox("1. Seleziona l'oratore o la sessione:", list(elenco_completo.keys()))
video_info = elenco_completo[scelta]

# 2. Interfaccia di Selezione della Qualità
qualita_scelta = st.selectbox(
    "2. Seleziona la qualità del video:",
    [
        "Massima Qualità Disponibile (Risoluzione originale del sito sorgente)",
        "Alta Qualità (Fino a 1080p)",
        "Qualità Standard (Fino a 720p)",
        "Qualità Bassa (Fino a 480p)",
        "Qualità Minima (Fino a 360p)"
    ]
)

# Configurazione filtri altezza per yt-dlp
if "Massima" in qualita_scelta:
    format_arg = "-f bestvideo+bestaudio/best"
elif "1080p" in qualita_scelta:
    format_arg = '-f "bestvideo[height<=1080]+bestaudio/best[height<=1080]"'
elif "720p" in qualita_scelta:
    format_arg = '-f "bestvideo[height<=720]+bestaudio/best[height<=720]"'
elif "480p" in qualita_scelta:
    format_arg = '-f "bestvideo[height<=480]+bestaudio/best[height<=480]"'
else:
    format_arg = '-f "bestvideo[height<=360]+bestaudio/best[height<=360]"'

output_placeholder = st.empty()

# 3. Pulsante per avviare il Download
if st.button("Scarica e Genera File Video 🚀"):
    output_placeholder.warning("Connessione ai server e download del video in corso... Attendi.")
    
    session_id = str(uuid.uuid4())[:8]
    final_file = f"video_{session_id}.mp4"
    
    # Gestione efficiente del download nativo parziale tramite yt-dlp e ffmpeg interni
    download_options = f'{format_arg} --merge-output-format mp4 --no-playlist --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"'
    
    # Se l'oratore richiede una frazione di tempo specifica, diciamo a yt-dlp di scaricare solo quel pezzo tramite gli argomenti esterni di ffmpeg
    if video_info["start"] and video_info["end"]:
        # Questo flag dice alla sorgente di inviare solo i pacchetti video compresi tra le due ore indicate, scaricando l'intervento completo senza scaricare i GB inutili del resto della giornata
        download_options += f' --downloader ffmpeg --downloader-args "ffmpeg:-ss {video_info["start"]} -to {video_info["end"]}"'
    
    cmd_dl = f'yt-dlp {download_options} "{video_info["url"]}" -o "{final_file}"'
    
    # Esecuzione del download
    dl_res = subprocess.run(cmd_dl, shell=True, capture_output=True, text=True)
    
    if dl_res.returncode == 0 and os.path.exists(final_file) and os.path.getsize(final_file) > 0:
        output_placeholder.success("Il file video è pronto per essere salvato!")
        
        nome_salvataggio = f"{scelta.replace(' ', '_').replace('-', '').replace('(', '').replace(')', '').replace('\'', '')}.mp4"
        
        with open(final_file, "rb") as file:
            st.download_button(
                label="⬇️ Salva il Video sul tuo Dispositivo",
                data=file,
                file_name=nome_salvataggio,
                mime="video/mp4"
            )
    else:
        output_placeholder.error(f"Errore nel recupero del file. Dettaglio: {dl_res.stderr[:400]}")
    
    # Pulizia automatica dei file temporanei sul server cloud
    if os.path.exists(final_file):
        try:
            os.remove(final_file)
        except Exception:
            pass
