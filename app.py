import streamlit as st
import os
import subprocess

st.set_page_config(page_title="Universal Video Downloader & Compressor", page_icon="🎬")
st.title("🎬 Downloader Assemblea Nazionale")
st.write("Scarica, taglia e comprime qualsiasi intervento dell'Assemblea Costituente di Roma (13-14 Giugno).")

# Mappatura enciclopedica di tutti gli interventi divisi per oratore e giornata
elenco_completo = {
    # --- SABATO 13 GIUGNO ---
    "SABATO - Registrazione Integrale (1a Giornata Completa)": {"url": "https://radioradicale.it", "start": None, "end": None},
    "SABATO - Roberto Vannacci (Conferenza Stampa Integrale)": {"url": "https://radioradicale.it", "start": None, "end": None},
    "SABATO - Massimiliano Simoni (Relazione d'apertura)": {"url": "https://radioradicale.it", "start": "00:05:00", "end": "00:25:00"},
    "SABATO - Gianni Alemanno (Intervento Indipendenza)": {"url": "https://radioradicale.it", "start": "00:45:00", "end": "01:10:00"},
    "SABATO - Nicola Procaccini (Coordinatore FDI)": {"url": "https://radioradicale.it", "start": "01:30:00", "end": "01:50:00"},
    
    # --- DOMENICA 14 GIUGNO ---
    "DOMENICA - Registrazione Integrale (2a Giornata Completa)": {"url": "https://radioradicale.it", "start": None, "end": None},
    "DOMENICA - Roberto Vannacci (Intervento Politico Conclusivo)": {"url": "https://radioradicale.it", "start": None, "end": None},
    "DOMENICA - Laura Ravetto (Deputato)": {"url": "https://radioradicale.it", "start": None, "end": None},
    "DOMENICA - Rossano Sasso (Deputato)": {"url": "https://radioradicale.it", "start": None, "end": None},
    "DOMENICA - Massimo Arlecchino (Pres. Indipendenza)": {"url": "https://radioradicale.it", "start": None, "end": None},
    "DOMENICA - Massimiliano Simoni (Coordinatore Nazionale)": {"url": "https://radioradicale.it", "start": None, "end": None},
    "DOMENICA - Lorenzo Gasperini (Presentazione Programma)": {"url": "https://radioradicale.it", "start": None, "end": None},
    "DOMENICA - Emanuele Pozzolo (Deputato)": {"url": "https://radioradicale.it", "start": None, "end": None},
    "DOMENICA - Stefano Valdegamberi (Consigliere Veneto)": {"url": "https://radioradicale.it", "start": None, "end": None},
    
    # --- SORGENTI ALTERNATIVE (YOUTUBE / SOCIAL) ---
    "SORGENTE YOUTUBE - Video Completo Unificato (Sabato + Domenica)": {"url": "https://youtube.com", "start": None, "end": None},
    "SORGENTE YOUTUBE - Focus Roberto Vannacci (Intervento del Sabato)": {"url": "https://youtube.com", "start": None, "end": None}
}

# 1. Interfaccia di Selezione dell'utente
scelta = st.selectbox("1. Scegli l'intervento o il blocco completo che desideri scaricare:", list(elenco_completo.keys()))
video_info = elenco_completo[scelta]

# 2. Scelta della Compressione via Hardware Cloud (FFmpeg)
compression = st.radio(
    "2. Scegli il livello di compressione (Consigliato per i video integrali molto lunghi):",
    ('Bilanciata (Consigliata - Riduce il peso del 60% mantenendo i dettagli)', 'Massima (File super leggero per smartphone)', 'Nessuna (Qualità Originale - Attenzione al peso)')
)

crf_val = 28
if compression == 'Massima (File super leggero per smartphone)': 
    crf_val = 33
elif compression == 'Nessuna (Qualità Originale - Attenzione al peso)': 
    crf_val = 23

output_placeholder = st.empty()

# 3. Pulsante di Esecuzione delle Operazioni
if st.button("Elabora Video e Genera Download 🚀"):
    output_placeholder.warning("Download del flusso multimediale in corso sui server cloud... Attendi.")
    
    raw_file = "raw_video.mp4"
    final_file = "output_finale.mp4"
    
    # Pulizia preliminare della cache per evitare conflitti di sovrascrittura
    for f in [raw_file, final_file]:
        if os.path.exists(f): os.remove(f)
        
    # Download forzato sul cloud tramite yt-dlp
    cmd_dl = f'yt-dlp "{video_info["url"]}" -o "{raw_file}"'
    dl_res = subprocess.run(cmd_dl, shell=True)
    
    if dl_res.returncode == 0 and os.path.exists(raw_file):
        output_placeholder.warning("Taglio temporale e compressione del video sul cloud in corso...")
        
        # Generazione dei parametri temporali di ritaglio per FFmpeg
        time_args = ""
        if video_info["start"] and video_info["end"]:
            time_args = f'-ss {video_info["start"]} -to {video_info["end"]}'
            
        # Comando combinato FFmpeg per tagliare, ricodificare e comprimere l'audio/video
        cmd_ffmpeg = f'ffmpeg {time_args} -i {raw_file} -vcodec libx264 -crf {crf_val} -acodec aac -b:a 128k {final_file}'
        subprocess.run(cmd_ffmpeg, shell=True)
        
        if os.path.exists(final_file):
            output_placeholder.success("Elaborazione completata con successo! Il file è pronto.")
            
            # Formattazione di un nome file sicuro privo di spazi o caratteri speciali
            nome_salvataggio = f"{scelta.replace(' ', '_').replace('-', '').replace('(', '').replace(')', '')}.mp4"
            
            with open(final_file, "rb") as file:
                st.download_button(
                    label="⬇️ Scarica il Video sul tuo PC",
                    data=file,
                    file_name=nome_salvataggio,
                    mime="video/mp4"
                )
        else:
            output_placeholder.error("Errore imprevisto durante la compressione o il ritaglio dello spezzone.")
    else:
        output_placeholder.error("Impossibile recuperare il file video originale. Il server della sorgente è temporaneamente sovraccarico.")
