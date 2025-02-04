import os

import numpy as np
from pathlib import Path
from scipy.spatial.transform import Rotation

from opensfm.dataset import DataSet
from opensfm.transformations import quaternion_from_matrix
from opensfm.align import apply_similarity


def run_dataset(data: DataSet) -> None:
    """Export the reconstruction to OnePose format"""
    reconstructions = data.load_reconstruction()
    tracks_manager = data.load_tracks_manager()
    if not reconstructions:
        return
    for rcn in reconstructions:
        b = np.array([0.0, 0.0, 0.0])
        A = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]])
        apply_similarity(rcn, 1.0, A, b)
        A = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, -1.0]])
        apply_similarity(rcn, 1.0, A, b)
        data.save_ply(rcn, tracks_manager, no_cameras=True)

    frames_strs = []
    poses_strs = []
    cameras = [camera for rcn in reconstructions for camera in rcn.cameras.values()]
    camera = cameras[0]
    fx = camera.focal * max(camera.width, camera.height)
    cx = (camera.width + 1) / 2.0
    cy = (camera.height + 1) / 2.0
    shots = [shot for rcn in reconstructions for shot in rcn.shots.values()]
    sorted_shots = sorted(shots, key=lambda shot: shot.id)
    for shot in sorted_shots:
        pos = shot.pose.get_origin()
        idx = Path(shot.id).stem
        frame_idx = int(idx)
        pos_str = ','.join([str(v) for v in pos])
        r = Rotation.from_matrix(shot.pose.get_R_cam_to_world())
        angles = r.as_euler('xyz')
        r = Rotation.from_euler('xyz', [angles[0] + np.pi, angles[1], angles[2]])
        quat_wxyz = quaternion_from_matrix(r.as_matrix())
        quat_str = ','.join([str(v) for v in quat_wxyz])
        pose_str = f"{idx},{pos_str},{quat_str}"
        poses_strs.append(pose_str)
        frame_str = f"{idx},{frame_idx},{fx},{fx},{cx},{cy}"
        frames_strs.append(frame_str)
    arposes_filepath = os.path.join(data.data_path, "ARposes.txt")
    with open(arposes_filepath, 'w', encoding="utf-8") as file:
        file.write('\n'.join(poses_strs))
    frames_filepath = os.path.join(data.data_path, "Frames.txt")
    with open(frames_filepath, 'w', encoding="utf-8") as file:
        file.write('\n'.join(frames_strs))
