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

# 1. MENU A TENDINA CON TUTTI GLI URL DEGLI INTERVENTI PRESENTI
st.subheader("🔗 Selezione Sorgente Video dell'Assemblea")

dizionario_video = {
    # --- REGISTRAZIONI INTEGRALI DELLE GIORNATE ---
    "SABATO 13 GIUGNO - Registrazione Integrale (Intero File dell'Evento)": "https://radioradicale.it",
    "DOMENICA 14 GIUGNO - Sessione Pomeridiana e Conclusioni (File Unificato)": "https://radioradicale.it",
    
    # --- INTERVENTI ED ESTRATTI SINGOLI PRESENTI ---
    "SABATO - Roberto Vannacci (Conferenza Stampa ed Apertura dei Lavori - YouTube)": "https://youtube.com",
    "DOMENICA - Roberto Vannacci (Discorso Politico Conclusivo - YouTube)": "https://youtube.com",
    "SORGENTE ALTERNATIVA - Sintesi Video e Highlights dell'Assemblea Costituente": "https://youtube.com"
}

scelta_sorgente = st.selectbox(
    "Seleziona il video o l'intervento dell'Assemblea da analizzare e scaricare:", 
    list(dizionario_video.keys())
)
url_selezionato = dizionario_video[scelta_sorgente]

# Inizializzazione degli stati della sessione Streamlit per memorizzare i dati estratti
if "info_estratte" not in st.session_state:
    st.session_state.info_estratte = None
if "url_precedente" not in st.session_state:
    st.session_state.url_precedente = ""

# Se cambia l'URL selezionato nella tendina, resetta le informazioni in cache
if url_selezionato != st.session_state.url_precedente:
    st.session_state.info_estratte = None
    st.session_state.url_precedente = url_selezionato

# 2. LETTURA DEI METADATI DEL VIDEO SELEZIONATO
if st.session_state.info_estratte is None:
    with st.spinner("🔍 Lettura delle risoluzioni e delle varianti disponibili sul server sorgente..."):
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
                info_dict = ydl.extract_info(url_selezionato, download=False)
                st.session_state.info_estratte = info_dict
        except Exception as e:
            st.error(f"❌ Impossibile leggere il flusso video del server. Dettaglio: {str(e)}")
            st.stop()

info = st.session_state.info_estratte

# Estrazione dinamica delle risoluzioni reali verticali (es. 1080, 720, 480)
formati_grezzi = info.get('formats', [])
qualita_disponibili = set()

for f in formati_grezzi:
    if f.get('height'):
        qualita_disponibili.add(f.get('height'))
        
lista_altezze_ordinate = sorted(list(qualita_disponibili), reverse=True)

# 3. COSTRUZIONE INTERFACCIA DI SELEZIONE DELLA QUALITÀ (CON ALTA E MEDIA)
st.subheader("🎬 Configurazione Risoluzione Finale")

opzioni_qualita_utente = []
mappatura_formati = {}

# Inserimento dinamico delle opzioni descrittive basate sulle altezze reali rilevate
for altezza in lista_altezze_ordinate:
    if altezza >= 1080:
        label = f"Alta Qualità ({altezza}p - Definizione Massima)"
    elif altezza >= 720:
        label = f"Media Qualità ({altezza}p - Consigliata per PC)"
    elif altezza >= 480:
        label = f"Qualità Standard ({altezza}p - Bilanciata per Smartphone)"
    else:
        label = f"Bassa Qualità ({altezza}p - File leggero)"
        
    opzioni_qualita_utente.append(label)
    mappatura_formati[label] = altezza

# Se il server non restituisce altezze esplicite (es. file MP4 statici), mette i valori di default
if not opzioni_qualita_utente:
    opzioni_qualita_utente = ["Alta Qualità (Massima originale disponibile)", "Media Qualità (Risoluzione standard compressed)"]
    mappatura_formati["Alta Qualità (Massima originale disponibile)"] = "best"
    mappatura_formati["Media Qualità (Risoluzione standard compressed)"] = "720"

qualita_scelta = st.selectbox("Scegli il livello di qualità e compressione del video:", opzioni_qualita_utente)

output_placeholder = st.empty()

# 4. PULSANTE DI ESECUZIONE DOWNLOAD DEL VIDEO INTEGRALE
if st.button("Scarica e Genera File Video Integrale 🚀"):
    output_placeholder.warning("Connessione ai server di rete e download del file integrale avviato... Attendi.")
    
    session_id = str(uuid.uuid4())[:8]
    final_file = f"video_{session_id}.mp4"
    
    # Recupero del parametro altezza associato alla scelta dell'utente
    valore_altezza = mappatura_formati[qualita_scelta]
    
    if isinstance(valore_altezza, int):
        stringa_formato = f"bestvideo[height<={valore_altezza}]+bestaudio/best[height<={valore_altezza}]"
    else:
        stringa_formato = "bestvideo+bestaudio/best" if valore_altezza == "best" else "bestvideo[height<=720]+bestaudio/best"
        
    ydl_opts_dl = {
        'format': stringa_formato,
        'merge_output_format': 'mp4',
        'outtmpl': f'video_{session_id}.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts_dl) as ydl:
            ydl.download([url_selezionato])
            
        # Verifica ed eventuale normalizzazione dell'estensione del file unito
        if os.path.exists(f"video_{session_id}.mp4"):
            final_file = f"video_{session_id}.mp4"
        elif os.path.exists(f"video_{session_id}.mkv"):
            os.rename(f"video_{session_id}.mkv", f"video_{session_id}.mp4")
            
        if os.path.exists(final_file) and os.path.getsize(final_file) > 0:
            output_placeholder.success("Il file video integrale è stato scaricato ed è pronto!")
            
            # Formattazione del nome di salvataggio pulito
            nome_file_pulito = scelta_sorgente.split(' - ')[0].replace(' ', '_')
            nome_salvataggio = f"{nome_file_pulito}_integrale.mp4"
            
            with open(final_file, "rb") as file:
                st.download_button(
                    label="⬇️ Salva il Video sul tuo Dispositivo",
                    data=file,
                    file_name=nome_salvataggio,
                    mime="video/mp4"
                )
        else:
            output_placeholder.error("Errore durante la scrittura locale del file multimediale. Spazio sul server insufficiente.")
            
    except Exception as e:
        output_placeholder.error(f"Impossibile completare il download. Errore del server sorgente: {str(e)}")
        
    # Pulizia automatica dello storage locale del server cloud per evitare saturazione
    if os.path.exists(final_file):
        try: os.remove(final_file)
        except Exception: pass

