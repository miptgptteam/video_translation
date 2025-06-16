from pathlib import Path
import json


def read_json(path: Path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(obj, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def read_jsonl(path: Path):
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]


def write_jsonl(items, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
