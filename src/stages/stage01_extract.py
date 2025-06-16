import logging
from pathlib import Path
import ffmpeg


def run(video: Path, audio_out: Path):
    if audio_out.exists():
        logging.info(f"[01] Skipping extraction, exists: {audio_out}")
        return
    audio_out.parent.mkdir(parents=True, exist_ok=True)
    logging.info(f"[01] Extracting audio from {video}")
    (
        ffmpeg
        .input(str(video))
        .output(str(audio_out), acodec='pcm_s16le', ac=1, ar='16k')
        .overwrite_output()
        .run(quiet=True)
    )
