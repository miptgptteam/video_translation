import logging
from pathlib import Path
from ruautopunct import RuAutoPunct
from src.utils.io import read_jsonl, write_jsonl


def run(asr_jsonl: Path, punct_out: Path):
    if punct_out.exists():
        logging.info(f"[04] Skipping punctuation, exists: {punct_out}")
        return
    logging.info(f"[04] Restoring punctuation for {asr_jsonl}")
    segments = read_jsonl(asr_jsonl)
    texts = [seg['text'] for seg in segments]
    punct = RuAutoPunct().restore_punctuations_batch(texts)
    for seg, p in zip(segments, punct):
        seg['text'] = p
    write_jsonl(segments, punct_out)
