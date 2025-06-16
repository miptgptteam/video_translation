from pathlib import Path

DATA_DIR = Path("data")
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
INTERM_DIR = DATA_DIR / "interm"

ASR_MODEL = "large-v3-turbo"
MT_MODEL = "ALMA-13B-ct2-int8_float16"
TTS_MODEL = "tts_models/multilingual/multi-dataset/xtts_v2"

MAX_PAR_LEN = 250
MAX_PAR_SEC = 15.0

DEVICE = "cuda"
BATCH_ASR = 16
BATCH_MT = 16
