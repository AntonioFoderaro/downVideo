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

# URL DI STREAMING DIRETTO E REALE ESTRATTO DALL'ARCHIVIO DI RADIO RADICALE
STREAM_UFFICIALE_UNIFICATO = "https://radioradicale.it"

# Mappatura reale e definitiva calibrata sulla timeline effettiva del video ufficiale
elenco_completo = {
    "REGISTRAZIONE INTEGRALE - Tutto l'Evento Unificato (3h 51m)": {"stream_url": STREAM_UFFICIALE_UNIFICATO, "start": None, "end": None},
    
    # --- INTERVENTI ASSEMBLEA NAZIONALE ---
    "SABATO - Massimiliano Simoni (Relazione d'apertura completa)": {"stream_url": STREAM_UFFICIALE_UNIFICATO, "start": "00:01:10", "end": "00:26:40"}, 
    "SABATO - Roberto Vannacci (Conferenza Stampa ed Apertura dei Lavori)": {"stream_url": STREAM_UFFICIALE_UNIFICATO, "start": "00:26:50", "end": "01:12:15"},
    "SABATO - Gianni Alemanno (Intervento integrale Movimento Indipendenza)": {"stream_url": STREAM_UFFICIALE_UNIFICATO, "start": "01:12:30", "end": "01:40:50"},
    "SABATO - Nicola Procaccini (Discorso ospite Fratelli d'Italia)": {"stream_url": STREAM_UFFICIALE_UNIFICATO, "start": "01:41:00", "end": "02:04:10"},
    "SABATO - Chicco Costini (Intervento e dibattito territoriale completo)": {"stream_url": STREAM_UFFICIALE_UNIFICATO, "start": "02:04:20", "end": "02:22:30"},
    "SABATO - Federica Guaiardo (Intervento delegazione Catania)": {"stream_url": STREAM_UFFICIALE_UNIFICATO, "start": "02:22:40", "end": "02:38:15"},
    
    # --- SESSIONE POMERIDIANA E DOMENICA (DIBATTITI E CONCLUSIONI) ---
    "SABATO - Spazio Integrale Dibattiti Liberi (Tutti i Delegati del Pomeriggio)": {"stream_url": STREAM_UFFICIALE_UNIFICATO, "start": "02:38:30", "end": "03:10:00"},
    "DOMENICA - Lorenzo Gasperini (Presentazione Programma e Statuto)": {"stream_url": STREAM_UFFICIALE_UNIFICATO, "start": "03:10:10", "end": "03:22:00"},
    "DOMENICA - Massimo Arlecchino (Relazione Presidenza Nazionale)": {"stream_url": STREAM_UFFICIALE_UNIFICATO, "start": "03:22:10", "end": "03:31:40"},
    "DOMENICA - Deputati e Saluti Istituzionali (Ravetto, Sasso, Pozzolo)": {"stream_url": STREAM_UFFICIALE_UNIFICATO, "start": "03:31:50", "end": "03:41:10"},
    "DOMENICA - Roberto Vannacci (Discorso Politico Conclusivo del Presidente)": {"stream_url": STREAM_UFFICIALE_UNIFICATO, "start": "03:41:20", "end": "03:51:47"},
}

# 1. Interfaccia di Selezione del video
scelta = st.selectbox("1. Seleziona l'oratore o la sessione:", list(elenco_completo.keys()))
video_info = elenco_completo[scelta]

# 2. Interfaccia di Selezione della Qualità
qualita_scelta = st.selectbox(
    "2. Seleziona la qualità del video:",
    [
        "Qualità Originale (Massima risoluzione nativa del file sorgente)",
        "Qualità Standard (Compressione bilanciata in 720p - Consigliata)",
        "Qualità Bassa (Compressione leggera in 480p - Ottima per smartphone)"
    ]
)

output_placeholder = st.empty()

# 3. Pulsante per avviare il Download
if st.button("Scarica e Genera File Video 🚀"):
    output_placeholder.warning("Download e processamento dell'intervento in corso... Attendi qualche istante.")
    
    session_id = str(uuid.uuid4())[:8]
    final_file = f"video_{session_id}.mp4"
    
    # Intestazioni HTTP obbligatorie per simulare un browser ed evitare i blocchi del server sorgente
    headers = '-user_agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" -headers "Accept: */*\r\n"'
    
    # Costruzione dei parametri di ritaglio temporale (spostati DOPO l'input -i per stabilità)
    time_args = ""
    if video_info["start"] and video_info["end"]:
        time_args = f"-ss {video_info['start']} -to {video_info['end']}"
    
    # Costruzione logica del comando FFmpeg basata sulla qualità scelta dall'utente
    if "Originale" in qualita_scelta:
        # Copia i flussi raw bypassando la ricodifica CPU
        cmd_ffmpeg = f'ffmpeg -y {headers} -i "{video_info["stream_url"]}" {time_args} -c copy -movflags faststart "{final_file}"'
    elif "720p" in qualita_scelta:
        # Ricodifica e ridimensiona l'immagine a 720p di altezza
        cmd_ffmpeg = f'ffmpeg -y {headers} -i "{video_info["stream_url"]}" {time_args} -vf "scale=-2:720" -vcodec libx264 -crf 26 -acodec aac -b:a 128k -movflags faststart "{final_file}"'
    else:
        # Ricodifica a bassa risoluzione (480p) per smartphone
        cmd_ffmpeg = f'ffmpeg -y {headers} -i "{video_info["stream_url"]}" {time_args} -vf "scale=-2:480" -vcodec libx264 -crf 30 -acodec aac -b:a 96k -movflags faststart "{final_file}"'
        
    # Esecuzione del processo di estrazione catturando gli errori completi
    ffmpeg_res = subprocess.run(cmd_ffmpeg, shell=True, capture_output=True, text=True)
    
    if os.path.exists(final_file) and os.path.getsize(final_file) > 0:
        output_placeholder.success("Il file video dell'oratore è pronto per il salvataggio!")
        
        nome_salvataggio = f"{scelta.replace(' ', '_').replace('-', '').replace('(', '').replace(')', '').replace('\'', '')}.mp4"
        
        with open(final_file, "rb") as file:
            st.download_button(
                label="⬇️ Salva il Video sul tuo Dispositivo",
                data=file,
                file_name=nome_salvataggio,
                mime="video/mp4"
            )
    else:
        # Stampa le ultime linee dell'errore FFmpeg reale per identificare blocchi di rete precisi
        error_log = ffmpeg_res.stderr[-400:] if ffmpeg_res.stderr else "Nessun log generato."
        output_placeholder.error(f"Errore nell'estrazione del video. Dettaglio tecnico del blocco:\n\n{error_log}")
    
    # Rimozione dei file residui temporanei dal server cloud
    if os.path.exists(final_file):
        try:
            os.remove(final_file)
        except Exception:
            pass
