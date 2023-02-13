import sys
import json
from pathlib import Path
from os import listdir

import numpy as np
import nibabel as nib


def load_matrix_from_nifti_file(nifti_file_path):
    nifti_matrix = nib.load(nifti_file_path)
    nifti_matrix = np.array(nifti_matrix.dataobj, dtype='float')

    return nifti_matrix


def load_nifti_folder(nifti_folder_path, prefix=''):
    ''' Store 3d images in a list and reading the json files to create a EchoTime vector '''    
    nifti_matrix_list = []
    
    # List the filenames of the nifti_folder into nifti_folder_filename_list
    nifti_folder_filename_list = list(listdir(nifti_folder_path))
    
    # Filter out the non-Nifti files and associate through a reduced / sortable id (suffix) mapping
    nifti_folder_filename_dict = dict([(filename.replace(prefix, ''), filename) for filename in nifti_folder_filename_list if filename.lower().endswith('.nii')])
    
    # Retrieve and sort the suffix list
    nifti_suffix_list = list(nifti_folder_filename_dict.keys())
    nifti_suffix_list = sorted(nifti_suffix_list)
    
    # Store the ordered filename list
    nifti_filename_list = [nifti_folder_filename_dict[suffix][:-4] for suffix in nifti_suffix_list]
    te_vector = np.empty([len(nifti_filename_list), 1], dtype=float)

    # Go through each nifti_filenme and load the associated matrix and EchoTime (TE)
    for (te_index, nifti_filename) in enumerate(nifti_filename_list):
        # Load the nifti matrix
        nifti_file_path = Path(nifti_folder_path).joinpath('{:}.nii'.format(nifti_filename))
        nifti_matrix = load_matrix_from_nifti_file(nifti_file_path)
        
        # Add the nifti matrix to the nifti_matrix_list
        nifti_matrix_list.append(nifti_matrix)
        
        # Load EchoTime (TE) information
        json_file_path = Path(nifti_folder_path).joinpath('{:}.json'.format(nifti_filename))
        with open(json_file_path) as file:
            json_data = json.load(file)

        # Store TE in the te_vector at the matrix index's
        te_vector[te_index, 0] = json_data['acqpar'][0]['EchoTime']

    # Aggregate loaded data into a 4D matrix of successively sampled 3D hMRI matrices
    nifti_matrix_list = np.array(nifti_matrix_list)

    return (te_vector, nifti_matrix_list)


def load_data(nifti_matrix_path, prefix=''):
    return load_nifti_folder(nifti_matrix_path, prefix)


def ordinary_least_squares(voxel_signal_matrix, te_vector):
    voxel_signal_matrix[voxel_signal_matrix == 0] = 1
    voxel_signal_matrix = np.log(voxel_signal_matrix)

    echo_time_vector = te_vector.reshape([1, 8])

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
