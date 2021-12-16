import argparse
from pathlib import Path

from metadata import SUBJECTS


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()

    root = args.root

    executable = "python database_images.py"

    for subject in SUBJECTS:
        sequences = sorted((root / subject / "Sequences").glob("*"))
        for sequence in sequences:
            videos = sorted((sequence / "Videos").glob("*.mp4"))
            for video in videos:
                cmd = f"{executable} --sequence={sequence} --video_name={video.name}"
                print(cmd)


if __name__ == '__main__':
    main()
