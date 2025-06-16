import logging
from pathlib import Path
from src import config
from src.stages import stage01_extract, stage02_vad, stage03_asr, stage04_punct, stage05_merge, stage06_translate, stage07_tts, stage08_mux


def process_video(video: Path, save_interm: bool):
    base = video.stem
    interm_dir = config.INTERM_DIR / base
    audio = interm_dir / '01_extract.wav'
    vad = interm_dir / '02_vad.json'
    asr = interm_dir / '03_asr.jsonl'
    punct = interm_dir / '04_punct.jsonl'
    merged = interm_dir / '05_parsed.jsonl'
    mt = interm_dir / '06_ru.jsonl'
    ttswav = interm_dir / '07_tts.wav'
    final_wav = interm_dir / '08_final.wav'
    final_mp4 = config.OUTPUT_DIR / f'{base}.mp4'

    if final_mp4.exists():
        logging.info(f"[final] Skipping {video}, output exists")
        return

    stage01_extract.run(video, audio)
    stage02_vad.run(audio, vad)
    stage03_asr.run(audio, asr, config.DEVICE, config.BATCH_ASR)
    stage04_punct.run(asr, punct)
    stage05_merge.run(punct, merged)
    glossary = config.DATA_DIR / 'glossary.tsv'
    stage06_translate.run(merged, mt, glossary)
    stage07_tts.run(mt, ttswav, config.DEVICE)
    stage08_mux.run(video, ttswav, final_mp4)

    if not save_interm:
        logging.info("Cleaning intermediate files")
        for f in [audio, vad, asr, punct, merged, mt, ttswav, final_wav]:
            if f.exists():
                f.unlink()
        if interm_dir.exists() and not any(interm_dir.iterdir()):
            interm_dir.rmdir()
