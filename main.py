import argparse
import logging
from pathlib import Path
from src import config
from src.pipeline import process_video


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


def find_videos(directory: Path):
    for ext in ('*.mp4', '*.mkv', '*.mov', '*.avi'):
        for path in directory.rglob(ext):
            yield path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--save-interm', action='store_true', help='keep intermediate files')
    args = parser.parse_args()

    videos = list(find_videos(config.INPUT_DIR))
    if not videos:
        logging.info('No input videos found')
        return

    for video in videos:
        process_video(video, args.save_interm)


if __name__ == '__main__':
    main()
