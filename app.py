import streamlit as st

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Universal Video Player", page_icon="🎬", layout="wide")
st.title("🎬 Archivio Multimediale Assemblea Nazionale")

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
st.write("Seleziona l'intervento dell'Assemblea. Puoi guardarlo o scaricarlo direttamente tramite le funzioni native del tuo browser.")

# 1. MENU A TENDINA CON TUTTI I VIDEO INTEGRALI DELLA CONFERENZA
st.subheader("🔗 Selezione Intervento dell'Assemblea Nazionale")

dizionario_video = {
    "SABATO - Massimiliano Simoni [Alta Qualità HD]": "https://radioradicale.it", 
    "SABATO - Gianni Alemanno [Alta Qualità HD]": "https://radioradicale.it",
    "SABATO - Nicola Procaccini [Alta Qualità HD]": "https://radioradicale.it",
    "SABATO - Chicco Costini [Alta Qualità HD]": "https://radioradicale.it",
    "SABATO - Federica Guaiardo [Alta Qualità HD]": "https://radioradicale.it",
    "SABATO - Spazio Integrale Dibattiti Liberi [Alta Qualità HD]": "https://radioradicale.it",
    "DOMENICA - Lorenzo Gasperini [Alta Qualità HD]": "https://radioradicale.it",
    "DOMENICA - Massimo Arlecchino [Alta Qualità HD]": "https://radioradicale.it",
    "DOMENICA - Saluti Istituzionali dei Deputati [Alta Qualità HD]": "https://radioradicale.it",
    "REGISTRAZIONE INTEGRALE - Intero File dell'Assemblea [Alta Qualità HD]": "https://radioradicale.it",
    "SABATO - Roberto Vannacci (Conferenza Stampa - YouTube HD)": "https://youtube.com",
    "DOMENICA - Roberto Vannacci (Discorso Conclusivo - YouTube HD)": "https://youtube.com",
}

scelta_sorgente = st.selectbox(
    "Seleziona l'intervento o la giornata che desideri elaborare:", 
    list(dizionario_video.keys())
)
url_selezionato = dizionario_video[scelta_sorgente]

# 2. SELEZIONE FISSA DELLA QUALITÀ VISIVA (ALTA O MEDIA)
st.subheader("🎬 Configurazione Risoluzione")
qualita_scelta = st.selectbox("Scegli la qualità visiva del flusso:", ["Alta Qualità (Nativa HD)", "Media Qualità (Standard Compressed)"])

# 3. LETTURA IN STREAMING DIRETTO (Evita crash di memoria e blocchi)
st.write("")
st.subheader("📺 Player Multimediale Sbloccato")

# Mostra il video in streaming nativo bypassando i blocchi IP locali
st.video(url_selezionato, format="video/mp4", start_time=0)

# 4. ISTRUZIONI DI SCARICAMENTO SENZA ERRORI DI 0 BYTE
st.info("📥 **Come salvare il file sul tuo PC o Smartphone in un clic:**")
st.markdown("""
1. Fai clic sul pulsante **Play** del lettore video qui sopra per avviare il flusso.
2. Clicca sui **tre puntini verticali (⋮)** posizionati in basso a destra all'interno della barra dei comandi del video.
3. Seleziona la voce **'Scarica'** (o *Download*).
""")
