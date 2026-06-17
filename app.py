import streamlit as st
import os
import subprocess
import json

st.set_page_config(page_title="Universal Video Downloader & Compressor", page_icon="🎬")
st.title("🎬 Video Downloader & Compressor")
st.write("Scarica e comprime video da qualsiasi sito web, superando i blocchi di rete.")

# Input principale per l'URL della pagina
url = st.text_input("1. Incolla l'URL della pagina web o del video:", "")

if url:
    # Selezione universale della compressione
    compression = st.radio(
        "2. Scegli il tipo di compressione:",
        ('Nessuna (Qualità Originale)', 'Bilanciata (Consigliata per PC/Smartphone)', 'Massima (File leggerissimo)')
    )
    
    crf_val = 23
    if compression == 'Bilanciata (Consigliata per PC/Smartphone)':
        crf_val = 28
    elif compression == 'Massima (File leggerissimo)':
        crf_val = 32

    output_placeholder = st.empty()
    
    # Tentativo di estrazione automatica delle informazioni
    cmd_info = f'yt-dlp "{url}" -J'
    result = subprocess.run(cmd_info, shell=True, capture_output=True, text=True)
    
    # CASO A: Il sito viene analizzato correttamente
    if result.returncode == 0:
        try:
            video_data = json.loads(result.stdout)
            entries = video_data.get('entries', [video_data])
            video_options = {entry.get('title', f"Video {i+1}"): i + 1 for i, entry in enumerate(entries)}
            
            selected_title = st.selectbox("Seleziona il video specifico trovato nella pagina:", list(video_options.keys()))
            item_index = video_options[selected_title]
            
            if st.button("Avvia Download e Compressione 🚀"):
                output_placeholder.warning("Download in corso sui server cloud...")
                out_filename = "video_originale.mp4"
                if os.path.exists(out_filename): os.remove(out_filename)
                
                cmd_dl = f'yt-dlp --playlist-items {item_index} "{url}" -o "{out_filename}"'
                dl_res = subprocess.run(cmd_dl, shell=True)
                
                if dl_res.returncode == 0 and os.path.exists(out_filename):
                    final_filename = out_filename
                    if compression != 'Nessuna (Qualità Originale)':
                        output_placeholder.warning("Compressione in corso sul cloud... Attendi.")
                        final_filename = "video_compresso.mp4"
                        if os.path.exists(final_filename): os.remove(final_filename)
                        cmd_compress = f'ffmpeg -i {out_filename} -vcodec libx264 -crf {crf_val} -acodec aac -b:a 128k {final_filename}'
                        subprocess.run(cmd_compress, shell=True)
                    
                    output_placeholder.success("Pronto!")
                    with open(final_filename, "rb") as file:
                        st.download_button(label="⬇️ Scarica il Video sul tuo PC", data=file, file_name="video_finale.mp4", mime="video/mp4")
        except:
            st.error("Errore di lettura dati.")
            
    # CASO B: Il sito blocca l'analisi automatica (Es. Radio Radicale) -> Attiva la modalità forzata
    else:
        st.warning("⚠️ Questa specifica pagina richiede il Download Forzato. Usa il link video diretto.")
        direct_url = st.text_input("Inserisci l'URL diretto del file MP4/M3U8 (per Gasperini inserisci quello fornito):", "https://radioradicale.it")
        
        if st.button("Avvia Download Forzato 🚀"):
            output_placeholder.warning("Download forzato dal server cloud in corso...")
            out_filename = "video_originale.mp4"
            if os.path.exists(out_filename): os.remove(out_filename)
            
            # Scarica direttamente senza analizzare la pagina web
            cmd_dl = f'yt-dlp "{direct_url}" -o "{out_filename}"'
            dl_res = subprocess.run(cmd_dl, shell=True)
            
            if dl_res.returncode == 0 and os.path.exists(out_filename):
                final_filename = out_filename
                if compression != 'Nessuna (Qualità Originale)':
                    output_placeholder.warning("Compressione del video in corso sul cloud... Attendi.")
                    final_filename = "video_compresso.mp4"
                    if os.path.exists(final_filename): os.remove(final_filename)
                    cmd_compress = f'ffmpeg -i {out_filename} -vcodec libx264 -crf {crf_val} -acodec aac -b:a 128k {final_filename}'
                    subprocess.run(cmd_compress, shell=True)
                
                output_placeholder.success("Elaborazione completata!")
                with open(final_filename, "rb") as file:
                    st.download_button(label="⬇️ Scarica il Video sul tuo PC", data=file, file_name="intervento_gasperini_compresso.mp4", mime="video/mp4")
            else:
                output_placeholder.error("Errore nel download forzato. Il link del server potrebbe essere cambiato.")
