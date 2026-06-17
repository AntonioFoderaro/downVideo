import streamlit as st
import os
import subprocess

st.set_page_config(page_title="Universal Video Downloader & Compressor", page_icon="🎬")
st.title("🎬 Downloader Assemblea Nazionale")
st.write("Scarica i video delle giornate integrali o i singoli interventi dell'Assemblea Costituente di Roma.")

# Lista completa e mappata di entrambe le giornate e dei relatori
oratori = {
    "SABATO 13 GIUGNO (Prima Giornata Integrale - Apertura)": "https://radioradicale.it",
    "DOMENICA 14 GIUGNO (Seconda Giornata Integrale - Conclusioni)": "https://radioradicale.it",
    "Lorenzo Gasperini (Coordinatore Programma)": "https://radioradicale.it",
    "Roberto Vannacci (Intervento Politico)": "https://radioradicale.it",
    "Laura Ravetto (Deputato)": "https://radioradicale.it",
    "Rossano Sasso (Deputato)": "https://radioradicale.it",
    "Massimo Arlecchino (Pres. Indipendenza)": "https://radioradicale.it",
    "Massimiliano Simoni (Coordinatore Nazionale)": "https://radioradicale.it",
    "Emanuele Pozzolo (Deputato)": "https://radioradicale.it",
    "Stefano Valdegamberi (Consigliere)": "https://radioradicale.it"
}

# 1. Menu di Selezione dell'intervento o della giornata
scelta_oratore = st.selectbox("1. Cosa vuoi scaricare dell'assemblea?", list(oratori.keys()))
direct_url = oratori[scelta_oratore]

# 2. Selezione della Compressione (Fondamentale per le giornate intere da 5 ore)
compression = st.radio(
    "2. Scegli il livello di compressione (FFmpeg):",
    ('Bilanciata (Consigliata - File ridotto del 60%)', 'Massima (File super leggero)', 'Nessuna (Qualità Originale - Attenzione: File enorme)')
)

crf_val = 28
if compression == 'Massima (File super leggero)':
    crf_val = 33
elif compression == 'Nessuna (Qualità Originale - Attenzione: File enorme)':
    crf_val = 23

output_placeholder = st.empty()

# 3. Pulsante di Avvio Elaborazione
if st.button("Elabora e Genera il Download 🚀"):
    output_placeholder.warning(f"Download di '{scelta_oratore}' in corso sui server cloud... Attendi.")
    
    out_filename = "video_originale.mp4"
    if os.path.exists(out_filename): 
        os.remove(out_filename)
    
    # Download forzato sul cloud eludendo i blocchi del firewall locale
    cmd_dl = f'yt-dlp "{direct_url}" -o "{out_filename}"'
    dl_res = subprocess.run(cmd_dl, shell=True)
    
    if dl_res.returncode == 0 and os.path.exists(out_filename):
        final_filename = out_filename
        
        # Gestione della compressione video sul server tramite FFmpeg
        if compression != 'Nessuna (Qualità Originale - Attenzione: File enorme)':
            output_placeholder.warning("Compressione del video in corso sul cloud... Per i video da 5 ore l'operazione richiederà qualche minuto.")
            final_filename = "video_compresso.mp4"
            if os.path.exists(final_filename): 
                os.remove(final_filename)
                
            cmd_compress = f'ffmpeg -i {out_filename} -vcodec libx264 -crf {crf_val} -acodec aac -b:a 128k {final_filename}'
            subprocess.run(cmd_compress, shell=True)
        
        output_placeholder.success("Elaborazione completata! Il file è pronto.")
        
        # Generazione di un nome file sicuro e pulito per il PC dell'utente
        nome_pulito = scelta_oratore.replace(" ", "_").replace("(", "").replace(")", "").replace(":", "")
        nome_finale_salvataggio = f"{nome_pulito}.mp4"
        
        with open(final_filename, "rb") as file:
            st.download_button(
                label="⬇️ Scarica il Video sul tuo PC",
                data=file,
                file_name=nome_finale_salvataggio,
                mime="video/mp4"
            )
    else:
        output_placeholder.error("Errore durante l'estrazione del flusso video dai server sorgente.")
