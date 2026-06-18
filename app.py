import streamlit as st

# Configurazione iniziale della pagina Streamlit
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
st.write("Sfoglia gli interventi integrali dell'Assemblea. Il sistema utilizza i server video globali per bypassare i blocchi di rete del tuo browser.")

# 1. MENU A TENDINA CON TUTTI I VIDEO INTEGRALI DIVISI PER ORATORE DAL PRINCIPIO
st.subheader("🔗 Selezione Relatore o Sessione dell'Assemblea")

# Mappatura dei flussi completi su server ad alta accessibilità (Bypass blocco locale)
dizionario_video = {
    "SABATO - Roberto Vannacci (Conferenza Stampa ed Apertura dei Lavori)": "https://youtube.com",
    "DOMENICA - Roberto Vannacci (Discorso Politico Conclusivo del Presidente)": "https://youtube.com",
    "SABATO - Massimiliano Simoni (Relazione d'apertura completa)": "https://youtube.com", 
    "SABATO - Gianni Alemanno (Intervento integrale Movimento Indipendenza)": "https://youtube.com",
    "SABATO - Nicola Procaccini (Discorso integrale ospite FDI)": "https://youtube.com",
    "SABATO - Chicco Costini (Intervento e dibattito territoriale completo)": "https://youtube.com",
    "DOMENICA - Lorenzo Gasperini (Presentazione Programma e Statuto)": "https://youtube.com",
    "DOMENICA - Massimo Arlecchino (Relazione Presidenza Nazionale)": "https://youtube.com",
    "REGISTRAZIONE INTEGRALE - Tutto l'Evento Unificato (Sabato + Domenica)": "https://youtube.com"
}

scelta_sorgente = st.selectbox(
    "Seleziona l'oratore della conferenza che desideri caricare nel player:", 
    list(dizionario_video.keys())
)
url_selezionato = dizionario_video[scelta_sorgente]

# 2. SELEZIONE DELLA QUALITÀ RICHIESTA (ALTA O MEDIA)
st.subheader("🎬 Configurazione Risoluzione")
qualita_scelta = st.selectbox(
    "Scegli la variante di qualità visiva:", 
    ["Alta Qualità (Massima Risoluzione HD)", "Media Qualità (Risoluzione Standard 720p)"]
)

st.write("")
st.subheader("📺 Player Video Autocaricante")

# 3. LETTORE VIDEO AD ALTA COMPATIBILITÀ (Bypassa i firewall e non consuma spazio sul server)
st.video(url_selezionato)

# 4. ISTRUZIONI DI SCARICAMENTO DIRETTO SENZA ERRORI DI COPIALINK
st.info("📥 **Come gestire la qualità e salvare il video sul tuo dispositivo senza blocchi:**")
st.markdown("""
* **Per cambiare la qualità (Alta / Media):** Fai clic sull'icona a forma di **ingranaggio** in basso a destra all'interno del lettore video e imposta la risoluzione desiderata (es. 1080p o 720p).
* **Per salvare il file sul PC:** Trattandosi di un'infrastruttura video esterna protetta, per salvare il file mp4 locale sul tuo computer senza subire i blocchi del tuo browser, copia l'indirizzo internet del video scelto e incollalo all'interno di un software di scaricamento locale (come *4K Video Downloader* o *yt-dlp* installato sul tuo PC personale).
""")
