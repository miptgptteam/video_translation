import logging
from pathlib import Path
from deepmultilingualpunctuation import PunctuationModel
from src.utils.io import read_jsonl, write_jsonl

_MODEL = None


def _get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = PunctuationModel()
    return _MODEL


def run(asr_jsonl: Path, punct_out: Path):
    if punct_out.exists():
        logging.info(f"[04] Skipping punctuation, exists: {punct_out}")
        return
    logging.info(f"[04] Restoring punctuation for {asr_jsonl}")
    segments = read_jsonl(asr_jsonl)
    model = _get_model()
    for seg in segments:
        seg['text'] = model.restore_punctuation(seg['text'])
    write_jsonl(segments, punct_out)
