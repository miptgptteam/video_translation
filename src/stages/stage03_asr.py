import logging
from pathlib import Path
from faster_whisper import WhisperModel
from src.utils.io import write_jsonl


def run(wav_path: Path, asr_out: Path, device: str, batch_size: int):
    if asr_out.exists():
        logging.info(f"[03] Skipping ASR, exists: {asr_out}")
        return
    logging.info(f"[03] Running ASR on {wav_path}")
    model = WhisperModel("large-v3-turbo", device=device, compute_type="float16")
    segments, _ = model.transcribe(str(wav_path), batch_size=batch_size, word_timestamps=True, vad_filter=False)
    results = []
    for seg in segments:
        results.append({
            'start': seg.start,
            'end': seg.end,
            'text': seg.text.strip()
        })
    write_jsonl(results, asr_out)
