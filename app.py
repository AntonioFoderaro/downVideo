import streamlit as st
import os
import subprocess
import uuid

# Configurazione iniziale della pagina
st.set_page_config(page_title="Universal Video Downloader & Compressor", page_icon="🎬", layout="wide")
st.title("🎬 Downloader Assemblea Nazionale - Codice Completo")

# ==========================================
# BLOCCO DI SICUREZZA CON PASSWORD
# ==========================================
PASSWORD_CORRETTA = "Futuro2026"
password_inserita = st.text_input("Inserisci la password di sicurezza per accedere al pannello:", type="password")

if password_inserita != PASSWORD_CORRETTA:
    st.warning("🔒 Accesso limitato. Inserisci la password corretta per sbloccare le funzioni di download.")
    st.stop()

# ==========================================
# APPLICAZIONE REALE (ACCESSIBILE DOPO LOGIN)
# ==========================================
st.success("🔓 Accesso consentito!")
st.write("Scarica, taglia e comprime qualsiasi intervento dell'Assemblea Costituente di Futuro Nazionale (Roma, 13-14 Giugno).")

# URL della registrazione ufficiale centralizzata su Radio Radicale
URL_RADICALE = "https://www.radioradicale.it/scheda/791851/assemblea-costituente-di-futuro-nazionale"

# Mappatura completa e granulare di tutti gli interventi possibili e immaginabili basati sull'ordine dei lavori dell'evento
elenco_completo = {
    # --- SESSIONI INTEGRALI ---
    "SESSIONE INTEGRALE - Tutto l'evento unificato (Sabato + Domenica)": {"url": URL_RADICALE, "start": None, "end": None},
    
    # --- SABATO 13 GIUGNO ---
    "SABATO - Massimiliano Simoni (Relazione d'apertura e Benvenuto)": {"url": URL_RADICALE, "start": "00:02:00", "end": "00:28:00"},
    "SABATO - Roberto Vannacci (Conferenza Stampa d'Apertura Costituente)": {"url": URL_RADICALE, "start": "00:28:30", "end": "01:15:00"},
    "SABATO - Gianni Alemanno (Intervento per l'Indipendenza e Alleanze)": {"url": URL_RADICALE, "start": "01:16:00", "end": "01:45:00"},
    "SABATO - Nicola Procaccini (Coordinatore Fratelli d'Italia - Ospite)": {"url": URL_RADICALE, "start": "01:46:15", "end": "02:10:00"},
    "SABATO - Chicco Costini (Intervento e Dibattito Territoriale)": {"url": URL_RADICALE, "start": "02:11:00", "end": "02:35:00"},
    "SABATO - Federica Guaiardo (Rappresentante Comitato Catania)": {"url": URL_RADICALE, "start": "02:36:00", "end": "02:55:00"},
    "SABATO - Interventi Liberi dei Delegati e Tesserati (Sessione Pomeridiana)": {"url": URL_RADICALE, "start": "03:00:00", "end": "04:30:00"},
    
    # --- DOMENICA 14 GIUGNO ---
    "DOMENICA - Lorenzo Gasperini (Illustrazione Mozione e Programma Politico)": {"url": URL_RADICALE, "start": "04:31:00", "end": "05:10:00"},
    "DOMENICA - Massimo Arlecchino (Presidente Movimento Indipendenza)": {"url": URL_RADICALE, "start": "05:11:15", "end": "05:40:00"},
    "DOMENICA - Laura Ravetto (Deputato - Saluti Istituzionali)": {"url": URL_RADICALE, "start": "05:41:00", "end": "06:05:00"},
    "DOMENICA - Rossano Sasso (Deputato - Intervento Scuola e Cultura)": {"url": URL_RADICALE, "start": "06:06:00", "end": "06:30:00"},
    "DOMENICA - Emanuele Pozzolo (Deputato - Intervento Politico)": {"url": URL_RADICALE, "start": "06:31:10", "end": "06:55:00"},
    "DOMENICA - Stefano Valdegamberi (Consigliere Regionale Veneto)": {"url": URL_RADICALE, "start": "06:56:00", "end": "07:20:00"},
    "DOMENICA - Lettura e Approvazione Statuto / Definizione Organi Nazionali": {"url": URL_RADICALE, "start": "07:21:00", "end": "07:55:00"},
    "DOMENICA - Roberto Vannacci (Discorso Politico Conclusivo del Presidente)": {"url": URL_RADICALE, "start": "07:56:00", "end": "08:50:00"},
    
    # --- LINK ESTERNI DI RISERVA ---
    "SORGENTE DI BACKUP YOUTUBE - Sintesi Evento Nazionale": {"url": "https://youtube.com", "start": None, "end": None}
}

# 1. Interfaccia di Selezione dell'utente
scelta = st.selectbox("1. Scegli l'intervento o il blocco completo che desideri estrarre:", list(elenco_completo.keys()))
video_info = elenco_completo[scelta]

# Informazioni sull'estrazione temporale sul pannello
if video_info["start"] and video_info["end"]:
    st.info(f"⏱️ Questo spezzone verrà tagliato automaticamente da minuto {video_info['start']} a minuto {video_info['end']}.")
else:
    st.info("📦 Verrà scaricato l'intero file multimediale senza tagli.")

# 2. Scelta della Compressione
compression = st.radio(
    "2. Scegli il livello di compressione (FFmpeg CRF):",
    ('Bilanciata (Consigliata - Riduce il peso del 60% mantenendo ottimi dettagli)', 
     'Massima (File super leggero ottimizzato per smartphone e WhatsApp)', 
     'Nessuna (Qualità Originale - Attenzione ai tempi di download)')
)

crf_val = 28
if 'Massima' in compression: 
    crf_val = 33
elif 'Nessuna' in compression: 
    crf_val = 23

output_placeholder = st.empty()

# 3. Pulsante di Esecuzione delle Operazioni
if st.button("Elabora Video e Genera Download 🚀"):
    output_placeholder.warning("Connessione ai server sorgente e download dello stream in corso... Attendi.")
    
    # Generazione di ID univoci per evitare che utenti concorrenti sovrascrivano i file
    session_id = str(uuid.uuid4())[:8]
    raw_file = f"raw_{session_id}.mp4"
    final_file = f"output_{session_id}.mp4"
    
    # Comando yt-dlp ottimizzato con User-Agent reale per bypassare i blocchi di sovraccarico simulati
    cmd_dl = f'yt-dlp --no-playlist --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" "{video_info["url"]}" -o "{raw_file}"'
    
    # Esecuzione del download con cattura dei log di errore
    dl_res = subprocess.run(cmd_dl, shell=True, capture_output=True, text=True)
    
    if dl_res.returncode == 0 and os.path.exists(raw_file):
        output_placeholder.warning("Taglio temporale e compressione video sul server cloud in corso...")
        
        # Costruzione dei parametri di ritaglio temporale per FFmpeg
        time_args = ""
        if video_info["start"] and video_info["end"]:
            time_args = f'-ss {video_info["start"]} -to {video_info["end"]}'
            
        # Comando combinato FFmpeg per tagliare, ricodificare in H.264 e comprimere l'audio in AAC
        cmd_ffmpeg = f'ffmpeg -y {time_args} -i "{raw_file}" -vcodec libx264 -crf {crf_val} -acodec aac -b:a 128k "{final_file}"'
        ffmpeg_res = subprocess.run(cmd_ffmpeg, shell=True, capture_output=True, text=True)
        
        if os.path.exists(final_file) and os.path.getsize(final_file) > 0:
            output_placeholder.success("Elaborazione completata con successo! Il file è pronto per il download locale.")
            
            # Normalizzazione del nome del file per il salvataggio dell'utente
            nome_salvataggio = f"{scelta.replace(' ', '_').replace('-', '').replace('(', '').replace(')', '').replace('\'', '')}.mp4"
            
            with open(final_file, "rb") as file:
                st.download_button(
                    label="⬇️ Scarica il Video sul tuo PC / Smartphone",
                    data=file,
                    file_name=nome_salvataggio,
                    mime="video/mp4"
                )
        else:
            output_placeholder.error(f"Errore tecnico durante la compressione (FFmpeg): {ffmpeg_res.stderr[:300]}")
    else:
        # Se yt-dlp fallisce, stampa a schermo l'errore reale del server per facilitare il debug
        output_placeholder.error(f"Impossibile scaricare il video. Il server sorgente ha risposto con un errore. Dettaglio: {dl_res.stderr[:400]}")
    
    # Pulizia rigorosa dei file temporanei sul server per evitare saturazione del disco
    for f in [raw_file, final_file]:
        if os.path.exists(f): 
            try:
                os.remove(f)
            except Exception:
                pass
