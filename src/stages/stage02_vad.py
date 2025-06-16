import logging
from pathlib import Path
import soundfile as sf
import numpy as np
from silero import vad as silero_vad
from src.utils.io import write_json


def run(wav_path: Path, vad_out: Path):
    if vad_out.exists():
        logging.info(f"[02] Skipping VAD, exists: {vad_out}")
        return
    logging.info(f"[02] Running VAD on {wav_path}")
    wav, sr = sf.read(wav_path)
    speech_ts = silero_vad.get_speech_ts(
        wav,
        silero_vad.SileroVad(device='cpu'),
        sampling_rate=sr,
        min_speech_duration_ms=300,
        max_speech_duration_s=30,
    )
    result = [{'start': t['start']/sr, 'end': t['end']/sr} for t in speech_ts]
    write_json(result, vad_out)
