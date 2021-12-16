import argparse
from pathlib import Path
import subprocess
import shutil
import pickle
import lmdb
from time import time
from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sequence", type=Path, required=True)
    parser.add_argument("--video_name", type=Path, required=True)
    args = parser.parse_args()

    sequence = args.sequence
    video_name = args.video_name
    video = sequence / "Masks" / "SOLO" / video_name

    assert video.exists()

    # Make temporary directories.
    tmp_dir = Path("/tmp") / f"TEMP_{time()}"
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    image_dir = tmp_dir / "Images"
    image_dir.mkdir(parents=True)

    # Prepare ffmpeg instructions.
    video_cmd = f"/usr/bin/ffmpeg -i {video} -q:v 1 -f image2 -start_number 0 {image_dir}/%12d.jpg"

    # Run ffmpeg.
    video_process = subprocess.run(video_cmd.split(), check=True)

    images = {int(image.stem): image for image in sorted(image_dir.glob("*.jpg"))}

    stem = video.stem

    tmp_database = tmp_dir / f"{stem}.lmdb"

    # Remove any existing database.
    database = sequence / "Databases" / "Masks" / "SOLO" / f"{stem}.lmdb"
    database.parent.mkdir(parents=True, exist_ok=True)
    if database.exists():
        shutil.rmtree(database)
    print(database)

    indexes = sorted(images.keys())

    # Create the database.
    with lmdb.open(path=f"{tmp_database}", map_size=2 ** 40) as env:
        # Add the images to the database.
        for index in tqdm(indexes):
            with env.begin(write=True) as txn:
                with images[index].open(mode="rb") as file:
                    key = pickle.dumps(index)
                    value = file.read()
                    txn.put(key=key, value=value, dupdata=False)
        # Add the keys to the database.
        with env.begin(write=True) as txn:
            key = pickle.dumps("keys")
            value = pickle.dumps(indexes)
            txn.put(key=key, value=value, dupdata=False)
        # Add the keys to the database.
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
