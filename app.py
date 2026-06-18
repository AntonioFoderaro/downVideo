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
st.write("Seleziona l'oratore per scaricare ed estrarre il suo intervento video originale.")

# LINK DIRETTI AI FLUSSI STREAMING (Sostituisci questi URL con i file .mp4 o .m3u8 reali del server video)
STREAM_DIRETTO_SABATO = "https://radioradicale.it"
STREAM_DIRETTO_DOMENICA = "https://radioradicale.it"

# Mappatura: ciascun oratore punta al file di streaming video reale con il suo minutaggio nativo completo
elenco_completo = {
    "SESSIONE COMPLETA - Sabato 13 Giugno (Registrazione Integrale)": {"stream_url": STREAM_DIRETTO_SABATO, "start": None, "end": None},
    
    # --- ORATORI ED INTERVENTI SABATO 13 GIUGNO ---
    "SABATO - Massimiliano Simoni (Relazione d'apertura completa)": {"stream_url": STREAM_DIRETTO_SABATO, "start": "00:02:00", "end": "00:28:00"}, 
    "SABATO - Roberto Vannacci (Conferenza Stampa ed Apertura dei Lavori)": {"stream_url": STREAM_DIRETTO_SABATO, "start": "00:28:30", "end": "01:15:00"},
    "SABATO - Gianni Alemanno (Intervento integrale Movimento Indipendenza)": {"stream_url": STREAM_DIRETTO_SABATO, "start": "01:16:00", "end": "01:45:00"},
    "SABATO - Nicola Procaccini (Discorso integrale ospite FDI)": {"stream_url": STREAM_DIRETTO_SABATO, "start": "01:46:15", "end": "02:10:00"},
    "SABATO - Chicco Costini (Intervento e dibattito territoriale completo)": {"stream_url": STREAM_DIRETTO_SABATO, "start": "02:11:00", "end": "02:35:00"},
    "SABATO - Federica Guaiardo (Intervento delegazione Catania completo)": {"stream_url": STREAM_DIRETTO_SABATO, "start": "02:36:00", "end": "02:55:00"},
    "SABATO - Spazio Integrale Dibattiti Liberi (Tutti i Delegati del Pomeriggio)": {"stream_url": STREAM_DIRETTO_SABATO, "start": "03:00:00", "end": "09:00:00"},
    
    # --- ORATORI ED INTERVENTI DOMENICA 14 GIUGNO ---
    "DOMENICA - Lorenzo Gasperini (Presentazione Programma e Mozione Nazionale)": {"stream_url": STREAM_DIRETTO_DOMENICA, "start": "09:01:00", "end": "09:40:00"},
    "DOMENICA - Massimo Arlecchino (Relazione Presidenza Nazionale)": {"stream_url": STREAM_DIRETTO_DOMENICA, "start": "09:41:15", "end": "10:10:00"},
    "DOMENICA - Laura Ravetto (Saluti Istituzionali completi)": {"stream_url": STREAM_DIRETTO_DOMENICA, "start": "10:11:00", "end": "10:35:00"},
    "DOMENICA - Rossano Sasso (Intervento integrale Scuola e Cultura)": {"stream_url": STREAM_DIRETTO_DOMENICA, "start": "10:36:00", "end": "11:00:00"},
    "DOMENICA - Emanuele Pozzolo (Intervento Politico completo)": {"stream_url": STREAM_DIRETTO_DOMENICA, "start": "11:01:10", "end": "11:25:00"},
    "DOMENICA - Stefano Valdegamberi (Discorso Autonomie e Territorio Veneto)": {"stream_url": STREAM_DIRETTO_DOMENICA, "start": "11:26:00", "end": "11:50:00"},
    "DOMENICA - Sessione Integrale Approvazione Statuto e Votazione Organi": {"stream_url": STREAM_DIRETTO_DOMENICA, "start": "11:51:00", "end": "12:30:00"},
    "DOMENICA - Roberto Vannacci (Discorso Politico Conclusivo del Presidente)": {"stream_url": STREAM_DIRETTO_DOMENICA, "start": "12:31:00", "end": "13:30:00"},
}

# 1. Interfaccia di Selezione del video
scelta = st.selectbox("Seleziona l'oratore o la sessione:", list(elenco_completo.keys()))
video_info = elenco_completo[scelta]

output_placeholder = st.empty()

# 2. Pulsante per avviare il Download
if st.button("Scarica e Genera File Video 🚀"):
    output_placeholder.warning("Connessione al server video in corso... Download dell'intervento avviato.")
    
    session_id = str(uuid.uuid4())[:8]
    final_file = f"video_{session_id}.mp4"
    
    # Costruzione del comando FFmpeg nativo (Legge il flusso video diretto senza usare yt-dlp)
    if video_info["start"] and video_info["end"]:
        # Taglia lo spezzone copiando i codec originali (velocissimo, zero consumo di memoria e CPU)
        cmd_ffmpeg = f'ffmpeg -y -ss {video_info["start"]} -to {video_info["end"]} -i "{video_info["stream_url"]}" -c copy -bsf:a aac_adtstoasc "{final_file}"'
    else:
        # Scarica il file video intero così com'è
        cmd_ffmpeg = f'ffmpeg -y -i "{video_info["stream_url"]}" -c copy -bsf:a aac_adtstoasc "{final_file}"'
        
    # Esecuzione dell'estrazione multimediale
    ffmpeg_res = subprocess.run(cmd_ffmpeg, shell=True, capture_output=True, text=True)
    
    if os.path.exists(final_file) and os.path.getsize(final_file) > 0:
        output_placeholder.success("Il file video dell'oratore è pronto per il salvataggio!")
        
        # Pulizia del nome per il salvataggio sul PC dell'utente
        nome_salvataggio = f"{scelta.replace(' ', '_').replace('-', '').replace('(', '').replace(')', '').replace('\'', '')}.mp4"
        
        with open(final_file, "rb") as file:
            st.download_button(
                label="⬇️ Salva il Video sul tuo Dispositivo",
                data=file,
                file_name=nome_salvataggio,
                mime="video/mp4"
            )
    else:
        output_placeholder.error(f"Impossibile estrarre il video. Verifica che il link di streaming sia online. Log tecnico: {ffmpeg_res.stderr[:350]}")
    
    # Rimozione immediata del file temporaneo locale
    if os.path.exists(final_file):
        try:
            os.remove(final_file)
        except Exception:
            pass
