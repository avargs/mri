import sys
import json

import numpy as np
import nibabel as nib


def load_matrix_from_nifti_file(nifti_file_path):
    nifti_data = nib.load(nifti_file_path)
    nifti_matrix = np.array(nifti_data.dataobj, dtype='float')

    return nifti_matrix


def load_data(prefix):
    # Store 3d images in a list and reading the json files to create a EchoTime vector
    suffixes = ['0224-1', '0448-2', '0672-3', '0896-4', '1120-5', '1344-6', '1568-7', '1792-8']

    list_mri = []
    te_matrix_list = np.empty([8, 1], dtype=float)

    for i in range(len(suffixes)):
        path_nii = prefix + suffixes[i] + '.nii'
        data_nii = load_matrix_from_nifti_file(path_nii)
        list_mri.append(data_nii)

        path_json = prefix+suffixes[i]+'.json'
        file = open(path_json)
        data_json = json.load(file)

        for j in data_json['acqpar']:
            te_matrix_list[i, 0] = j['EchoTime']

    list_mri = np.array(list_mri)

    return (te_matrix_list, list_mri)


def ordinary_least_squares(voxel_signal_matrix, te_matrix_list):
    voxel_signal_matrix[voxel_signal_matrix == 0] = 1
    voxel_signal_matrix = np.log(voxel_signal_matrix)

    echo_time_vector = te_matrix_list.reshape([1, 8])

    dx = echo_time_vector - np.mean(echo_time_vector)
    dy = voxel_signal_matrix - np.mean(voxel_signal_matrix)

    # Transform the 4D array into a 2D matrix
    dy = dy.reshape((8, np.product(dy.shape[1:])))

    numerator = np.matmul(dx, dy)
    numerator = np.sum(numerator, axis=0)
    numerator = numerator.reshape(voxel_signal_matrix.shape[1:])

    dx_sq = np.sum((echo_time_vector - np.mean(echo_time_vector)) ** 2)
    denominator = np.sum(dx_sq)

    result = -numerator / denominator

    return result


if sys.version_info[:2] >= (4, 0):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
