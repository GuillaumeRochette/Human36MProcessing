import argparse
from pathlib import Path
import shutil
import pickle
import lmdb
from time import time
from tqdm import tqdm

import numpy as np

import torch


def load(path):
    with np.load(path) as file:
        keys = file["keys"]
        values = file["values"]

    assert len(keys) == len(values)

    return keys, values


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sequence", type=Path, required=True)
    parser.add_argument("--poses_3d_name", type=str, required=True)
    args = parser.parse_args()

    sequence = args.sequence
    poses_3d_name = args.poses_3d_name

    poses_3d_path = sequence / "Poses" / "3D" / poses_3d_name

    assert poses_3d_path.exists()

    keys, values = load(poses_3d_path)
    keys = keys.tolist()
    values = [torch.tensor(value) for value in values]

    # Make temporary directories.
    tmp_dir = Path("/tmp") / f"TEMP_{time()}"
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir(parents=True)

    stem = poses_3d_name.split(".")[0]

    tmp_database = tmp_dir / f"{stem}.lmdb"

    # Remove any existing database.
    database = sequence / "Databases" / "Poses" / "3D" / f"{stem}.lmdb"
    database.parent.mkdir(parents=True, exist_ok=True)
    if database.exists():
        shutil.rmtree(database)
    print(database)

    # Create the database.
    with lmdb.open(path=f"{tmp_database}", map_size=2 ** 40) as env:
        # Add the poses to the database.
        for key, value in zip(tqdm(keys), values):
            with env.begin(write=True) as txn:
                key = pickle.dumps(key)
                value = pickle.dumps(value)
                txn.put(key=key, value=value, dupdata=False)
        # Add the keys to the database.
        with env.begin(write=True) as txn:
            key = pickle.dumps("keys")
            value = pickle.dumps(keys)
            txn.put(key=key, value=value, dupdata=False)
        # Add the protocol to the database.
        with env.begin(write=True) as txn:
            key = "protocol".encode("ascii")
            value = pickle.dumps(pickle.DEFAULT_PROTOCOL)
            txn.put(key=key, value=value, dupdata=False)

    # Move the database to its destination.
    shutil.move(f"{tmp_database}", database.parent)

    # Remove the temporary directories.
    shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    main()
