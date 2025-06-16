import logging
from pathlib import Path
from src.utils.io import read_jsonl, write_jsonl
from src.config import MAX_PAR_LEN, MAX_PAR_SEC


def run(punct_jsonl: Path, merged_out: Path):
    if merged_out.exists():
        logging.info(f"[05] Skipping merge, exists: {merged_out}")
        return
    logging.info(f"[05] Merging segments in {punct_jsonl}")
    segments = read_jsonl(punct_jsonl)
    merged = []
    buf = []
    start = None
    for seg in segments:
        if start is None:
            start = seg['start']
        buf.append(seg)
        text_len = sum(len(s['text']) for s in buf)
        dur = seg['end'] - start
        if text_len >= MAX_PAR_LEN or dur >= MAX_PAR_SEC:
            merged.append({
                'start': start,
                'end': seg['end'],
                'text': ' '.join(s['text'] for s in buf)
            })
            buf = []
            start = None
    if buf:
        merged.append({
            'start': start,
            'end': buf[-1]['end'],
            'text': ' '.join(s['text'] for s in buf)
        })
    write_jsonl(merged, merged_out)
