if st.button("Elabora"):

    progress = st.progress(0)
    status = st.empty()

    # 0–10% Preparazione
    progress.progress(5)
    status.write("🔧 Preparazione...")

    raw = "raw.mp4"
    out = "finale.mp4"

    for f in [raw, out]:
        if os.path.exists(f):
            os.remove(f)

    time.sleep(0.5)
    progress.progress(10)

    # 10–40% Download
    status.write("⬇️ Download in corso...")
    r = scarica(info["url"], raw)

    if r.returncode != 0 or not os.path.exists(raw):
        progress.progress(100)
        status.error("❌ Errore download. Possibile blocco firewall o server lento.")
        st.stop()

    progress.progress(40)

    # 40–90% Conversione
    status.write("🎞️ Conversione in corso...")

    t = ""
    if info["start"] and info["end"]:
        t = f'-ss {info["start"]} -to {info["end"]}'

    cmd = f'ffmpeg -y {t} -i "{raw}" {ff} "{out}"'
    conv = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if conv.returncode != 0 or not os.path.exists(out):
        progress.progress(100)
        status.error("❌ Errore conversione.")
        st.stop()

    progress.progress(90)

    # 90–100% Finalizzazione
    status.write("📦 Preparazione download...")
    time.sleep(0.5)
    progress.progress(100)

    st.success("✅ Pronto!")

    with open(out, "rb") as f:
        st.download_button("Scarica", f, file_name="video.mp4")
