PanopticProcessing
===
---
### Requirements

1. Install Docker and follow post-installation steps: https://docs.docker.com/engine/install/
2. Install NVIDIA Docker: https://github.com/NVIDIA/nvidia-docker
3. Install Miniconda: https://docs.conda.io/en/latest/miniconda.html
4. Set-up the following environment:
```bash
conda create -y -n processing-env python=3.9 pip
conda activate processing-env
conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
pip install lmdb tqdm cdflib
```
Note: Regarding the SOLOv2 part, if you are using a GPU (which is recommended), its CUDA Compute Capability must be >= 5.0 and <=8.0, otherwise these Docker images might not work. 

### Overview
Here's how the file structure should look like:
```
/path/to/datasets/
├─ human3.6m/
│  ├─ data/
│  │  ├─ S1/
│  │  │  ├─ Videos/
│  │  │  ├─ MyPoseFeatures/
│  │  │  │  ├─ D3_Positions/
│  │  ├─ .../
│  ├─ .../
├─ Human3.6M/
│  ├─ S1/
│  ├─ .../

/path/to/projects/
├─ Human36MProcessing/
├─ SOLOv2/

```

### 1. Clone the Side Repositories
```bash
git clone https://github.com/GuillaumeRochette/SOLOv2.git /path/to/projects/SOLOv2/
```

### 2. Download the Original Dataset
Go to the official website, register and follow the instructions: http://vision.imar.ro/human3.6m/description.php

You only need the `Videos` and the `Poses`/`D3 Positions`.
Save the files under `/path/to/datasets/human3.6m` following the hierarchy specified above.

### 3. Clean the Original Dataset
```bash
python cleanup.py --src_root=/path/to/datasets/human3.6m --dst_root=/path/to/datasets/Human3.6M
```

### 4. Run SOLOv2 for Segmentation Masks
```bash
python list_solov2.py --root=/path/to/datasets/Human3.6M > /path/to/projects/SOLOv2/list_solov2.sh
cd /path/to/projects/SOLOv2
bash list_solov2.sh
```

### 5. Download and Extract 2D Poses.
```bash
wget https://dl.fbaipublicfiles.com/video-pose-3d/data_2d_h36m_cpn_ft_h36m_dbb.npz -P data/
python extract_poses_2d.py --root=/path/to/datasets/Human3.6M --poses_2d=data/data_2d_h36m_cpn_ft_h36m_dbb.npz
```

### 6. Extract 3D Poses.
```bash
python extract_poses_3d.py --root=/path/to/datasets/Human3.6M
```

### 7. Make Databases
```bash
python list_database_images.py --root=/path/to/datasets/Human3.6M > list_database_images.sh
bash list_database_images.sh

python list_database_masks.py --root=/path/to/datasets/Human3.6M > list_database_masks.sh
bash list_database_masks.sh
 
python list_database_poses_2d.py --root=/path/to/datasets/Human3.6M > list_database_poses_2d.sh
bash list_database_poses_2d.sh

python list_database_poses_3d.py --root=/path/to/datasets/Human3.6M > list_database_poses_3d.sh
bash list_database_poses_3d.sh
```
