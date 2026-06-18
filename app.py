import streamlit as st
import os
import yt_dlp
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

# 1. TENDINA CON TUTTI I VIDEO INTEGRALI ESTRATTI DA RADIO RADICALE E YOUTUBE
st.subheader("🔗 Selezione Intervento dell'Assemblea Nazionale")

dizionario_video = {
    # --- INTERVENTI DA RADIO RADICALE (STREAMING DIRETTI .MP4 COMPLETI) ---
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
    
    # --- INTERVENTI DA YOUTUBE (STREAMING COMPLETI) ---
    "SABATO - Roberto Vannacci (Conferenza Stampa ed Apertura dei Lavori)": "https://youtube.com",
    "DOMENICA - Roberto Vannacci (Discorso Politico Conclusivo del Presidente)": "https://youtube.com",
    "SORGENTE DI BACKUP - Sintesi e Highlights dell'Assemblea Costituente": "https://youtube.com"
}

scelta_sorgente = st.selectbox(
    "Seleziona l'intervento o la giornata che desideri scaricare integralmente:", 
    list(dizionario_video.keys())
)
url_selezionato = dizionario_video[scelta_sorgente]

# 2. SELEZIONE DELLA QUALITÀ (CON ALTA E MEDIA)
st.subheader("🎬 Configurazione Risoluzione e Qualità Video")

qualita_scelta = st.selectbox(
    "Scegli il livello di qualità desiderato per il file finale:",
    [
        "Alta Qualità (Massima risoluzione originale senza compressione)",
        "Media Qualità (Risoluzione ottimizzata in 720p - Consigliata per PC)",
        "Qualità Standard (Risoluzione bilanciata in 480p per Smartphone)",
        "Bassa Qualità (Risoluzione compressa a 360p - Minimo peso)"
    ]
)

# Mappatura dei parametri di filtraggio altezza per yt-dlp
if "Alta" in qualita_scelta:
    stringa_formato = "bestvideo+bestaudio/best"
elif "Media" in qualita_scelta:
    stringa_formato = "bestvideo[height<=720]+bestaudio/best[height<=720]"
elif "Standard" in qualita_scelta:
    stringa_formato = "bestvideo[height<=480]+bestaudio/best[height<=480]"
else:
    stringa_formato = "bestvideo[height<=360]+bestaudio/best[height<=360]"

output_placeholder = st.empty()

# 3. PULSANTE DI SCARICAMENTO DEL VIDEO INTEGRALE
if st.button("Scarica e Genera File Video Integrale 🚀"):
    output_placeholder.warning("Connessione ai server cloud e download del file multimediale avviato... Attendi.")
    
    session_id = str(uuid.uuid4())[:8]
    final_file = f"video_{session_id}.mp4"
    
    # Opzioni di download stabili per gestire flussi MP4 diretti ed evitare blocchi
    ydl_opts_dl = {
        'format': stringa_formato,
        'merge_output_format': 'mp4',
        'outtmpl': f'video_{session_id}.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        # Esclude gli estrattori di testo automatici se rileva un link di Radio Radicale
        'force_generic_extractor': True if "radioradicale" in url_selezionato else False,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts_dl) as ydl:
            ydl.download([url_selezionato])
            
        # Normalizzazione del formato in caso di elaborazioni MKV in background
        if os.path.exists(f"video_{session_id}.mp4"):
            final_file = f"video_{session_id}.mp4"
        elif os.path.exists(f"video_{session_id}.mkv"):
            os.rename(f"video_{session_id}.mkv", f"video_{session_id}.mp4")
            
        if os.path.exists(final_file) and os.path.getsize(final_file) > 0:
            output_placeholder.success("File video generato con successo!")
            
            # Creazione di un nome file pulito per il salvataggio locale dell'utente
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
            output_placeholder.error("Errore: il file è stato scaricato ma risulta vuoto. Verifica lo spazio sul server cloud.")
            
    except Exception as e:
        output_placeholder.error(f"Impossibile completare il download. Dettaglio tecnico del server sorgente: {str(e)}")
        
    # Rimozione dei residui temporanei dal disco del server
    if os.path.exists(final_file):
        try: os.remove(final_file)
        except Exception: pass
