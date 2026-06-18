import streamlit as st
import os
import yt_dlp
import uuid

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Universal Video Downloader Dinamico", page_icon="🎬", layout="wide")
st.title("🎬 Downloader Nazionale con Analisi Flussi")

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

# 1. INPUT DELL'URL DA PARTE DELL'UTENTE
st.subheader("🔗 Configurazione Sorgente Video")
url_utente = st.text_input(
    "Incolla qui l'URL (Radio Radicale, YouTube, ecc.) per estrarre l'elenco dei flussi:",
    placeholder="https://www.youtube.com/watch?v=... o link Radio Radicale"
)

# Inizializzazione degli stati della sessione Streamlit per memorizzare i dati estratti
if "info_estratte" not in st.session_state:
    st.session_state.info_estratte = None
if "url_precedente" not in st.session_state:
    st.session_state.url_precedente = ""

# Se l'utente cambia l'URL, resetta le informazioni memorizzate in cache
if url_utente != st.session_state.url_precedente:
    st.session_state.info_estratte = None
    st.session_state.url_precedente = url_utente

if not url_utente:
    st.info("📌 Inserisci un URL nel campo sopra per leggere l'elenco delle risoluzioni disponibili.")
    st.stop()

# 2. LETTURA DEI VIDEO E DEI FORMATI TRAMITE API PYTHON DI YT-DLP
if st.session_state.info_estratte is None:
    with st.spinner("🔍 Analisi dell'URL e lettura delle risoluzioni disponibili sul server sorgente..."):
        # Opzioni di estrazione sicura dei metadati (senza effettuare il download dei file)
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'no_warnings': True,
            'extract_flat': False,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Estrae il dizionario dei dati strutturati direttamente dal server
                info_dict = ydl.extract_info(url_utente, download=False)
                st.session_state.info_estratte = info_dict
        except Exception as e:
            st.error(f"❌ Impossibile leggere la sorgente. Verifica l'URL inserito. Dettaglio: {str(e)}")
            st.stop()

# Recupero dei dati estratti dalla memoria di sessione
info = st.session_state.info_estratte

# Gestione se l'URL è un video singolo o una Playlist di interventi
video_targets = []
if 'entries' in info:
    # È una playlist: estrae tutti i video presenti all'interno dell'elenco
    st.info(f"📂 Rilevata Playlist: **{info.get('title', 'Elenco')}** ({len(info['entries'])} video trovati)")
    for entry in info['entries']:
        if entry:
            video_targets.append({"title": entry.get("title", "Video senza titolo"), "dict": entry})
else:
    # È un video singolo
    video_targets.append({"title": info.get("title", "Video Singolo Estratto"), "dict": info})

# Mappatura dei minutaggi interni storici dell'Assemblea (Mantenuta come opzione di taglio)
elenco_oratori_tagli = {
    "SCARICA INTERVENTO INTERO (Senza tagli temporali)": {"start": None, "end": None},
    "SABATO - Massimiliano Simoni (Relazione d'apertura)": {"start": "00:01:10", "end": "00:26:40"}, 
    "SABATO - Roberto Vannacci (Conferenza Stampa ed Apertura)": {"start": "00:26:50", "end": "01:12:15"},
    "SABATO - Gianni Alemanno (Intervento integrale Indipendenza)": {"start": "01:12:30", "end": "01:40:50"},
    "SABATO - Nicola Procaccini (Discorso ospite FDI)": {"start": "01:41:00", "end": "02:04:10"},
    "SABATO - Chicco Costini (Dibattito territoriale)": {"start": "02:04:20", "end": "02:22:30"},
    "SABATO - Federica Guaiardo (Delegazione Catania)": {"start": "02:22:40", "end": "02:38:15"},
    "DOMENICA - Lorenzo Gasperini (Programma e Statuto)": {"start": "03:10:10", "end": "03:22:00"},
    "DOMENICA - Massimo Arlecchino (Relazione Presidenza)": {"start": "03:22:10", "end": "03:31:40"},
    "DOMENICA - Roberto Vannacci (Discorso Conclusivo Presidente)": {"start": "03:41:20", "end": "03:51:47"},
}

st.subheader("🎬 Selezione Video, Spezzone e Qualità Reale")
col1, col2, col3 = st.columns(3)

with col1:
    # Se ci sono più video (playlist), fa scegliere quale leggere
    lista_nomi_video = [v["title"] for v in video_targets]
    video_scelto_nome = st.selectbox("1. Seleziona il video da elaborare:", lista_nomi_video)
    idx_scelto = lista_nomi_video.index(video_scelto_nome)
    video_data_selezionato = video_targets[idx_scelto]["dict"]

with col2:
    # Menu degli oratori per applicare il corretto timestamp se applicabile al file
    oratore_scelto = st.selectbox("2. Seleziona la porzione o l'oratore:", list(elenco_oratori_tagli.keys()))
    taglio_info = elenco_oratori_tagli[oratore_scelto]

with col3:
    # ESTRAZIONE DINAMICA DELLE QUALITÀ REALI DISPONIBILI SUL SERVER PER QUEL VIDEO
    formati_grezzi = video_data_selezionato.get('formats', [])
    qualita_disponibili = set()
    
    for f in formati_grezzi:
        if f.get('height'):
            qualita_disponibili.add(f.get('height'))
            
    # Ordinamento decrescente delle risoluzioni verticali trovate (es: 1080, 720, 480, 360)
    lista_altezze_ordinate = sorted(list(qualita_disponibili), reverse=True)
    opzioni_risoluzione = [f"{h}p" for h in lista_altezze_ordinate]
    
    if not opzioni_risoluzione:
        opzioni_risoluzione = ["Migliore Qualità Automatica"]
        
    qualita_scelta = st.selectbox("3. Scegli la qualità reale rilevata sul server:", opzioni_risoluzione)

output_placeholder = st.empty()

# 4. PULSANTE DI ESECUZIONE DOWNLOAD
if st.button("Scarica e Genera File Video 🚀"):
    output_placeholder.warning("Avvio del download per la variante video e la risoluzione selezionata...")
    
    session_id = str(uuid.uuid4())[:8]
    final_file = f"video_{session_id}.mp4"
    
    # Costruzione del filtro formato di yt-dlp basato sulla scelta reale dell'utente
    if "p" in qualita_scelta:
        altezza_target = qualita_scelta.replace("p", "")
        stringa_formato = f"bestvideo[height<={altezza_target}]+bestaudio/best[height<={altezza_target}]"
    else:
        stringa_formato = "bestvideo+bestaudio/best"
        
    # Configurazione di download per catturare lo stream esatto
    url_finale_download = video_data_selezionato.get('webpage_url', url_utente)
    
    ydl_opts_dl = {
        'format': stringa_formato,
        'merge_output_format': 'mp4',
        'outtmpl': f'video_{session_id}.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }
    
    # Gestione del ritaglio temporale dell'oratore se selezionato
    if taglio_info["start"] and taglio_info["end"]:
        ydl_opts_dl['external_downloader'] = 'ffmpeg'
        ydl_opts_dl['external_downloader_args'] = {
            'ffmpeg': ['-ss', taglio_info["start"], '-to', taglio_info["end"]]
        }
        
    try:
        with yt_dlp.YoutubeDL(ydl_opts_dl) as ydl:
            ydl.download([url_finale_download])
            
        # Controllo dell'estensione effettiva generata dal merge
        if os.path.exists(f"video_{session_id}.mp4"):
            final_file = f"video_{session_id}.mp4"
        elif os.path.exists(f"video_{session_id}.mkv"):
            # Se ffmpeg impacchetta in mkv lo rinominiamo per lo smartphone dell'utente
            os.rename(f"video_{session_id}.mkv", f"video_{session_id}.mp4")
            
        if os.path.exists(final_file) and os.path.getsize(final_file) > 0:
            output_placeholder.success("Elaborazione completata! Il file è pronto alla risoluzione richiesta.")
            
            # Creazione di un nome file pulito
            nome_pulito = oratore_scelto.replace(' ', '_').replace('-', '').replace('(', '').replace(')', '')
            nome_salvataggio = f"{nome_pulito}_{qualita_scelta}.mp4"
            
            with open(final_file, "rb") as file:
                st.download_button(
                    label="⬇️ Salva il Video sul tuo Dispositivo",
                    data=file,
                    file_name=nome_salvataggio,
                    mime="video/mp4"
                )
        else:
            output_placeholder.error("Errore durante la generazione del file locale. Verifica i log del server.")
            
    except Exception as e:
        output_placeholder.error(f"Impossibile completare il download della risoluzione scelta. Dettaglio: {str(e)}")
        
    # Pulizia dello storage dei file temporanei
    if os.path.exists(final_file):
        try: os.remove(final_file)
        except Exception: pass
