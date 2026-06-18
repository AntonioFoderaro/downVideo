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

# 1. MENU A TENDINA CON FLUSSI DIRETTI COMPLETI PER EVITARE IL TRONCAMENTO DELL'URL
st.subheader("🔗 Selezione Sorgente Video dell'Assemblea")

dizionario_video = {
    # Usando il file multimediale raw diretto (.mp4) bypassiamo l'estrattore di testo di yt-dlp che causava il bug
    "REGISTRAZIONE INTEGRALE - Assemblea Costituente Nazionale (Video Completo - Radio Radicale)": "https://radioradicale.it",
    "SABATO - Roberto Vannacci (Conferenza Stampa di Apertura - YouTube)": "https://youtube.com",
    "DOMENICA - Roberto Vannacci (Discorso Politico Conclusivo - YouTube)": "https://youtube.com",
    "SORGENTE DI BACKUP - Sintesi e Highlights dell'Assemblea Costituente (YouTube)": "https://youtube.com"
}

scelta_sorgente = st.selectbox(
    "Seleziona il file video completo dell'Assemblea Nazionale da analizzare:", 
    list(dizionario_video.keys())
)
url_selezionato = dizionario_video[scelta_sorgente]

# Gestione della memoria di sessione Streamlit per evitare analisi ripetute dello stesso URL
if "info_estratte" not in st.session_state:
    st.session_state.info_estratte = None
if "url_precedente" not in st.session_state:
    st.session_state.url_precedente = ""

if url_selezionato != st.session_state.url_precedente:
    st.session_state.info_estratte = None
    st.session_state.url_precedente = url_selezionato

# 2. LETTURA DEI METADATI IN BACKGROUND CON OPZIONI DI FORZATURA GENERICA
if st.session_state.info_estratte is None:
    with st.spinner("🔍 Lettura delle risoluzioni e delle varianti disponibili sul server sorgente..."):
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'no_warnings': True,
            'extract_flat': False,
            # Forziamo yt-dlp a trattare l'URL in modo raw/generico se fallisce l'estrattore proprietario
            'force_generic_extractor': True if "radioradicale" in url_selezionato else False,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url_selezionato, download=False)
                st.session_state.info_estratte = info_dict
        except Exception as e:
            st.error(f"❌ Impossibile leggere il flusso video del server. Dettaglio: {str(e)}")
            st.stop()

info = st.session_state.info_estratte

# Estrazione delle risoluzioni reali disponibili (es. 1080, 720, 480)
formati_grezzi = info.get('formats', []) if info else []
qualita_disponibili = set()

for f in formati_grezzi:
    if f.get('height'):
        qualita_disponibili.add(f.get('height'))
        
lista_altezze_ordinate = sorted(list(qualita_disponibili), reverse=True)

# 3. INTERFACCIA DI SELEZIONE DELLA QUALITÀ CON ALTA E MEDIA IN CIMA
st.subheader("🎬 Configurazione Risoluzione e Download")

opzioni_tendina = []
mappatura_altezze = {}

# Creazione delle etichette descrittive richieste (Alta, Media, Standard, Bassa)
for altezza in lista_altezze_ordinate:
    if altezza >= 1080:
        label = f"Alta Qualità ({altezza}p - Massima Definizione)"
    elif altezza >= 720:
        label = f"Media Qualità ({altezza}p - Consigliata per PC)"
    elif altezza >= 480:
        label = f"Qualità Standard ({altezza}p - Bilanciata)"
    else:
        label = f"Bassa Qualità ({altezza}p - File leggero)"
        
    if label not in opzioni_tendina:
        opzioni_tendina.append(label)
        mappatura_altezze[label] = altezza

# Fallback di sicurezza stabile se la sorgente è un file video MP4 progressivo puro (come Radio Radicale)
if not opzioni_tendina:
    opzioni_tendina = [
        "Alta Qualità (Massima originale disponibile senza compressione)", 
        "Media Qualità (Risoluzione ottimizzata 720p compresso)"
    ]
    mappatura_altezze["Alta Qualità (Massima originale disponibile senza compressione)"] = "best"
    mappatura_altezze["Media Qualità (Risoluzione ottimizzata 720p compresso)"] = "720"

qualita_scelta = st.selectbox("Scegli il livello di qualità desiderato per il file integrale:", opzioni_tendina)

output_placeholder = st.empty()

# 4. PULSANTE DI SCARICAMENTO DEL FILE INTERO
if st.button("Scarica e Genera File Video Integrale 🚀"):
    output_placeholder.warning("Connessione ai server cloud e download del flusso multimediale avviato... Attendi.")
    
    session_id = str(uuid.uuid4())[:8]
    final_file = f"video_{session_id}.mp4"
    
    target_height = mappatura_altezze[qualita_scelta]
    
    # Generazione dei parametri di formato corretti per yt-dlp
    if isinstance(target_height, int):
        stringa_formato = f"bestvideo[height<={target_height}]+bestaudio/best[height<={target_height}]"
    elif target_height == "best":
        stringa_formato = "bestvideo+bestaudio/best"
    else:
        stringa_formato = "bestvideo[height<=720]+bestaudio/best"
        
    ydl_opts_dl = {
        'format': stringa_formato,
        'merge_output_format': 'mp4',
        'outtmpl': f'video_{session_id}.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'force_generic_extractor': True if "radioradicale" in url_selezionato else False,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts_dl) as ydl:
            ydl.download([url_selezionato])
            
        # Controllo della presenza del file finale generato sul disco del server
        if os.path.exists(f"video_{session_id}.mp4"):
            final_file = f"video_{session_id}.mp4"
        elif os.path.exists(f"video_{session_id}.mkv"):
            os.rename(f"video_{session_id}.mkv", f"video_{session_id}.mp4")
            
        if os.path.exists(final_file) and os.path.getsize(final_file) > 0:
            output_placeholder.success("File video integrale generato con successo!")
            
            # Creazione di un nome pulito per il salvataggio locale del file
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
        
    # Rimozione dei residui video per non esaurire la memoria locale
    if os.path.exists(final_file):
        try: os.remove(final_file)
        except Exception: pass
