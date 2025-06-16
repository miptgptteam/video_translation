import logging
from pathlib import Path
from typing import List
import ctranslate2
from src.utils.io import read_jsonl, write_jsonl
from src.config import MT_MODEL, BATCH_MT


def _load_glossary(glossary_path: Path):
    glossary = {}
    if glossary_path.exists():
        with open(glossary_path, 'r', encoding='utf-8') as f:
            for line in f:
                en, ru = line.strip().split('\t')
                glossary[en] = ru
    return glossary


def run(merged_jsonl: Path, mt_out: Path, glossary_path: Path):
    if mt_out.exists():
        logging.info(f"[06] Skipping translation, exists: {mt_out}")
        return
    logging.info(f"[06] Translating {merged_jsonl}")
    translator = ctranslate2.Translator(MT_MODEL, device='cuda')
    segments = read_jsonl(merged_jsonl)
    glossary = _load_glossary(glossary_path)
    texts = [seg['text'] for seg in segments]
    results = []
    for i in range(0, len(texts), BATCH_MT):
        batch = texts[i:i+BATCH_MT]
        translations = translator.translate_batch(
            [[">>ru<<"] + t.split() for t in batch],
            beam_size=4,
            max_batch_size=BATCH_MT,
        )
        for trans in translations:
            tokens = trans.hypotheses[0]
            ru = ' '.join(tokens)
            # apply glossary substitutions
            for en, ru_term in glossary.items():
                ru = ru.replace(en, ru_term)
            results.append(ru)
    for seg, ru in zip(segments, results):
        seg['text'] = ru
    write_jsonl(segments, mt_out)
