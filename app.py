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

# L'unico URL reale e supportato dall'estrattore per l'evento di Radio Radicale
URL_SORGENTE_UFFICIALE = "https://radioradicale.it"

# Mappatura: ciascun oratore punta alla sorgente corretta con il suo rispettivo minutaggio nativo completo
elenco_completo = {
    "SESSIONE COMPLETA - Sabato 13 Giugno (Registrazione Integrale)": {"url": URL_SORGENTE_UFFICIALE, "start": None, "end": None},
    
    # --- ORATORI ED INTERVENTI SABATO 13 GIUGNO ---
    "SABATO - Massimiliano Simoni (Relazione d'apertura completa)": {"url": URL_SORGENTE_UFFICIALE, "start": "00:02:00", "end": "00:28:00"}, 
    "SABATO - Roberto Vannacci (Conferenza Stampa ed Apertura dei Lavori)": {"url": URL_SORGENTE_UFFICIALE, "start": "00:28:30", "end": "01:15:00"},
    "SABATO - Gianni Alemanno (Intervento integrale Movimento Indipendenza)": {"url": URL_SORGENTE_UFFICIALE, "start": "01:16:00", "end": "01:45:00"},
    "SABATO - Nicola Procaccini (Discorso integrale ospite FDI)": {"url": URL_SORGENTE_UFFICIALE, "start": "01:46:15", "end": "02:10:00"},
    "SABATO - Chicco Costini (Intervento e dibattito territoriale completo)": {"url": URL_SORGENTE_UFFICIALE, "start": "02:11:00", "end": "02:35:00"},
    "SABATO - Federica Guaiardo (Intervento delegazione Catania completo)": {"url": URL_SORGENTE_UFFICIALE, "start": "02:36:00", "end": "02:55:00"},
    "SABATO - Spazio Integrale Dibattiti Liberi (Tutti i Delegati del Pomeriggio)": {"url": URL_SORGENTE_UFFICIALE, "start": "03:00:00", "end": "09:00:00"},
    
    # --- ORATORI ED INTERVENTI DOMENICA 14 GIUGNO ---
    "DOMENICA - Lorenzo Gasperini (Presentazione Programma e Mozione Nazionale)": {"url": URL_SORGENTE_UFFICIALE, "start": "09:01:00", "end": "09:40:00"},
    "DOMENICA - Massimo Arlecchino (Relazione Presidenza Nazionale)": {"url": URL_SORGENTE_UFFICIALE, "start": "09:41:15", "end": "10:10:00"},
    "DOMENICA - Laura Ravetto (Saluti Istituzionali completi)": {"url": URL_SORGENTE_UFFICIALE, "start": "10:11:00", "end": "10:35:00"},
    "DOMENICA - Rossano Sasso (Intervento integrale Scuola e Cultura)": {"url": URL_SORGENTE_UFFICIALE, "start": "10:36:00", "end": "11:00:00"},
    "DOMENICA - Emanuele Pozzolo (Intervento Politico completo)": {"url": URL_SORGENTE_UFFICIALE, "start": "11:01:10", "end": "11:25:00"},
    "DOMENICA - Stefano Valdegamberi (Discorso Autonomie e Territorio Veneto)": {"url": URL_SORGENTE_UFFICIALE, "start": "11:26:00", "end": "11:50:00"},
    "DOMENICA - Sessione Integrale Approvazione Statuto e Votazione Organi": {"url": URL_SORGENTE_UFFICIALE, "start": "11:51:00", "end": "12:30:00"},
    "DOMENICA - Roberto Vannacci (Discorso Politico Conclusivo del Presidente)": {"url": URL_SORGENTE_UFFICIALE, "start": "12:31:00", "end": "13:30:00"},
}

# 1. Interfaccia di Selezione del video
scelta = st.selectbox("1. Seleziona l'oratore o la sessione:", list(elenco_completo.keys()))
video_info = elenco_completo[scelta]

# 2. Interfaccia di Selezione della Qualità
qualita_scelta = st.selectbox(
    "2. Seleziona la qualità del video:",
    [
        "Massima Qualità Disponibile (Risoluzione originale)",
        "Alta Qualità (Fino a 1080p)",
        "Qualità Standard (Fino a 720p)",
        "Qualità Bassa (Fino a 480p)",
        "Qualità Minima (Fino a 360p)"
    ]
)

# Definizione dei selettori di formato compatibili
if "Massima" in qualita_scelta:
    format_arg = "best"
elif "1080p" in qualita_scelta:
    format_arg = "best[height<=1080]"
elif "720p" in qualita_scelta:
    format_arg = "best[height<=720]"
elif "480p" in qualita_scelta:
    format_arg = "best[height<=480]"
else:
    format_arg = "best[height<=360]"

output_placeholder = st.empty()

# 3. Pulsante per avviare il Download
if st.button("Scarica e Genera File Video 🚀"):
    output_placeholder.warning("Connessione ai server di Radio Radicale e download dello stream in corso...")
    
    session_id = str(uuid.uuid4())[:8]
    raw_file = f"raw_{session_id}.mp4"
    final_file = f"video_{session_id}.mp4"
    
    # Estrazione dell'URL dello stream diretto tramite yt-dlp per evitare blocchi e analizzare l'indirizzo reale
    cmd_url = f'yt-dlp -f "{format_arg}" --get-url --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "{video_info["url"]}"'
    url_res = subprocess.run(cmd_url, shell=True, capture_output=True, text=True)
    
    if url_res.returncode == 0 and url_res.stdout.strip():
        stream_url = url_res.stdout.strip().split('\n')[0] # Prende il primo stream video/audio unificato valido
        
        output_placeholder.warning("Generazione del file video in corso sul server... Attendi.")
        
        # Gestione del ritaglio temporale direttamente tramite FFmpeg nativo per evitare conflitti di URL esterni
        if video_info["start"] and video_info["end"]:
            cmd_ffmpeg = f'ffmpeg -y -ss {video_info["start"]} -to {video_info["end"]} -i "{stream_url}" -c copy "{final_file}"'
        else:
            cmd_ffmpeg = f'ffmpeg -y -i "{stream_url}" -c copy "{final_file}"'
            
        ffmpeg_res = subprocess.run(cmd_ffmpeg, shell=True, capture_output=True, text=True)
        
        if os.path.exists(final_file) and os.path.getsize(final_file) > 0:
            output_placeholder.success("Il file video dell'oratore è pronto per il salvataggio!")
            
            # Normalizzazione del nome file
            nome_salvataggio = f"{scelta.replace(' ', '_').replace('-', '').replace('(', '').replace(')', '').replace('\'', '')}.mp4"
            
            with open(final_file, "rb") as file:
                st.download_button(
                    label="⬇️ Salva il Video sul tuo Dispositivo",
                    data=file,
                    file_name=nome_salvataggio,
                    mime="video/mp4"
                )
        else:
            output_placeholder.error(f"Errore durante la scrittura del file video. Log tecnico: {ffmpeg_res.stderr[:300]}")
    else:
        output_placeholder.error(f"Impossibile connettersi a Radio Radicale. Dettaglio: {url_res.stderr[:300]}")
    
    # Pulizia rigorosa dello storage temporaneo
    for f in [raw_file, final_file]:
        if os.path.exists(f):
            try:
                os.remove(f)
            except Exception:
                pass
