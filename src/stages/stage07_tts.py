import logging
from pathlib import Path
from TTS.api import TTS
from src.config import TTS_MODEL
import numpy as np
from src.utils.io import read_jsonl
import soundfile as sf


def run(mt_jsonl: Path, wav_out: Path, device: str):
    if wav_out.exists():
        logging.info(f"[07] Skipping TTS, exists: {wav_out}")
        return
    logging.info(f"[07] Synthesizing speech for {mt_jsonl}")
    segments = read_jsonl(mt_jsonl)
    tts = TTS(TTS_MODEL, gpu=device.startswith('cuda'))
    waves = []
    for seg in segments:
        wav = tts.tts(seg['text'], language='ru')
        waves.append(wav)
    audio = np.concatenate(waves)
    wav_out.parent.mkdir(parents=True, exist_ok=True)
    sf.write(wav_out, audio, 22050)
