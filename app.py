import streamlit as st
import os
import urllib.request
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

# 1. MENU A TENDINA CON TUTTI I FLUSSI INTERI DIRETTI (.MP4) SENZA SPEZZONI
st.subheader("🔗 Selezione Intervento dell'Assemblea Nazionale")

dizionario_video = {
    "SABATO - Massimiliano Simoni (Relazione d'apertura completa)": "https://radioradicale.it", 
    "SABATO - Gianni Alemanno (Intervento integrale Movimento Indipendenza)": "https://radioradicale.it",
    "SABATO - Nicola Procaccini (Discorso integrale ospite FDI)": "https://radioradicale.it",
    "SABATO - Chicco Costini (Intervento e dibattito territoriale completo)": "https://radioradicale.it",
    "SABATO - Federica Guaiardo (Intervento delegazione Catania completo)": "https://radioradicale.it",
    "SABATO - Spazio Integrale Dibattiti Liberi (Tutti i Delegati del Pomeriggio)": "https://radioradicale.it",
    "DOMENICA - Lorenzo Gasperini (Presentazione Programma e Statuto)": "https://radioradicale.it",
    "DOMENICA - Massimo Arlecchino (Relazione Presidenza Nazionale)": "https://radioradicale.it",
    "DOMENICA - Saluti Istituzionali dei Deputati (Ravetto, Sasso, Pozzolo)": "https://radioradicale.it",
    "REGISTRAZIONE INTEGRALE - Sabato + Domenica (File Unificato Radio Radicale)": "https://radioradicale.it",
    "SABATO - Roberto Vannacci (Conferenza Stampa - Link di Backup Alternativo)": "https://radioradicale.it",
    "DOMENICA - Roberto Vannacci (Discorso Conclusivo - Link di Backup Alternativo)": "https://radioradicale.it"
}

scelta_sorgente = st.selectbox(
    "Seleziona l'intervento o la giornata che desideri scaricare integralmente:", 
    list(dizionario_video.keys())
)
url_selezionato = dizionario_video[scelta_sorgente]

# 2. SELEZIONE FISSA DELLA QUALITÀ (ALTA, MEDIA, BASSA)
st.subheader("🎬 Configurazione Risoluzione e Qualità Video")

qualita_scelta = st.selectbox(
    "Scegli il livello di qualità desiderato per il file finale:",
    [
        "Alta Qualità (Massima risoluzione originale del file nativo)",
        "Media Qualità (Risoluzione bilanciata ottimizzata in 720p)",
        "Bassa Qualità (Risoluzione compressa a 480p per Smartphone)"
    ]
)

output_placeholder = st.empty()

# 3. PULSANTE DI SCARICAMENTO DEL VIDEO INTEGRALE
if st.button("Scarica e Genera File Video Integrale 🚀"):
    session_id = str(uuid.uuid4())[:8]
    raw_file = f"raw_{session_id}.mp4"
    final_file = f"video_{session_id}.mp4"
    
    try:
        # Definizione della barra di avanzamento e dei messaggi nello stato grafico
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Funzione di tracciamento dei blocchi di byte scaricati per animare la barra
        def hook_avanzamento(blocco_count, blocco_size, totale_size):
            if totale_size > 0:
                percentuale = min(int(blocco_count * blocco_size * 100 / totale_size), 100)
                progress_bar.progress(percentuale / 100)
                status_text.text(f"📥 Download dello stream originale in corso: {percentuale}% completato...")
        
        # Creazione della richiesta HTTP con User-Agent per evitare qualsiasi blocco di sicurezza dei server
        richiesta = urllib.request.Request(
            url_selezionato, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        
        # Download lineare del file binario MP4 nativo sul disco del server
        with urllib.request.urlopen(richiesta) as response, open(raw_file, 'wb') as out_file:
            totale_dimensione = int(response.info().get('Content-Length', 0))
            blocco_dimensione = 1024 * 256
            conteggio_blocchi = 0
            
            while True:
                buffer = response.read(blocco_dimensione)
                if not buffer:
                    break
                conteggio_blocchi += 1
                out_file.write(buffer)
                hook_avanzamento(conteggio_blocchi, blocco_dimensione, totale_dimensione)
                
        status_text.text("⚙️ Ottimizzazione della risoluzione e del formato video richiesto...")
        
        # 4. GESTIONE DELLA QUALITÀ TRAMITE FFMPEG LOCALE (Alta, Media, Bassa)
        if "Alta" in qualita_scelta:
            # Sposta l'indice in cima (faststart) senza toccare la CPU, mantenendo la qualità originale massima
            cmd_ffmpeg = f'ffmpeg -y -i "{raw_file}" -c copy -movflags faststart "{final_file}"'
        elif "Media" in qualita_scelta:
            # Applica una compressione ed effettua il ridimensionamento a 720p di altezza
            cmd_ffmpeg = f'ffmpeg -y -i "{raw_file}" -vf "scale=-2:720" -vcodec libx264 -crf 26 -acodec aac -b:a 128k -movflags faststart "{final_file}"'
        else:
            # Comprime in 480p per generare un file super leggero
            cmd_ffmpeg = f'ffmpeg -y -i "{raw_file}" -vf "scale=-2:480" -vcodec libx264 -crf 30 -acodec aac -b:a 96k -movflags faststart "{final_file}"'
            
        # Esecuzione del processo multimediale interno
        subprocess.run(cmd_ffmpeg, shell=True, capture_output=True, text=True)
        
        # Rimozione immediata del file raw scaricato per liberare memoria sul server
        if os.path.exists(raw_file):
            os.remove(raw_file)
            
        if os.path.exists(final_file) and os.path.getsize(final_file) > 0:
            progress_bar.empty()
            status_text.empty()
            output_placeholder.success("File video integrale generato con successo!")
            
            # Normalizzazione del nome file finale per l'utente
            nome_file_pulito = scelta_sorgente.replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '')
            nome_salvataggio = f"{nome_file_pulito}.mp4"
            
            with open(final_file, "rb") as file:
                st.download_button(
                    label="⬇️ Salva il Video sul tuo Dispositivo",
                    data=file,
                    file_name=nome_salvataggio,
                    mime="video/mp4"
                )
        else:
            output_placeholder.error("Errore durante l'ottimizzazione del file video locale. Spazio su disco terminato.")
            
    except Exception as e:
        output_placeholder.error(f"Impossibile completare l'operazione di download. Dettaglio: {str(e)}")
        
    # Pulizia automatica dello storage locale del server cloud per evitare saturazione
    for f in [raw_file, final_file]:
        if os.path.exists(f):
            try: os.remove(f)
            except Exception: pass

