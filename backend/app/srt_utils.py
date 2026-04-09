def generate_srt(segments):
    def format_time(seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    srt = ""

    for i, seg in enumerate(segments):
        start = format_time(seg["start"])
        end = format_time(seg["end"])
        text = seg["text"]

        srt += f"{i+1}\n{start} --> {end}\n{text}\n\n"

    return srt