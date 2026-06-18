import streamlit as st
import os
import subprocess
import uuid  # Genera ID univoci per evitare conflitti tra utenti

st.set_page_config(page_title="Universal Video Downloader & Compressor", page_icon="🎬")
st.title("🎬 Downloader Assemblea Nazionale")

# ==========================================
# BLOCCO DI SICUREZZA CON PASSWORD
# ==========================================
PASSWORD_CORRETTA = "Futuro2026"
password_inserita = st.text_input("Inserisci la password di sicurezza per accedere al pannello:", type="password")

if password_inserita != PASSWORD_CORRETTA:
    st.warning("🔒 Accesso limitato. Inserisci la password corretta per sbloccare le funzioni di download.")
    st.stop()

st.success("🔓 Accesso consentito!")
st.write("Scarica, taglia e comprime qualsiasi intervento dell'Assemblea Costituente di Roma (13-14 Giugno).")

# Mappatura completa (NOTA: Inserisci gli URL esatti delle pagine video, non la home generica)
elenco_completo = {
    "SABATO - Massimiliano Simoni (Relazione d'apertura)": {"url": "https://radioradicale.it...", "start": "00:05:00", "end": "00:25:00"},
    "SABATO - Gianni Alemanno (Intervento Indipendenza)": {"url": "https://radioradicale.it...", "start": "00:45:00", "end": "01:10:00"},
    "SORGENTE YOUTUBE - Video Completo Unificato": {"url": "https://youtube.com", "start": None, "end": None},
}

scelta = st.selectbox("1. Scegli l'intervento o il blocco completo che desideri scaricare:", list(elenco_completo.keys()))
video_info = elenco_completo[scelta]

compression = st.radio(
    "2. Scegli il livello di compressione:",
    ('Bilanciata (Consigliata)', 'Massima (File leggero)', 'Nessuna (Qualità Originale)')
)

crf_val = 28
if 'Massima' in compression: 
    crf_val = 33
elif 'Nessuna' in compression: 
    crf_val = 23

output_placeholder = st.empty()

if st.button("Elabora Video e Genera Download 🚀"):
    output_placeholder.warning("Download del flusso multimediale in corso... Attendi.")
    
    # 1. Rende i nomi dei file univoci usando un ID sessione (Previene crash multi-utente)
    session_id = str(uuid.uuid4())[:8]
    raw_file = f"raw_{session_id}.mp4"
    final_file = f"output_{session_id}.mp4"
    
    # 2. Comando yt-dlp ottimizzato con User-Agent per evitare i blocchi del server sorgente
    # Aggiunto anche '--no-playlist' per evitare che scarichi interi canali per errore
    cmd_dl = f'yt-dlp --no-playlist --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" "{video_info["url"]}" -o "{raw_file}"'
    
    # Esegue il download catturando l'errore per il debug
    dl_res = subprocess.run(cmd_dl, shell=True, capture_output=True, text=True)
    
    if dl_res.returncode == 0 and os.path.exists(raw_file):
        output_placeholder.warning("Taglio temporale e compressione del video in corso...")
        
        time_args = ""
        if video_info["start"] and video_info["end"]:
            time_args = f'-ss {video_info["start"]} -to {video_info["end"]}'
            
        cmd_ffmpeg = f'ffmpeg -y {time_args} -i "{raw_file}" -vcodec libx264 -crf {crf_val} -acodec aac -b:a 128k "{final_file}"'
        ffmpeg_res = subprocess.run(cmd_ffmpeg, shell=True, capture_output=True, text=True)
        
        if os.path.exists(final_file) and os.path.getsize(final_file) > 0:
            output_placeholder.success("Elaborazione completata con successo! Il file è pronto.")
            
            nome_salvataggio = f"{scelta.replace(' ', '_').replace('-', '').replace('(', '').replace(')', '')}.mp4"
            
            with open(final_file, "rb") as file:
                st.download_button(
                    label="⬇️ Scarica il Video sul tuo PC",
                    data=file,
                    file_name=nome_salvataggio,
                    mime="video/mp4"
                )
        else:
            output_placeholder.error(f"Errore FFmpeg durante il taglio: {ffmpeg_res.stderr[:200]}")
    else:
        # Mostra il vero errore restituito da yt-dlp per capire cosa fallisce
        output_placeholder.error(f"Errore nel recupero del video sorgente. Dettaglio tecnico: {dl_res.stderr[:300]}")
    
    # Pulizia finale dei file temporanei sul server per non esaurire lo spazio sul disco
    for f in [raw_file, final_file]:
        if os.path.exists(f): 
            os.remove(f)
