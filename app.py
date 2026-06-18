import streamlit as st

# Configurazione iniziale della pagina Streamlit
st.set_page_config(page_title="Universal Video Downloader", page_icon="🎬", layout="wide")
st.title("🎬 Sblocco File Integrale Assemblea Nazionale")

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
st.write("Seleziona l'intervento dell'Assemblea Nazionale per generare la stringa di sblocco immediato.")

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
    "Seleziona l'intervento o la giornata che desideri salvare:", 
    list(dizionario_video.keys())
)
url_video_originale = dizionario_video[scelta_sorgente]

# 2. SELEZIONE FISSA DELLA QUALITÀ CON ALTA E MEDIA
st.subheader("🎬 Configurazione Qualità")
qualita_scelta = st.selectbox(
    "Scegli il livello di qualità del file finale:", 
    ["Alta Qualità (Massima originale nativa)", "Media Qualità (720p Compresso ottimizzato)"]
)

st.write("")
st.subheader("🚀 Pannello di Sblocco Comando Locale")

# Formattazione del nome file per il salvataggio
nome_file_pulito = scelta_sorgente.replace(' ', '_').replace('-', '_').replace('[', '').replace(']', '')
nome_salvataggio = f"{nome_file_pulito}.mp4"

# 3. GENERAZIONE DEL COMANDO DI SCARICAMENTO UNIVERSALE AUTOMATICO (FFMPEG NATIVO)
if "Alta" in qualita_scelta:
    comando_generato = f'ffmpeg -y -user_agent "Mozilla/5.0" -i "{url_video_originale}" -c copy {nome_salvataggio}'
else:
    comando_generato = f'ffmpeg -y -user_agent "Mozilla/5.0" -i "{url_video_originale}" -vf "scale=-2:720" -vcodec libx264 -crf 24 -acodec aac {nome_salvataggio}'

st.info("💡 **Istruzioni per scaricare il file in 5 secondi senza passare dal browser o dal server:**")
st.markdown(f"""
1. Fai clic sul pulsante in alto a destra nel riquadro grigio qui sotto per **copiare il comando preconfigurato**.
2. Apri il **Terminale** (o il *Prompt dei comandi*) sul tuo computer personale.
3. Incolla il testo copiato e premi **Invio**: il tuo PC avvierà il download diretto alla massima velocità, salvando il file video integro nella cartella corrente.
""")

# Mostra il comando pronto per essere copiato in un clic con il tasto nativo di Streamlit
st.code(comando_generato, language="bash")
