if st.button("Elabora"):
    log = st.empty()
    log.write("Download in corso...")

    raw = "raw.mp4"
    out = "finale.mp4"

    for f in [raw, out]:
        if os.path.exists(f):
            os.remove(f)

    # DOWNLOAD
    log.write("Eseguo yt-dlp...")
    r = scarica(info["url"], raw)

    if r.returncode != 0 or not os.path.exists(raw):
        log.write("Comando eseguito:")
        log.write(str(r))
        st.error("Errore nel download.")
        st.stop()

    log.write("Download completato.")

    # CONVERSIONE
    log.write("Conversione in corso...")

    t = ""
    if info["start"] and info["end"]:
        t = f'-ss {info["start"]} -to {info["end"]}'

    cmd = f'ffmpeg -y {t} -i "{raw}" {ff} "{out}"'
    log.write("Eseguo ffmpeg:")
    log.write(cmd)

    conv = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    log.write("Output FFmpeg:")
    log.write(conv.stdout)
    log.write(conv.stderr)

    if not os.path.exists(out):
        st.error("Errore durante la conversione.")
        st.stop()

    st.success("Pronto!")

    with open(out, "rb") as f:
        st.download_button("Scarica", f, file_name="video.mp4")
