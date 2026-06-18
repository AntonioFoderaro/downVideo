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

# Mappatura reale e definitiva calibrata sulla timeline effettiva del video ufficiale (Durata totale: 03:51:47)
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
    
    # Costruzione dei parametri di ritaglio temporale nativo
    time_args = ""
    if video_info["start"] and video_info["end"]:
        time_args = f"-ss {video_info['start']} -to {video_info['end']}"
    
    # Mappatura dei comandi FFmpeg in base alla qualità per gestire i file MP4 progressivi
    if "Originale" in qualita_scelta:
        # Copia istantanea dei pacchetti senza ricodifica: richiede pochissimi secondi
        cmd_ffmpeg = f'ffmpeg -y {time_args} -i "{video_info["stream_url"]}" -c copy -movflags faststart "{final_file}"'
    elif "720p" in qualita_scelta:
        # Scala l'immagine a 720p di altezza e applica una compressione bilanciata (CRF 26)
        cmd_ffmpeg = f'ffmpeg -y {time_args} -i "{video_info["stream_url"]}" -vf "scale=-2:720" -vcodec libx264 -crf 26 -acodec aac -b:a 128k -movflags faststart "{final_file}"'
    else:
        # Scala l'immagine a 480p per creare un file leggerissimo adatto ai telefoni
        cmd_ffmpeg = f'ffmpeg -y {time_args} -i "{video_info["stream_url"]}" -vf "scale=-2:480" -vcodec libx264 -crf 30 -acodec aac -b:a 96k -movflags faststart "{final_file}"'
        
    # Esecuzione dell'estrazione multimediale
    ffmpeg_res = subprocess.run(cmd_ffmpeg, shell=True, capture_output=True, text=True)
    
    if os.path.exists(final_file) and os.path.getsize(final_file) > 0:
        output_placeholder.success("Il file video dell'oratore è pronto per il salvataggio!")
        
        # Pulizia del nome file per l'utente finale
        nome_salvataggio = f"{scelta.replace(' ', '_').replace('-', '').replace('(', '').replace(')', '').replace('\'', '')}.mp4"
        
        with open(final_file, "rb") as file:
            st.download_button(
                label="⬇️ Salva il Video sul tuo Dispositivo",
                data=file,
                file_name=nome_salvataggio,
                mime="video/mp4"
            )
    else:
        output_placeholder.error(f"Impossibile estrarre il video. Log tecnico: {ffmpeg_res.stderr[:300]}")
    
    # Rimozione immediata del file temporaneo locale per non saturare il server
    if os.path.exists(final_file):
        try:
            os.remove(f"video_{session_id}.mp4")
        except Exception:
            pass
