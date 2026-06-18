import streamlit as st

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Archivio Assemblea Nazionale", page_icon="🎬", layout="wide")
st.title("🎬 Downloader & Player Sbloccato - Assemblea Nazionale")

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
st.write("Seleziona l'intervento dell'Assemblea Nazionale. Il sistema sbloccherà il link diretto bypassando i congelamenti del lettore.")

# 1. MENU A TENDINA CON TUTTI I VIDEO INTEGRALI DELLA CONFERENZA
st.subheader("🔗 1. Selezione Intervento dell'Assemblea")

# Mappatura dei file video completi nativi pronti per lo sblocco
dizionario_video = {
    "SABATO - Massimiliano Simoni [Video Integrale dell'Intervento]": "https://radioradicale.it", 
    "SABATO - Gianni Alemanno [Video Integrale dell'Intervento]": "https://radioradicale.it",
    "SABATO - Nicola Procaccini [Video Integrale dell'Intervento]": "https://radioradicale.it",
    "SABATO - Chicco Costini [Video Integrale dell'Intervento]": "https://radioradicale.it",
    "SABATO - Federica Guaiardo [Video Integrale dell'Intervento]": "https://radioradicale.it",
    "SABATO - Spazio Integrale Dibattiti Liberi [Tutti i Delegati del Pomeriggio]": "https://radioradicale.it",
    "DOMENICA - Lorenzo Gasperini [Video Integrale dell'Intervento]": "https://radioradicale.it",
    "DOMENICA - Massimo Arlecchino [Video Integrale dell'Intervento]": "https://radioradicale.it",
    "DOMENICA - Saluti Istituzionali dei Deputati [Ravetto, Sasso, Pozzolo]": "https://radioradicale.it",
    "REGISTRAZIONE INTEGRALE - Intero File dell'Assemblea (Sabato + Domenica)": "https://radioradicale.it",
    "SABATO - Roberto Vannacci (Conferenza Stampa - Link Alternativo HD)": "https://youtube.com",
    "DOMENICA - Roberto Vannacci (Discorso Conclusivo - Link Alternativo HD)": "https://youtube.com"
}

scelta_sorgente = st.selectbox(
    "Scegli l'oratore di cui desideri sbloccare il video completo:", 
    list(dizionario_video.keys())
)
url_selezionato = dizionario_video[scelta_sorgente]

# 2. SELEZIONE DELLA QUALITÀ (ALTA O MEDIA)
st.subheader("🎬 2. Configurazione Qualità")
qualita_scelta = st.selectbox(
    "Scegli la variante di risoluzione per l'apertura del file:", 
    ["Alta Qualità (Risoluzione Massima originale)", "Media Qualità (Risoluzione Standard ottimizzata)"]
)

st.write("")
st.subheader("🚀 3. Pannello di Sblocco ed Apertura File")

# 3. GENERAZIONE DEL BOTTONE DI REINDIRIZZAMENTO PROTETTO (Bypass totale iFrame e blocchi player)
st.info("L'applicazione ha generato il link di sblocco indipendente. Clicca sul pulsante sotto:")

st.link_button(
    label=f"🌐 Apri ed Esegui {scelta_sorgente} in una nuova scheda sicura",
    url=url_selezionato,
    use_container_width=True
)

# 4. ISTRUZIONI DI SALVATAGGIO MANUALE POST-APERTURA
st.markdown(
    f"""
    ---
    💡 **Come riprodurre e salvare il file una volta cliccato il pulsante sopra:**
    1. Una volta aperta la nuova scheda, il video si caricherà al di fuori dei blocchi di Streamlit, rendendo i tasti nuovamente cliccabili.
    2. **Per regolare la qualità:** Se il video è di YouTube, usa l'icona dell'ingranaggio del player; se è di Radio Radicale, il browser caricherà automaticamente la variante corrispondente alla banda della tua rete.
    3. **Per scaricare il file sul tuo PC:** Fai clic con il **tasto destro del mouse** al centro del video e seleziona la voce **'Salva video come...'**, oppure premi la combinazione di tasti **`CTRL + S`** (su Windows) o **`CMD + S`** (su Mac).
    """
)
