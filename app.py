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

# 1. MENU A TENDINA CON FLUSSI DIRETTI COMPLETI (.MP4) PER ESCLUDERE L'ERRORE DI URL NON SUPPORTATO
st.subheader("🔗 Selezione Sorgente Video dell'Assemblea")

dizionario_video = {
    "REGISTRAZIONE INTEGRALE - Assemblea Costituente Nazionale (Video Completo - Radio Radicale)": "https://radioradicale.it",
    "SABATO - Roberto Vannacci (Conferenza Stampa di Apertura - YouTube)": "https://youtube.com",
    "DOMENICA - Roberto Vannacci (Discorso Politico Conclusivo - YouTube)": "https://youtube.com",
    "SORGENTE DI BACKUP - Sintesi e Highlights dell'Assemblea Costituente (YouTube)": "https://youtube.com"
}

scelta_sorgente = st.selectbox(
    "Seleziona il file video completo dell'Assemblea Nazionale da scaricare:", 
    list(dizionario_video.keys())
)
url_selezionato = dizionario_video[scelta_sorgente]

# 2. SELEZIONE FISSA DELLA QUALITÀ RICHIESTA (ALTA, MEDIA, BASSA)
st.subheader("🎬 Configurazione Risoluzione e Compressione")

qualita_scelta = st.selectbox(
    "Scegli il livello di qualità desiderato per il file integrale:",
    [
        "Alta Qualità (Massima risoluzione originale senza compressione)",
        "Media Qualità (Risoluzione ottimizzata in 720p - Consigliata)",
        "Qualità Standard (Risoluzione bilanciata in 480p per smartphone)",
        "Bassa Qualità (Risoluzione compressa a 360p - Minimo peso)"
    ]
)

# Mappatura delle altezze in pixel accettate dal filtro di yt-dlp
if "Alta" in qualita_scelta:
    stringa_formato = "bestvideo+bestaudio/best"
elif "Media" in qualita_scelta:
    stringa_formato = "bestvideo[height<=720]+bestaudio/best[height<=720]"
elif "Standard" in qualita_scelta:
    stringa_formato = "bestvideo[height<=480]+bestaudio/best[height<=480]"
else:
    stringa_formato = "bestvideo[height<=360]+bestaudio/best[height<=360]"

output_placeholder = st.empty()

# 3. PULSANTE DI SCARICAMENTO DEL FILE INTERO (SENZA COSTRUTTI DI TAGLIO SPEZZONI)
if st.button("Scarica e Genera File Video Integrale 🚀"):
    output_placeholder.warning("Connessione ai server cloud e download del flusso multimediale avviato... Attendi.")
    
    session_id = str(uuid.uuid4())[:8]
    final_file = f"video_{session_id}.mp4"
    
    # Configurazione lineare delle opzioni di yt-dlp per l'unione dei flussi MP4 nativi
    ydl_opts_dl = {
        'format': stringa_formato,
        'merge_output_format': 'mp4',
        'outtmpl': f'video_{session_id}.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        # Impedisce a yt-dlp di attivare gli estrattori automatici di testo sui domini specificati
        'force_generic_extractor': True if "radioradicale" in url_selezionato else False,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts_dl) as ydl:
            ydl.download([url_selezionato])
            
        # Normalizzazione estensione in caso di formati video compositi (MKV)
        if os.path.exists(f"video_{session_id}.mp4"):
            final_file = f"video_{session_id}.mp4"
        elif os.path.exists(f"video_{session_id}.mkv"):
            os.rename(f"video_{session_id}.mkv", f"video_{session_id}.mp4")
            
        if os.path.exists(final_file) and os.path.getsize(final_file) > 0:
            output_placeholder.success("File video integrale generato con successo!")
            
            # Formattazione del nome di salvataggio pulito privo di spazi per i sistemi operativi
            nome_file_pulito = scelta_sorgente.split(' - ')[0].replace(' ', '_')
            nome_salvataggio = f"{nome_file_pulito}_Integrale.mp4"
            
            with open(final_file, "rb") as file:
                st.download_button(
                    label="⬇️ Salva il Video sul tuo Dispositivo",
                    data=file,
                    file_name=nome_salvataggio,
                    mime="video/mp4"
                )
        else:
            output_placeholder.error("Errore durante il salvataggio del file video locale sul server storage.")
            
    except Exception as e:
        output_placeholder.error(f"Errore nello scaricamento del file alla qualità selezionata. Dettaglio: {str(e)}")
        
    # Rimozione dei residui video per non esaurire lo spazio su disco del server cloud
    if os.path.exists(final_file):
        try: os.remove(final_file)
        except Exception: pass
