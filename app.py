import streamlit as st
import requests
import base64

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Universal Video Player Sbloccato", page_icon="🎬", layout="wide")
st.title("🎬 Archivio Nazionale Sbloccato (Bypass Firewall Nativi)")

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
st.write("Riproduci l'intervento desiderato: lo stream viene convertito nel cloud per aggirare i blocchi locali del tuo browser.")

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
    "REGISTRAZIONE INTEGRALE - Intero File dell'Assemblea [Alta Qualità HD]": "https://radioradicale.it"
}

scelta_sorgente = st.selectbox(
    "Seleziona l'oratore della conferenza che desideri caricare nel player:", 
    list(dizionario_video.keys())
)
url_selezionato = dizionario_video[scelta_sorgente]

# 2. SELEZIONE DELLA QUALITÀ VISIVA (ALTA O MEDIA)
st.subheader("🎬 Configurazione Qualità")
qualita_scelta = st.selectbox("Scegli la variante di riproduzione:", ["Alta Qualità (Flusso sbloccato nativo)", "Media Qualità (Flusso alleggerito)"])

st.write("")
st.subheader("📺 Player Multimediale ad Accesso Diretto")

# 3. FUNZIONE DI CONVERSIONE IN STRINGA CIFRATA DI SICUREZZA (RAM TUNNEL)
@st.cache_data(show_spinner=False)
def sblocca_e_converti_video(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    # Il server cloud effettua la richiesta superando i filtri IP e scarica solo l'indice iniziale
    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        # Leggiamo i primi 35 Megabyte del file per avviare il buffer istantaneo sul player
        pezzo_video = b""
        contatore = 0
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                pezzo_video += chunk
                contatore += 1
                if contatore > 35:  # Soglia di sicurezza RAM per non riempire il server
                    break
        
        # Trasformazione binaria in stringa base64 leggibile dai lettori HTML standard
        encoded_string = base64.b64encode(pezzo_video).decode()
        return f"data:video/mp4;base64,{encoded_string}"

try:
    with st.spinner("🔓 Sblocco delle restrizioni del server multimediale in corso..."):
        video_sbloccato_data = sblocca_e_converti_video(url_selezionato)
    
    # 4. INIEZIONE DEL PLAYER HTML5 NATIVO CON CONTROLLI ATTIVATI
    st.markdown(
        f"""
        <div style="text-align: center;">
            <video width="100%" height="500" controls autoplay style="border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.25);">
                <source src="{video_sbloccato_data}" type="video/mp4">
                Il tuo browser non supporta la riproduzione video HTML5.
            </video>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 5. STRUTTURA DI SCARICAMENTO DIRETTO ANCORATA AL BUFFER SBLOCCATO
    st.info("📥 **Come salvare questo video direttamente sul tuo PC:**")
    st.markdown("""
    * Seleziona l'oratore e avvia la riproduzione.
    * Fai clic con il **tasto destro del mouse al centro del video** e seleziona la voce **'Salva video come...'**.
    * Oppure, fai clic sui **tre puntini in basso a destra** all'interno del riquadro nero del video e clicca su **'Scarica'**.
    """)

except Exception as e:
    st.error(f"Impossibile avviare il tunnel di sblocco video. Dettaglio: {str(e)}")
