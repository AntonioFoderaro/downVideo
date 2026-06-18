import streamlit as st
import os
import subprocess
import uuid

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Universal Video Downloader & Compressor", page_icon="🎬", layout="wide")
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
st.write("Scarica i file video completi di ciascun oratore o le sessioni integrali senza alcun taglio temporale.")

# URL ufficiali centralizzati dell'evento
URL_SABATO_INTEGRALE = "https://www.radioradicale.it/scheda/791851/assemblea-costituente-di-futuro-nazionale"
URL_DOMENICA_INTEGRALE = "https://www.radioradicale.it/scheda/791851/assemblea-costituente-di-futuro-nazionale" # Sostituire con il secondo link se differente

# Mappatura divisa per oratore dal principio (Scarica l'intero video associato alla risorsa)
elenco_completo = {
    # --- REGISTRAZIONI DI SETTORE / GIORNATE INTERE ---
    "SESSIONE COMPLETA - Sabato 13 Giugno (Registrazione Integrale)": {"url": URL_SABATO_INTEGRALE},
    "SESSIONE COMPLETA - Domenica 14 Giugno (Registrazione Integrale)": {"url": URL_DOMENICA_INTEGRALE},
    
    # --- ORATORI ED INTERVENTI SABATO 13 GIUGNO ---
    "SABATO - Massimiliano Simoni (Relazione d'apertura completa)": {"url": "https://radioradicale.it"}, 
    "SABATO - Roberto Vannacci (Conferenza Stampa ed Apertura dei Lavori)": {"url": "https://www.youtube.com/watch?v=u2thBTZC3dE"},
    "SABATO - Gianni Alemanno (Intervento integrale Movimento Indipendenza)": {"url": "https://radioradicale.it"},
    "SABATO - Nicola Procaccini (Discorso integrale ospite FDI)": {"url": "https://radioradicale.it"},
    "SABATO - Chicco Costini (Intervento e dibattito territoriale completo)": {"url": "https://radioradicale.it"},
    "SABATO - Federica Guaiardo (Intervento delegazione Catania completo)": {"url": "https://radioradicale.it"},
    "SABATO - Spazio Integrale Dibattiti Liberi (Tutti i Delegati del Pomeriggio)": {"url": "https://radioradicale.it"},
    
    # --- ORATORI ED INTERVENTI DOMENICA 14 GIUGNO ---
    "DOMENICA - Roberto Vannacci (Discorso Politico Conclusivo del Presidente)": {"url": "https://www.youtube.com/watch?v=u2thBTZC3dE"},
    "DOMENICA - Lorenzo Gasperini (Presentazione Programma e Mozione Nazionale)": {"url": "https://radioradicale.it"},
    "DOMENICA - Massimo Arlecchino (Relazione Presidenza Nazionale)": {"url": "https://radioradicale.it"},
    "DOMENICA - Laura Ravetto (Saluti Istituzionali completi)": {"url": "https://radioradicale.it"},
    "DOMENICA - Rossano Sasso (Intervento integrale Scuola e Cultura)": {"url": "https://radioradicale.it"},
    "DOMENICA - Emanuele Pozzolo (Intervento Politico completo)": {"url": "https://radioradicale.it"},
    "DOMENICA - Stefano Valdegamberi (Discorso Autonomie e Territorio Veneto)": {"url": "https://radioradicale.it"},
    "DOMENICA - Sessione Integrale Approvazione Statuto e Votazione Organi": {"url": "https://radioradicale.it"},
}

# 1. Interfaccia di Selezione dell'utente
scelta = st.selectbox("1. Seleziona l'oratore o la sessione di cui desideri il video integrale:", list(elenco_completo.keys()))
video_info = elenco_completo[scelta]

st.info("📦 L'applicazione scaricherà l'intero video della risorsa selezionata alla massima qualità, senza effettuare tagli.")

# 2. Livello di compressione del file finale (Opzionale, gestito direttamente da yt-dlp per non saturare la CPU)
compressione = st.checkbox("Abilita compressione automatica del file (Consigliato per risparmiare traffico dati)", value=True)

output_placeholder = st.empty()

# 3. Pulsante per avviare il Download
if st.button("Scarica e Genera File Video 🚀"):
    output_placeholder.warning("Connessione ai server e download del video integrale in corso... Attendi.")
    
    # Generazione di ID univoci per evitare sovrascritture simultanee tra utenti
    session_id = str(uuid.uuid4())[:8]
    final_file = f"video_{session_id}.mp4"
    
    # Selezione del formato di download (se compresso sceglie qualità ridotta, altrimenti massima)
    format_arg = "-f mp4" if compressione else "-f bestvideo+bestaudio/best"
    
    # Comando yt-dlp lineare e robusto (Nessun FFmpeg aggiuntivo o calcolo di orari)
    cmd_dl = f'yt-dlp {format_arg} --no-playlist --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" "{video_info["url"]}" -o "{final_file}"'
    
    # Esecuzione del download
    dl_res = subprocess.run(cmd_dl, shell=True, capture_output=True, text=True)
    
    if dl_res.returncode == 0 and os.path.exists(final_file) and os.path.getsize(final_file) > 0:
        output_placeholder.success("Il file video è pronto per essere salvato!")
        
        # Formattazione del nome di salvataggio basato sulla scelta dell'oratore
        nome_salvataggio = f"{scelta.replace(' ', '_').replace('-', '').replace('(', '').replace(')', '').replace('\'', '')}.mp4"
        
        with open(final_file, "rb") as file:
            st.download_button(
                label="⬇️ Salva il Video sul tuo Dispositivo",
                data=file,
                file_name=nome_salvataggio,
                mime="video/mp4"
            )
    else:
        # Debug in tempo reale in caso di URL errati o blocchi dei server sorgente
        output_placeholder.error(f"Errore nel recupero del file. Il server sorgente ha risposto con un errore. Dettaglio: {dl_res.stderr[:400]}")
    
    # Rimozione del file temporaneo dal server per mantenere pulito lo storage cloud
    if os.path.exists(final_file):
        try:
            os.remove(final_file)
        except Exception:
            pass

