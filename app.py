import streamlit as st

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Archivio Assemblea Nazionale", page_icon="🎬", layout="wide")
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
st.write("Seleziona l'intervento. Il sistema utilizzerà un server di transito (Proxy) per bypassare i blocchi della tua rete.")

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
    "REGISTRAZIONE INTEGRALE - Intero File dell'Assemblea (Sabato + Domenica)": "https://radioradicale.it",
    "SABATO - Roberto Vannacci (Conferenza Stampa - YouTube)": "https://youtube.com",
    "DOMENICA - Roberto Vannacci (Discorso Conclusivo - YouTube)": "https://youtube.com"
}

scelta_sorgente = st.selectbox(
    "Scegli l'oratore o la sessione che desideri sbloccare:", 
    list(dizionario_video.keys())
)
url_video_originale = dizionario_video[scelta_sorgente]

# 2. SELEZIONE DELLA QUALITÀ (ALTA O MEDIA)
st.subheader("🎬 Configurazione Qualità")
qualita_scelta = st.selectbox(
    "Scegli la variante di risoluzione per l'apertura del file:", 
    ["Alta Qualità (Massima originale)", "Media Qualità (720p Standard)"]
)

# 3. GENERAZIONE AUTOMATICA DEL LINK DI PROXY (Bypass totale e immediato)
st.write("")
st.subheader("🚀 Pannello di Sblocco ed Apertura")
st.info("Clicca sul pulsante qui sotto: il video si aprirà attraverso un tunnel sicuro che nasconde il blocco di rete.")

# Costruiamo l'URL passando attraverso il proxy web gratuito di CroxyProxy
url_sbloccato_proxy = f"https://croxyproxy.com{url_video_originale}"

st.link_button(
    label=f"▶️ Apri e Scarica: {scelta_sorgente}",
    url=url_sbloccato_proxy,
    use_container_width=True
)

st.markdown(
    """
    ---
    💡 **Come salvare il video sul tuo computer una volta aperto:**
    1. Cliccando sul pulsante si aprirà una nuova scheda in cui il video partirà normalmente (il blocco della tua rete è rimosso) [🌐].
    2. Per salvarlo sul tuo PC, fai **click con il tasto destro del mouse al centro del video** e seleziona **'Salva video come...'**, oppure premi la combinazione di tasti **`CTRL + S`** (Windows) o **`CMD + S`** (Mac).
    """
)
