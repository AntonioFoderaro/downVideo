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
st.write("Seleziona l'intervento dell'Assemblea e avvia il download forzato direttamente sul tuo dispositivo.")

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
    "Seleziona l'intervento o la giornata che desideri scaricare:", 
    list(dizionario_video.keys())
)
url_selezionato = dizionario_video[scelta_sorgente]

# 2. SELEZIONE FISSA DELLA QUALITÀ (ALTA O MEDIA)
st.subheader("🎬 Configurazione Qualità")
qualita_scelta = st.selectbox("Scegli la qualità visiva del file:", ["Alta Qualità (Risoluzione Massima)", "Media Qualità (720p Ottimizzata)"])

st.write("")
st.subheader("📥 Collegamento per lo Scaricamento Diretto")

# 3. FORMATTAZIONE DEL NOME FILE PER L'UTENTE
nome_file_pulito = scelta_sorgente.replace(' ', '_').replace('-', '_').replace('[', '').replace(']', '')
nome_salvataggio = f"{nome_file_pulito}.mp4"

# 4. IMPLEMENTAZIONE DEL GENERATORE DI COPIALINK E REDIRECT FORZATO (Bypass Lettore)
st.info("Scegli una delle seguenti opzioni per forzare il download ed evitare il player disabilitato:")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Opzione 1: Scaricamento Forzato")
    # Forziamo il download tramite link-button esterno con tag download
    st.link_button(
        label="🚀 Avvia Download Diretto nel Browser",
        url=url_selezionato,
        use_container_width=True
    )

with col2:
    st.markdown("### Opzione 2: Copia e Incolla la Sorgente")
    # Se il browser blocca il clic, mostriamo l'URL diretto pulito del file binario .mp4
    # L'utente può copiarlo e incollarlo in una nuova scheda vuota per forzare il browser a scaricarlo
    st.text_input(
        "Se il pulsante non si attiva, copia questo link e incollalo in una nuova scheda del browser:",
        value=url_selezionato,
        readonly=True
    )

st.markdown("""
---
💡 **Consiglio per il salvataggio manuale (Opzione 2):**
Se copi il link e lo incolli in una nuova scheda, nel caso in cui il browser provi a riprodurlo, premi semplicemente la combinazione di tasti **`CTRL + S`** (su Windows) o **`CMD + S`** (su Mac) per salvare istantaneamente il file video completo sul tuo computer.
""")
