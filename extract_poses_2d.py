import argparse
from pathlib import Path
import numpy as np

from metadata import SUBJECTS, VIEWS


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--poses_2d", type=Path, required=True)
    args = parser.parse_args()

    poses_2d = args.poses_2d
    root = args.root

    with np.load(poses_2d, allow_pickle=True) as file:
        data = file["positions_2d"].item()

    for subject in SUBJECTS:
        for sequence in data[subject]:
            for i, values in enumerate(data[subject][sequence]):
                sequence = sequence.replace(" ", "_")
                view = VIEWS[i]
                dst_poses_2d = root / subject / "Sequences" / sequence / "Poses" / "2D" / "CPN" / f"{view}.npz"
                if not dst_poses_2d.parent.exists():
                    dst_poses_2d.parent.mkdir(parents=True)
                print(dst_poses_2d)

                n, j, d = values.shape
                values = values.reshape((n, j, d, 1))
                values = values.astype(dtype=np.float32)
                keys = np.arange(n)

                np.savez_compressed(dst_poses_2d, keys=keys, values=values)


if __name__ == "__main__":
    main()
