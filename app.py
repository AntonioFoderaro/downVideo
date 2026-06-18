import streamlit as st
import requests
import io

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Universal Video Downloader Proxy", page_icon="🎬", layout="wide")
st.title("🎬 Downloader Integrale Assemblea Nazionale (Bypass Blocco)")

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

# 1. MENU A TENDINA CON TUTTI I VIDEO INTEGRALI DELLA CONFERENZA
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
    "REGISTRAZIONE INTEGRALE - Sabato + Domenica (File Unificato Radio Radicale)": "https://radioradicale.it"
}

scelta_sorgente = st.selectbox(
    "Seleziona l'intervento o la giornata che desideri scaricare:", 
    list(dizionario_video.keys())
)
url_selezionato = dizionario_video[scelta_sorgente]

# 2. SELEZIONE DELLA QUALITÀ (ALTA O MEDIA)
st.subheader("🎬 Configurazione Risoluzione e Qualità Video")

qualita_scelta = st.selectbox(
    "Scegli il livello di qualità desiderato per il file finale:",
    ["Alta Qualità (Massima risoluzione originale)", "Media Qualità (Risoluzione standard compressed)"]
)

st.write("")
output_placeholder = st.empty()

# 3. FUNZIONE DI STREAMING CONTROLLATO IN MEMORIA VOLATILE RAM (ZERO SPAZIO DISCO)
def genera_stream_video(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    # Esegue la richiesta in modalità streaming (non scarica tutto subito)
    risposta = requests.get(url, headers=headers, stream=True)
    
    # Crea un buffer di byte dinamico in memoria RAM
    buffer_memoria = io.BytesIO()
    
    # Definizione della barra di avanzamento grafica
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    dimensione_totale = int(risposta.headers.get('content-length', 0))
    byte_scaricati = 0
    
    # Scarica a blocchi di 512 KB e trasferisce direttamente sul buffer
    for blocco in risposta.iter_content(chunk_size=512 * 1024):
        if blocco:
            buffer_memoria.write(blocco)
            byte_scaricati += len(blocco)
            if dimensione_totale > 0:
                percentuale = min(int(byte_scaricati * 100 / dimensione_totale), 100)
                progress_bar.progress(percentuale / 100)
                status_text.text(f"📥 Il server sta sbloccando e trasferendo il video: {percentuale}%")
                
    progress_bar.empty()
    status_text.empty()
    buffer_memoria.seek(0)
    return buffer_memoria.getvalue()

# 4. PULSANTE DI CONFIGURAZIONE DOWNLOAD SBLOCCATO
if st.button("Sblocca Video e Avvia Download 🚀"):
    try:
        # Il server fa da Proxy: scarica lui il file bloccato e lo impacchetta nella RAM al volo
        dati_video = genera_stream_video(url_selezionato)
        
        if dati_video and len(dati_video) > 0:
            output_placeholder.success("Sblocco completato! Clicca sul pulsante apparso qui sotto per salvare il file.")
            
            nome_file_pulito = scelta_sorgente.replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '')
            nome_salvataggio = f"{nome_file_pulito}.mp4"
            
            # Passa i byte della RAM direttamente al download button di Streamlit
            st.download_button(
                label="⬇️ Salva il Video sul tuo PC (Download Locale Sbloccato)",
                data=dati_video,
                file_name=nome_salvataggio,
                mime="video/mp4",
                use_container_width=True
            )
        else:
            output_placeholder.error("Il server ha ricevuto un file vuoto. Controlla lo stato della sorgente.")
            
    except Exception as e:
        output_placeholder.error(f"Errore durante lo sblocco del flusso video tramite proxy. Dettaglio: {str(e)}")
