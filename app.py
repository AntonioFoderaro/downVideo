import streamlit as st

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Universal Video Player", page_icon="🎬", layout="wide")
st.title("🎬 Archivio Nazionale Sbloccato - Assemblea Costituente")

# ==========================================
# BLOCCO DI SICUREZZA CON PASSWORD
# ==========================================
PASSWORD_CORRETTA = "Futuro2026"
password_inserita = st.text_input("Inserisci la password di sicurezza per accedere al pannello:", type="password")

if password_inserita != PASSWORD_CORRETTA:
    st.warning("🔒 Accesso limitato. Inserisci la password corretta per sbloccare le funzioni di visualizzazione.")
    st.stop()

# ==========================================
# APPLICAZIONE (ACCESSIBILE DOPO LOGIN)
# ==========================================
st.success("🔓 Accesso consentito!")
st.write("Riproduci gli interventi integrali dell'Assemblea sfruttando i server video globali ad alta compatibilità.")

# 1. MENU A TENDINA CON TUTTI GLI INTERVENTI INTEGRALI DELL'ASSEMBLEA
st.subheader("🔗 Selezione Relatore o Sessione dell'Assemblea")

# Mappatura dei video completi ospitati sulle sorgenti video ad alta compatibilità
dizionario_video = {
    "SABATO - Roberto Vannacci (Conferenza Stampa ed Apertura dei Lavori)": "https://youtube.com",
    "DOMENICA - Roberto Vannacci (Discorso Politico Conclusivo del Presidente)": "https://youtube.com",
    "SABATO - Massimiliano Simoni (Relazione d'apertura completa)": "https://youtube.com", 
    "SABATO - Gianni Alemanno (Intervento integrale Movimento Indipendenza)": "https://youtube.com",
    "SABATO - Nicola Procaccini (Discorso integrale ospite FDI)": "https://youtube.com",
    "SABATO - Chicco Costini (Intervento e dibattito territoriale completo)": "https://youtube.com",
    "DOMENICA - Lorenzo Gasperini (Presentazione Programma e Statuto)": "https://youtube.com",
    "DOMENICA - Massimo Arlecchino (Relazione Presidenza Nazionale)": "https://youtube.com",
    "REGISTRAZIONE INTEGRALE - Tutto l'Evento Unificato (Sabato + Domenica)": "https://youtube.com",
    "SORGENTE DI BACKUP - Sintesi e Highlights dell'Assemblea Costituente": "https://youtube.com"
}

scelta_sorgente = st.selectbox(
    "Seleziona l'oratore della conferenza che desideri caricare nel player:", 
    list(dizionario_video.keys())
)
url_selezionato = dizionario_video[scelta_sorgente]

st.write("")
st.subheader("📺 Player Video ad Alta Compatibilità")

# 2. LETTORE REALE COMPATIBILE CON TUTTI I FIREWALL E LE RETI
# Nota: La qualità (Alta, Media, Bassa) viene scelta direttamente dall'utente cliccando sull'icona dell'ingranaggio del player
st.video(url_selezionato)

# 3. ISTRUZIONI DI SALVATAGGIO ESTERNO SE LA RETE REGIONALE BLOCCA I DOWNLOAD
st.info("📥 **Come gestire la qualità e salvare il video sul tuo dispositivo:**")
st.markdown("""
* **Per cambiare la qualità (Alta / Media / Bassa):** Clicca sull'icona a forma di **ingranaggio** in basso a destra all'interno del riquadro del video e seleziona la risoluzione preferita (es. 1080p, 720p, 480p).
* **Per salvare il file sul PC:** Trattandosi di un flusso protetto, se desideri scaricarlo in locale per l'archivio, copia l'indirizzo del video e utilizza un software di download locale (come *4K Video Downloader* o *yt-dlp* installato sul tuo computer personale) in modo da scavalcare definitivamente i firewall aziendali o del browser cloud.
""")
