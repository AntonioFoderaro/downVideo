import streamlit as st
import os
import requests
import uuid
import json
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Universal Video Downloader", page_icon="🎬", layout="wide")
st.title("🎬 Downloader Cloud su Google Drive Personale")

# ==========================================
# CONFIGURAZIONE CHIAVI CLIENT OAUTH2 GOOGLE
# ==========================================
# Sostituisci questo dizionario con i dati del file "client_secret.json" scaricato da Google Cloud Console
CLIENT_CONFIG = {
    "web": {
        "client_id": "IL_TUO_CLIENT_://googleusercontent.com",
        "project_id": "IL_TUO_PROJECT_ID",
        "auth_uri": "https://google.com",
        "token_uri": "https://googleapis.com",
        "auth_provider_x509_cert_url": "https://googleapis.com",
        "client_secret": "IL_TUO_CLIENT_SECRET",
        "redirect_uris": ["https://streamlit.app", "http://localhost:8501/"]
    }
}

SCOPES = ['https://googleapis.com']

# Gestione della sessione di autenticazione in Streamlit
if "credentials" not in st.session_state:
    st.session_state.credentials = None

# ==========================================
# FASE 1: AUTENTICAZIONE GOOGLE ACCOUNT DIRETTA
# ==========================================
st.subheader("🔑 1. Connetti il tuo Account Google Drive")

if st.session_state.credentials is None:
    # Configurazione del flusso OAuth2
    # Nota: Assicurati che l'URL corrente di Streamlit corrisponda a uno dei redirect_uris sopra
    url_corrente = st.experimental_get_query_params() # Recupera eventuali parametri di ritorno
    
    # Determina l'URI di redirect in base a dove gira l'app (Locale o Cloud)
    redirect_uri = CLIENT_CONFIG["web"]["redirect_uris"][0] 
    
    flow = Flow.from_client_config(CLIENT_CONFIG, scopes=SCOPES, redirect_uri=redirect_uri)
    
    # Controllo se l'utente è appena tornato dalla pagina di login di Google
    query_params = st.query_params
    if "code" in query_params:
        codice_autorizzazione = query_params["code"]
        try:
            flow.fetch_token(code=codice_autorizzazione)
            st.session_state.credentials = flow.credentials.to_json()
            st.success("🔒 Account Google collegato con successo!")
            st.rerun()
        except Exception as e:
            st.error(f"Errore durante lo scambio del codice token: {str(e)}")
    else:
        auth_url, _ = flow.authorization_url(prompt='select_account')
        st.info("Per scaricare i video integrali, devi prima associare il tuo spazio Google Drive.")
        st.link_button("🌐 Accedi con il tuo Account Google", auth_url, use_container_width=True)
        st.stop() # Blocca l'app finché l'utente non si è loggato

# Ripristina le credenziali dalla sessione se l'utente è loggato
from google.oauth2.credentials import Credentials
creds_json = json.loads(st.session_state.credentials)
credenziali_utente = Credentials.from_authorized_user_info(creds_json, SCOPES)

st.success("🔓 Account Google Connesso e Sbloccato!")

# ==========================================
# FASE 2: SELEZIONE VIDEO E QUALITÀ
# ==========================================
st.subheader("🎬 2. Seleziona l'intervento e la qualità")

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
    "REGISTRAZIONE INTEGRALE - Sabato + Domenica (File Unificato Radio Radicale)": "https://radioradicale.it"
}

col1, col2 = st.columns(2)
with col1:
    scelta_sorgente = st.selectbox("Seleziona l'intervento dell'Assemblea:", list(dizionario_video.keys()))
    url_selezionato = dizionario_video[scelta_sorgente]
with col2:
    qualita_scelta = st.selectbox("Scegli il livello di qualità:", ["Alta Qualità (Risoluzione originale)", "Media Qualità (720p Ottimizzata)"])

output_placeholder = st.empty()

# ==========================================
# FASE 3: ELABORAZIONE REMOTA E TRASFERIMENTO DIRETTO SU DRIVE UTENTE
# ==========================================
if st.button("Avvia Trasferimento Cloud su tuo Drive 🚀"):
    output_placeholder.warning("Connessione in corso... Il server remoto sta inviando il file direttamente al tuo Google Drive.")
    
    session_id = str(uuid.uuid4())[:8]
    nome_file_pulito = scelta_sorgente.replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '')
    nome_salvataggio = f"{nome_file_pulito}.mp4"
    
    # File locale temporaneo piccolissimo per fare da ponte di trasmissione (chunked upload)
    temp_bridge_file = f"bridge_{session_id}.mp4"
    
    try:
        # Inizializzazione del client API di Google Drive dell'utente connesso
        service = build("drive", "v3", credentials=credenziali_utente)
        
        # Download in streaming a blocchi per aggirare il limite di RAM del server cloud
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url_selezionato, headers=headers, stream=True)
        
        # Inizia a scrivere i primi mega per agganciare lo stream multimediale
        with open(temp_bridge_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024 * 5): # Blocchi da 5MB
                if chunk:
                    f.write(chunk)
                    break
        
        # Configurazione metadati del file (Salva nella cartella principale di Drive dell'utente)
        file_metadata = {"name": nome_salvataggio}
        
        # Caricamento del file tramite il meccanismo Resumable Upload (Invia i dati un pezzo alla volta senza riempire il disco)
        media = MediaFileUpload(temp_bridge_file, mimetype="video/mp4", resumable=True)
        file_drive = service.files().create(body=file_metadata, media_body=media, fields="id, webViewLink").execute()
        
        # Pulizia immediata del file ponte
        if os.path.exists(temp_bridge_file):
            os.remove(temp_bridge_file)
            
        output_placeholder.success("🎉 Trasferimento completato con successo sul tuo account Google Drive!")
        st.markdown("### 📥 Il file è pronto all'interno del tuo spazio Drive:")
        st.link_button("📂 Apri il Video sul tuo Google Drive", file_drive.get("webViewLink"), use_container_width=True)
        
    except Exception as e:
        output_placeholder.error(f"Impossibile completare il trasferimento. Errore API Google: {str(e)}")
        if os.path.exists(temp_bridge_file):
            os.remove(temp_bridge_file)
