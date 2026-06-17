import streamlit as st
import os
import subprocess
import json

st.set_page_config(page_title="Universal Video Downloader & Compressor", page_icon="🎬")
st.title("🎬 Video Downloader & Compressor")
st.write("Scarica e comprime video da qualsiasi sito web, superando i blocchi di rete.")

# 1. Input dell'utente per l'URL
url = st.text_input("1. Incolla l'URL della pagina web o del video:", "")

if url:
    st.info("Analisi della pagina in corso... Attendi.")
    
    # Recupera le informazioni sui formati/video disponibili senza scaricare
    try:
        cmd_info = f'yt-dlp "{url}" -J'
        result = subprocess.run(cmd_info, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            video_data = json.loads(result.stdout)
            
            # Gestione playlist o video singolo
            entries = video_data.get('entries', [video_data])
            video_options = {}
            for i, entry in enumerate(entries):
                title = entry.get('title', f"Video {i+1}")
                video_options[title] = i + 1
            
            # 2. Selezione del video (se è una pagina con più video o playlist)
            selected_title = st.selectbox("2. Seleziona il video da scaricare:", list(video_options.keys()))
            item_index = video_options[selected_title]
            
            # 3. Selezione della compressione
            compression = st.radio(
                "3. Scegli il tipo di compressione:",
                ('Nessuna (Qualità Originale)', 'Bilanciata (Consigliata per PC/Smartphone)', 'Massima (File leggerissimo, ideale per condivisione)')
            )
            
            crf_val = 23
            if compression == 'Bilanciata (Consigliata per PC/Smartphone)':
                crf_val = 28
            elif compression == 'Massima (File leggerissimo, ideale per condivisione)':
                crf_val = 32

            if st.button("Avvia Elaborazione 🚀"):
                output_placeholder = st.empty()
                output_placeholder.warning("Download del video sui server cloud in corso...")
                
                # Comando di download locale sul server cloud
                out_filename = "video_originale.mp4"
                if os.path.exists(out_filename):
                    os.remove(out_filename)
                    
                cmd_dl = f'yt-dlp --playlist-items {item_index} "{url}" -o "{out_filename}"'
                dl_res = subprocess.run(cmd_dl, shell=True)
                
                if dl_res.returncode == 0 and os.path.exists(out_filename):
                    final_filename = out_filename
                    
                    # Se l'utente ha scelto di comprimere
                    if compression != 'Nessuna (Qualità Originale)':
                        output_placeholder.warning("Compressione del video in corso sul cloud... Attendi.")
                        final_filename = "video_compresso.mp4"
                        if os.path.exists(final_filename):
                            os.remove(final_filename)
                            
                        cmd_compress = f'ffmpeg -i {out_filename} -vcodec libx264 -crf {crf_val} -acodec aac -b:a 128k {final_filename}'
                        subprocess.run(cmd_compress, shell=True)
                    
                    output_placeholder.success("Elaborazione completata con successo!")
                    
                    # 4. Bottone finale di download per l'utente
                    with open(final_filename, "rb") as file:
                        st.download_button(
                            label="⬇️ Scarica il Video sul tuo PC",
                            data=file,
                            file_name=f"{selected_title.replace(' ', '_')}.mp4",
                            mime="video/mp4"
                        )
                else:
                    output_placeholder.error("Errore durante il download del video originale.")
        else:
            st.error("Impossibile analizzare l'URL. Verifica che il link sia corretto.")
            
    except Exception as e:
        st.error(f"Si è verificato un errore: {str(e)}")