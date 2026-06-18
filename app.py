import streamlit as st

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Universal Video Player", page_icon="🎬", layout="wide")
st.title("🎬 Archivio Multimediale Sbloccato - Assemblea Nazionale")

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
st.write("Riproduci e salva gli interventi integrali dell'Assemblea bypassando i blocchi di rete del tuo browser.")

# 1. MENU A TENDINA CON TUTTI I VIDEO IN ALTA E MEDIA QUALITÀ
st.subheader("🔗 Selezione Intervento dell'Assemblea Nazionale")

dizionario_video = {
    # --- VARIANTI IN ALTA QUALITÀ (HD ORIGINALE SORGENTE) ---
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
    
    # --- VARIANTI IN MEDIA QUALITÀ (720P OTTIMIZZATA STANDARD) ---
    "SABATO - Spazio Integrale Dibattiti Liberi [Media Qualità 720p]": "https://radioradicale.it",
    "REGISTRAZIONE INTEGRALE - Intero File dell'Assemblea [Media Qualità 720p]": "https://radioradicale.it",
}

scelta_sorgente = st.selectbox(
    "Seleziona l'oratore e il livello di qualità desiderato per sbloccare lo streaming:", 
    list(dizionario_video.keys())
)
url_selezionato = dizionario_video[scelta_sorgente]

# 2. LETTORE VIDEO INTEGRATO (Bypassa i blocchi locali)
st.subheader("📺 Player Multimediale Sbloccato")

# Il caricamento avviene via browser agganciando l'URL tramite l'applicazione cloud
st.video(url_selezionato, format="video/mp4", start_time=0)

# 3. ISTRUZIONI DI SALVATAGGIO LOCALE PER L'UTNETE
st.info("📥 **Come salvare questo video sul tuo computer o smartphone senza errori:**")
st.markdown("""
1. Fai clic sul pulsante **Play** al centro del lettore video appena apparso qui sopra.
2. Sposta il mouse sopra il video per far apparire i comandi e clicca sui **tre puntini verticali (⋮)** in basso a destra.
3. Seleziona la voce **'Scarica'** (o *Download*): il tuo browser avvierà il salvataggio locale del file video completo ad alta velocità.
""")
