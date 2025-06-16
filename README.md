# Video Translation Pipeline

This project implements an offline English→Russian dubbing pipeline. The pipeline processes videos located under `data/input/` and writes the final Russian dubbed mp4s to `data/output/`.

## Quick Start

```bash
conda env create -f env.yml
conda activate av_translate
python main.py --save-interm
```
