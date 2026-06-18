import streamlit as st
import requests

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Universal Video Downloader", page_icon="🎬", layout="wide")
st.title("🎬 Downloader Sbloccato - Assemblea Nazionale")

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
st.write("Seleziona l'intervento dell'Assemblea Nazionale. Il server cloud scaricherà e sbloccherà il flusso video in tempo reale per te.")

# 1. MENU A TENDINA CON TUTTI I VIDEO INTEGRALI DELLA CONFERENZA
st.subheader("🔗 Selezione Intervento dell'Assemblea")

dizionario_video = {
    "SABATO - Massimiliano Simoni [Video Integrale]": "https://radioradicale.it", 
    "SABATO - Gianni Alemanno [Video Integrale]": "https://radioradicale.it",
    "SABATO - Nicola Procaccini [Video Integrale]": "https://radioradicale.it",
    "SABATO - Chicco Costini [Video Integrale]": "https://radioradicale.it",
    "SABATO - Federica Guaiardo [Video Integrale]": "https://radioradicale.it",
    "SABATO - Spazio Integrale Dibattiti Liberi [Pomeriggio Completo]": "https://radioradicale.it",
    "DOMENICA - Lorenzo Gasperini [Video Integrale]": "https://radioradicale.it",
    "DOMENICA - Massimo Arlecchino [Video Integrale]": "https://radioradicale.it",
    "DOMENICA - Saluti Istituzionali dei Deputati [Ravetto, Sasso, Pozzolo]": "https://radioradicale.it",
    "REGISTRAZIONE INTEGRALE - Intero File dell'Assemblea (Sabato + Domenica)": "https://radioradicale.it"
}

scelta_sorgente = st.selectbox(
    "Seleziona l'intervento o la giornata che desideri sbloccare:", 
    list(dizionario_video.keys())
)
url_video_originale = dizionario_video[scelta_sorgente]

# 2. SELEZIONE FISSA DELLA QUALITÀ CON ALTA E MEDIA
st.subheader("🎬 Configurazione Qualità")
qualita_scelta = st.selectbox(
    "Scegli la variante di risoluzione per l'apertura del file:", 
    ["Alta Qualità (Massima originale)", "Media Qualità (720p Ottimizzata)"]
)

st.write("")
st.subheader("🚀 Pannello di Scaricamento Tunnel Cloud")

# Generazione di un nome file pulito per il salvataggio locale dell'utente
nome_file_pulito = scelta_sorgente.replace(' ', '_').replace('-', '_').replace('[', '').replace(']', '')
nome_salvataggio = f"{nome_file_pulito}.mp4"

# 3. CREAZIONE DELLA FUNZIONE GENERATRICE DI CHUNK (STREAM DIRETTO AL BROWSER)
def genera_video_stream(url_target):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    # Chiede al server remoto di inviare i dati in modalità streaming aperto
    with requests.get(url_target, headers=headers, stream=True) as response:
        response.raise_for_status()
        # Invia i blocchi da 1 MB ciascuno direttamente al browser dell'utente in tempo reale
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                yield chunk

# 4. BOTTONE DI DOWNLOAD DIRETTO SBLOCCATO DAL SERVER CLOUD
# Utilizzando una funzione generatrice (generator) agganciata al parametro data, 
# Streamlit non salva nulla in RAM o sul disco fisso: scarica e consegna direttamente i pacchetti al browser
st.download_button(
    label=f"⬇️ Salva il Video Integrale: {scelta_sorgente}",
    data=genera_video_stream(url_video_originale),
    file_name=nome_salvataggio,
    mime="video/mp4",
    use_container_width=True
)

st.info("💡 **Perché questo sistema funziona:** Cliccando sul pulsante sopra, il server cloud si collegherà a Radio Radicale al posto tuo e trasferirà i dati direttamente dentro la tua cartella Download, mascherando il sito bloccato dal tuo firewall.")
