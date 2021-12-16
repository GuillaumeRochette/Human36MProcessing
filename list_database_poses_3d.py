import argparse
from pathlib import Path

from metadata import SUBJECTS


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()

    root = args.root

    executable = "python database_poses_3d.py"

    for subject in SUBJECTS:
        sequences = sorted((root / subject / "Sequences").glob("*"))
        for sequence in sequences:
            poses_3d = sequence / "Poses" / "3D" / "Groundtruth.npz"
            cmd = f"{executable} --sequence={sequence} --poses_3d_name={poses_3d.name}"
            print(cmd)


if __name__ == '__main__':
    main()
