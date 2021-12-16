import argparse
from pathlib import Path
import cdflib
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()

    root = Path(args.root)

    joint_indexes = [0, 1, 2, 3, 6, 7, 8, 12, 13, 14, 15, 17, 18, 19, 25, 26, 27]

    for src_poses_3d in sorted(root.rglob("*.cdf")):
        dst_poses_3d = src_poses_3d.parent / (src_poses_3d.stem + ".npz")
        print(src_poses_3d)
        print(dst_poses_3d)

        values = cdflib.CDF(path=src_poses_3d)["Pose"]
        values = values.reshape((-1, 32, 3, 1))
        values = values[:, joint_indexes, :, :]
        values = values * 1e-3
        values = values.astype(dtype=np.float32)

        n = values.shape[0]
        keys = np.arange(n)

        np.savez_compressed(dst_poses_3d, keys=keys, values=values)


if __name__ == '__main__':
    main()
