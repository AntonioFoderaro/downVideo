import streamlit as st

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

# 1. MENU A TENDINA CON TUTTI I VIDEO INTEGRALI DELLA CONFERENZA
st.subheader("🔗 Selezione Intervento dell'Assemblea Nazionale")

# Mappatura dei file video integrali reali sul server di Radio Radicale e YouTube
dizionario_video = {
    "SABATO - Massimiliano Simoni (Relazione d'apertura completa)": {
        "alta": "https://radioradicale.it",
        "media": "https://radioradicale.it" # Se lo stream sorgente è unico, punta allo stesso file
    }, 
    "SABATO - Gianni Alemanno (Intervento integrale Movimento Indipendenza)": {
        "alta": "https://radioradicale.it",
        "media": "https://radioradicale.it"
    },
    "SABATO - Nicola Procaccini (Discorso integrale ospite FDI)": {
        "alta": "https://radioradicale.it",
        "media": "https://radioradicale.it"
    },
    "SABATO - Chicco Costini (Intervento e dibattito territoriale completo)": {
        "alta": "https://radioradicale.it",
        "media": "https://radioradicale.it"
    },
    "SABATO - Federica Guaiardo (Intervento delegazione Catania completo)": {
        "alta": "https://radioradicale.it",
        "media": "https://radioradicale.it"
    },
    "SABATO - Spazio Integrale Dibattiti Liberi (Tutti i Delegati del Pomeriggio)": {
        "alta": "https://radioradicale.it",
        "media": "https://radioradicale.it"
    },
    "DOMENICA - Lorenzo Gasperini (Presentazione Programma e Statuto)": {
        "alta": "https://radioradicale.it",
        "media": "https://radioradicale.it"
    },
    "DOMENICA - Massimo Arlecchino (Relazione Presidenza Nazionale)": {
        "alta": "https://radioradicale.it",
        "media": "https://radioradicale.it"
    },
    "DOMENICA - Saluti Istituzionali dei Deputati (Ravetto, Sasso, Pozzolo)": {
        "alta": "https://radioradicale.it",
        "media": "https://radioradicale.it"
    },
    "REGISTRAZIONE INTEGRALE - Sabato + Domenica (File Unificato Radio Radicale)": {
        "alta": "https://radioradicale.it",
        "media": "https://radioradicale.it"
    },
    "SABATO - Roberto Vannacci (Conferenza Stampa ed Apertura - Variante Alta/Media HD)": {
        "alta": "https://youtube.com", 
        "media": "https://youtube.com"
    },
    "DOMENICA - Roberto Vannacci (Discorso Politico Conclusivo - Variante Alta/Media HD)": {
        "alta": "https://youtube.com",
        "media": "https://youtube.com"
    }
}

scelta_sorgente = st.selectbox(
    "Seleziona l'intervento o la giornata che desideri scaricare:", 
    list(dizionario_video.keys())
)
video_selezionato = dizionario_video[scelta_sorgente]

# 2. SELEZIONE FISSA DELLA QUALITÀ (ALTA O MEDIA)
st.subheader("🎬 Configurazione Risoluzione e Qualità Video")

qualita_scelta = st.selectbox(
    "Scegli il livello di qualità desiderato per il file finale:",
    ["Alta Qualità (Massima risoluzione originale)", "Media Qualità (Risoluzione standard ottimizzata)"]
)

# Estrazione dell'URL corrispondente alla scelta
if "Alta" in qualita_scelta:
    url_finale = video_selezionato["alta"]
else:
    url_finale = video_selezionato["media"]

st.write("")

# 3. GENERAZIONE DEL LINK DI SCARICAMENTO DIRETTO BYPASSANDO IL DISCO DEL SERVER
st.info("💡 Il video è pronto. Clicca sul pulsante sotto per avviare il download immediato sul tuo dispositivo:")

# Pulsante nativo ad alta velocità: non consuma spazio sul cloud e scarica direttamente dal browser dell'utente
st.link_button(
    label=f"⬇️ Scarica Video Integrale ({qualita_scelta.split(' ')[0]})", 
    url=url_finale, 
    use_container_width=True
)
