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
st.write("Seleziona l'intervento dell'Assemblea Nazionale. Il server cloud scaricherà e sbloccherà il flusso video in memoria per te.")

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
st.subheader("🚀 Scaricamento e Sblocco tramite Tunnel RAM")

# Generazione di un nome file pulito per il salvataggio locale dell'utente
nome_file_pulito = scelta_sorgente.replace(' ', '_').replace('-', '_').replace('[', '').replace(']', '')
nome_salvataggio = f"{nome_file_pulito}.mp4"

# 3. SCARICAMENTO DIRETTO NELLA RAM VOLATILE DEL SERVER (ZERO DISCO UTILIZZATO)
@st.cache_data(show_spinner=False)
def scarica_video_in_ram(url_target):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    # Il server cloud scarica i dati binari direttamente nella cache RAM volatile
    response = requests.get(url_target, headers=headers, timeout=120)
    response.raise_for_status()
    return response.content

try:
    # Pulsante o processo di attivazione dello sblocco
    if st.button("🔄 Clicca qui per sbloccare e preparare il file video"):
        with st.spinner("🔓 Il server cloud si sta collegando alla sorgente protetta... Download in RAM in corso..."):
            bytes_video = scarica_video_in_ram(url_video_originale)
        
        if bytes_video and len(bytes_video) > 0:
            st.success("🎉 Sblocco completato con successo! Il file è pronto in memoria.")
            
            # 4. BOTTONE DI DOWNLOAD REALE ACCETTA SOLO STRINGHE DI BYTES VALIDE
            st.download_button(
                label=f"⬇️ Salva il Video sul tuo PC / Smartphone",
                data=bytes_video,
                file_name=nome_salvataggio,
                mime="video/mp4",
                use_container_width=True
            )
        else:
            st.error("Il file scaricato dal server risulta vuoto (0 byte). Riprova.")

except Exception as e:
    st.error(f"Impossibile completare il tunnel di sblocco in RAM. Dettaglio: {str(e)}")
