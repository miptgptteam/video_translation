
# Agent Specification: End‑to‑End English→Russian Video Dubbing Pipeline

**Goal:** Build an **offline** pipeline that converts every video in `data/input/**` into a Russian‑dubbed `.mp4` in `data/output/`, running entirely on a single NVIDIA A100 80 GB GPU.  
The agent **must not rely on any external online APIs** and should finish 15 hours of source video in ≈ 3 hours wall time.

---

## 0 · Repository Layout

```
project_root/
│
├── env.yml                 # Conda environment spec
├── README.md               # Quick‑start guide
│
├── src/
│   ├── config.py           # paths & hyper‑parameters
│   ├── pipeline.py         # high‑level orchestrator
│   ├── stages/
│   │   ├── stage01_extract.py
│   │   ├── stage02_vad.py
│   │   ├── stage03_asr.py
│   │   ├── stage04_punct.py
│   │   ├── stage05_merge.py
│   │   ├── stage06_translate.py
│   │   ├── stage07_tts.py
│   │   └── stage08_mux.py
│   │
│   └── utils/
│       ├── io.py
│       └── timecodes.py
│
└── main.py                 # CLI entry‑point
```

---

## 1 · Data Folders

```
data/
├── input/      # source videos (search recursively)
├── output/     # final Russian‑dubbed mp4
└── interm/     # optional intermediate artefacts
```

---

## 2 · Pipeline Stages

| # | Stage | Model / Library | Output artefact (when `--save-interm`) |
|--:|-------|-----------------|----------------------------------------|
| 01 | **Audio extraction** | `ffmpeg` | `01_extract.wav` |
| 02 | **Voice activity detection** | *Silero VAD* (`silero-vad`) | `02_vad.json` |
| 03 | **ASR** | *Whisper‑large‑v3‑turbo* via **faster‑whisper** (`int8_float16`) | `03_asr.jsonl` |
| 04 | **Punctuation & casing** | `deepmultilingualpunctuation` | `04_punct.jsonl` |
| 05 | **Paragraph grouping** | custom merge ≤ 250 chars **or** ≤ 15 s | `05_parsed.jsonl` |
| 06 | **Machine translation** | *ALMA‑13B‑R* via **CTranslate2** (`int8_float16`) + optional TSV glossary | `06_ru.jsonl` |
| 07 | **Text‑to‑speech** | *Coqui XTTS‑v2* (Russian female) | `07_tts.wav` |
| 08 | **Mux** (audio + video) | `ffmpeg` (`-shortest`) | `08_final.wav` (debug only) |

---

## 3 · CLI

```bash
python main.py [--save-interm]
```

* **Without** `--save-interm` no temporary files are written.  
* **With** the flag, each stage stores its artefact under  
  `data/interm/{video_basename}/{NN_stage}.{ext}`.

The pipeline must skip stages whose output file already exists (idempotency).

---

## 4 · Environment (`env.yml`)

```yaml
name: av_translate
channels:
  - defaults
dependencies:
  - python=3.10
  - pip
  - pip:
      - ffmpeg-python
      - soundfile
      - librosa
      - tqdm
      - faster-whisper==1.0.4
      - ctranslate2==4.6.0
      - sentencepiece
      - silero-vad==0.4.0
      - deepmultilingualpunctuation==1.0.1
      - tts==0.22.0           # Coqui XTTS‑v2
      - torch                 # auto‑selects correct CUDA wheel
```

---

## 5 · `config.py` (reference)

```python
from pathlib import Path

DATA_DIR   = Path("data")
INPUT_DIR  = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
INTERM_DIR = DATA_DIR / "interm"

ASR_MODEL = "large-v3-turbo"
MT_MODEL  = "ALMA-13B-ct2-int8_float16"
TTS_MODEL = "tts_models/multilingual/multi-dataset/xtts_v2"

MAX_PAR_LEN = 250       # characters
MAX_PAR_SEC = 15.0      # seconds

DEVICE    = "cuda"
BATCH_ASR = 16
BATCH_MT  = 16
```

---

## 6 · Non‑functional Requirements

1. **Idempotency**: if the final mp4 exists, skip the video; if an intermediate artefact exists (and `--save-interm` is set), skip that stage.  
2. **GPU efficiency**: batch sizes configured in `config.py`; stages must not load models onto GPU when no work is pending.  
3. **Logging**: global `logging` at INFO; DEBUG only when `--save-interm`.  
4. **Glossary**: if `data/glossary.tsv` is present, `stage06_translate` must enforce these mappings, using placeholder tokens or CTranslate2 lexicon constraints; otherwise run without error.  
5. **Timing fidelity**: final video length must match source within ±20 ms.

---

## 7 · Hints for the Agent

* **VAD**: `silero.utils.get_speech_ts(wav, model, sampling_rate, min_speech_duration_ms=300, max_speech_duration_s=30)`.  
* **ASR**: `WhisperModel.transcribe(..., word_timestamps=True, vad_filter=False)`.  
* **Punctuation**: `deepmultilingualpunctuation.PunctuationModel.restore_punctuation(text)`.
* **ALMA via CTranslate2**: pass target prefix `[">>ru<<"]`; enable `beam_size=4`, `max_batch_size` from config.  
* **XTTS‑v2** example:

  ```python
  from TTS.api import TTS
  tts = TTS(TTS_MODEL, gpu=True)
  wav = tts.tts("Пример текста", language="ru")
  ```
* **Audio alignment**: if XTTS output is shorter than the source chunk, pad with silence (`apad`) or apply `adelay` equal to segment start to preserve global timing.  
* **Mux**:  

  ```bash
  ffmpeg -i input.mp4 -i ru.wav          -c:v copy -map 0:v:0 -map 1:a:0 -shortest output.mp4
  ```

---

## 8 · Deliverables

* All Python modules fully implemented and passing `python main.py --save-interm` on sample data.  
* A concise `README.md` with the commands:

  ```bash
  conda env create -f env.yml
  conda activate av_translate
  python main.py --save-interm
  ```

* (Optional) PyTest unit tests for each stage.  

---

Good luck—implementing this spec will give you a production‑ready, GPU‑accelerated English→Russian dubbing pipeline!
