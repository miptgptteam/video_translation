import logging
from pathlib import Path
import subprocess


def run(video: Path, wav_path: Path, final_out: Path):
    if final_out.exists():
        logging.info(f"[08] Skipping mux, exists: {final_out}")
        return
    logging.info(f"[08] Muxing {video} + {wav_path}")
    final_out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        'ffmpeg', '-i', str(video), '-i', str(wav_path),
        '-c:v', 'copy', '-map', '0:v:0', '-map', '1:a:0', '-shortest', str(final_out)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
