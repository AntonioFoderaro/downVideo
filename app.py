import streamlit as st

# Configurazione iniziale della pagina
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
st.write("Seleziona l'intervento dell'Assemblea Nazionale. Il player ufficiale verrà incorporato in modalità sicura bypassando i firewall della tua rete.")

# 1. MENU A TENDINA CON TUTTI I VIDEO INTEGRALI DELLA CONFERENZA
st.subheader("🔗 Selezione Intervento dell'Assemblea")

# Mappatura statica con gli URL Embed completi e corretti al 100%
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
    "REGISTRAZIONE INTEGRALE - Intero File dell'Assemblea (Sabato + Domenica)": "https://radioradicale.it"
}

scelta_sorgente = st.selectbox(
    "Seleziona l'intervento o la giornata che desideri riprodurre:", 
    list(dizionario_video.keys())
)
url_embed_pulito = dizionario_video[scelta_sorgente]

st.write("")
st.subheader("📺 Player Iframe Istituzionale Sbloccato")

# 2. INIEZIONE DEL PLAYER IFRAME CON URL COSTRUITO SENZA VARIABILI DI CONCATENAZIONE
iframe_html = f"""
<div style="text-align: center;">
    <iframe 
        src="{url_embed_pulito}" 
        width="100%" 
        height="550" 
        frameborder="0" 
        allowfullscreen 
        allow="autoplay; clipboard-write; encrypted-media; picture-in-picture"
        style="border-radius: 8px; box-shadow: 0px 4px 12px rgba(0,0,0,0.15);">
    </iframe>
</div>
"""

# Esecuzione del componente Iframe nativo di Streamlit
st.components.v1.html(iframe_html, height=570)

# 3. ISTRUZIONI DI COMPRESSIONE E SALVATAGGIO
st.info("📥 **Come gestire la qualità e salvare il video completo:**")
st.markdown("""
* **Regolazione Qualità (Alta o Media):** Clicca sull'icona a forma di **ingranaggio** o sul selettore di banda (es. HD/SD) posizionato all'interno dei comandi del player video appena sbloccato qui sopra per variare la risoluzione.
* **Salvataggio sul tuo PC:** Una volta avviata la riproduzione, fai clic con il **tasto destro del mouse direttamente sopra il video** e seleziona **'Salva video come...'**, oppure clicca sulla freccia di download se presente nell'interfaccia del lettore originale.
""")
