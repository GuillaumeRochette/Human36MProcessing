import argparse
from pathlib import Path
import json

import numpy as np

from metadata import SUBJECTS


def symlink(src_path: Path, dst_path: Path):
    print(src_path, dst_path)
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    if dst_path.exists():
        dst_path.unlink()
    dst_path.symlink_to(src_path.resolve())


def cameras(src_path: Path, dst_path: Path):
    print(src_path, dst_path)
    with src_path.open() as file:
        calibration = json.load(file)

    raw_cameras = [c for c in calibration["cameras"] if c["type"] == "hd"]
    cameras = {}
    for raw_camera in raw_cameras:
        view = raw_camera["name"].replace("00_", "")

        cameras[view] = {
            "R": np.array(raw_camera["R"]).tolist(),
            "t": (np.array(raw_camera["t"]) * 1e-2).tolist(),
            "K": np.array(raw_camera["K"]).tolist(),
            "dist_coef": np.array(raw_camera["distCoef"]).tolist(),
            "resolution": np.array(raw_camera["resolution"]).tolist(),
        }

    with dst_path.open("w") as file:
        json.dump(cameras, file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src_root", type=Path, required=True)
    parser.add_argument("--dst_root", type=Path, required=True)
    args = parser.parse_args()

    src_root = args.src_root
    dst_root = args.dst_root

    for subject in SUBJECTS:
        src_subject = src_root / "data" / subject
        dst_subject = dst_root / subject

        src_videos = sorted((src_subject / "Videos").glob("*.mp4"))
        assert len(src_videos) == 128
        for src_video in src_videos:
            stem, suffix = src_video.stem, src_video.suffix
            sequence, view = stem.replace(" ", "_").split(".")

            sequence = sequence.replace("TakingPhoto", "Photo")
            sequence = sequence.replace("WalkingDog", "WalkDog")

            if subject == "S11" and sequence == "Directions":
                continue

            if "_ALL" in sequence:
                continue

            dst_video = dst_subject / "Sequences" / sequence / "Videos" / (view + suffix)

            symlink(
                src_path=src_video,
                dst_path=dst_video,
            )

        src_poses = sorted((src_subject / "MyPoseFeatures" / "D3_Positions").glob("*.cdf"))
        assert len(src_poses) == 30
        for src_pose in src_poses:
            stem, suffix = src_pose.stem, src_pose.suffix
            sequence = stem.replace(" ", "_")

            sequence = sequence.replace("TakingPhoto", "Photo")
            sequence = sequence.replace("WalkingDog", "WalkDog")

            if subject == "S11" and sequence == "Directions":
                continue

            dst_pose = dst_subject / "Sequences" / sequence / "Poses" / "3D" / ("Groundtruth" + suffix)

            symlink(
                src_path=src_pose,
                dst_path=dst_pose,
            )

        src_calibration = Path("data/calibration.json")
        with src_calibration.open() as file:
            calibration = json.load(file)

        extrinsics = calibration["extrinsics"][subject]
        intrinsics = calibration["intrinsics"]
        assert extrinsics.keys() == intrinsics.keys()

        cameras = {}
        for view in extrinsics:
            R = extrinsics[view]["R"]
            t = extrinsics[view]["t"]
            K = intrinsics[view]["calibration_matrix"]
            dist_coef = intrinsics[view]["distortion"]
            h, w = intrinsics[view]["resolution"]
            resolution = w, h

            t = np.array(t)
            t = t * 1e-3
            t = t.tolist()

            cameras[view] = {
                "R": R,
                "t": t,
                "K": K,
                "dist_coef": dist_coef,
                "resolution": resolution,
            }

        dst_calibration = dst_subject / "cameras.json"
        print(dst_calibration)
        with dst_calibration.open("w") as file:
            json.dump(cameras, file)

        sequences = sorted([x for x in (dst_subject / "Sequences").glob("*") if x.is_dir()])
        for sequence in sequences:
            symlink(
                src_path=dst_calibration,
                dst_path=sequence / "cameras.json",
            )


if __name__ == "__main__":
    main()
