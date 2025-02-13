# pyre-unsafe
from opensfm import dataset
from opensfm.dataset_base import DataSetBase

import numpy as np
from pathlib import Path


def scale_to_unit_sphere(points):
    centroid = np.mean(points, axis=0)
    centered_points = points - centroid
    norms = np.linalg.norm(centered_points, axis=1, keepdims=True)
    scale = np.max(norms)
    unit_sphere_points = centered_points / scale
    return unit_sphere_points, centroid, scale


def assemble_cameras_sphere(reconstruction, centroid, scaling_factor):
    data_out = dict()
    S = np.eye(4)
    S[:3, :3] *= scaling_factor
    S[0, 3] = centroid[0]
    S[1, 3] = centroid[1]
    S[2, 3] = centroid[2]
    assert len(reconstruction.cameras) == 1, "Only one camera is supported"
    camera = next(iter(reconstruction.cameras.values()))
    K = camera.get_K_in_pixel_coordinates(camera.width, camera.height)
    for i, (shot_id, shot) in enumerate(sorted(reconstruction.shots.items())):
        P = K @ shot.pose.get_Rt()
        data_out[f'world_mat_{i}'] = P
        data_out[f'scale_mat_{i}'] = S
    return data_out


def run_dataset(data: DataSetBase) -> None:
    udata_path = Path(data.data_path) / 'undistorted'
    udataset = dataset.UndistortedDataSet(
        data,
        udata_path,
        io_handler=data.io_handler
    )
    reconstructions = udataset.load_undistorted_reconstruction()
    assert len(reconstructions) == 1, "Only one reconstruction is supported"
    points, normals, colors, labels = udataset.load_point_cloud()
    points, centroid, scale = scale_to_unit_sphere(points)
    data_out = assemble_cameras_sphere(reconstructions[0], centroid, scale)
    camera_spheres_path = udata_path / 'cameras_sphere.npz'
    np.savez(camera_spheres_path, **data_out)
    point_cloud_path = udata_path / 'points.ply'
    udataset.save_point_cloud(
        points,
        normals,
        colors,
        labels,
        filename=point_cloud_path
    )
