import argparse
from pathlib import Path

from metadata import SUBJECTS


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()

    root = args.root

    executable = "python database_poses_2d.py"

    for subject in SUBJECTS:
        sequences = sorted((root / subject / "Sequences").glob("*"))
        for sequence in sequences:
            poses_2ds = sorted((sequence / "Poses" / "2D" / "CPN").glob("*"))
            for poses_2d in poses_2ds:
                cmd = f"{executable} --sequence={sequence} --poses_2d_name={poses_2d.name}"
                print(cmd)


if __name__ == '__main__':
    main()
