import argparse
from pathlib import Path

from metadata import SUBJECTS


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()

    root = args.root

    executable = "bash run_video.docker.sh"

    for subject in SUBJECTS:
        actions = sorted((root / subject / "Actions").glob("*"))
        for action in actions:
            videos = sorted((action / "Videos").glob("*.mp4"))
            for video in videos:
                dst_video = action / "Masks" / "SOLO" / video.name
                cmd = f"{executable} {video} {dst_video}"
                print(cmd)


if __name__ == '__main__':
    main()
