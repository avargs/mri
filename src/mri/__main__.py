import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib

from mri import load_data, load_matrix_from_nifti_file, ordinary_least_squares


def usage():
    pass


def get_config(args):
    config = dict()
    
    # Check if a path to Nifit files has been provided
    config["input_data_folder"] = args[1] if len(args) > 1 else None
    
    if config["input_data_folder"] is None:
        usage()
        raise Exception("Not enough args...\n\'{:}\'".format(('\'\n\'').join(args[1:])))
    
    # Use the provided prefix if any
    config["input_data_prefix"] = args[2] if len(args)> 2 else ''

    # Load the reference R2s map for future comparisons
    config["reference_relaxation_rate_map_path"] = args[3] if len(args) > 3 else None
    
    return config


def show_slice(relaxation_rate_map_matrix, slice_index=None):
    if slice_index is None:
        slice_index = relaxation_rate_map_matrix.shape[-1] // 2

    plt.figure()
    plt.imshow(relaxation_rate_map_matrix[:, :, slice_index])


def print_stats(relaxation_rate_map_matrix, name=""):
    print('Mean relaxation rate:', np.mean(relaxation_rate_map_matrix))
    print('Median relaxation rate:', np.median(relaxation_rate_map_matrix))
    print('Min relaxation rate:', np.min(relaxation_rate_map_matrix))
    print('Max relaxation rate:', np.max(relaxation_rate_map_matrix))


def main():
    # Get config parameters from the program's argument
    config = get_config(sys.argv)

    # Load images from nii1 files and store them into a 4D matrix hmri_matrix_list[TE, r] where:
    # - the first dimension (TE) indexes the successively sampled 3D hMRI matrices.
    # - the 3D hMRI matrix map 3d positions (r) to space-sampled intensities.
    #
    # The echo time (TE) for each matrix is loaded as well and stored into a the vector te_matrix_list[TE] where:
    # - the first dimension (TE) indexes the successive negated sample times as 3d matrices
    (te_matrix_list, hmri_matrix_list) = load_data(config["input_data_folder"], config["input_data_prefix"])

    # Compute the ordinary least square solution
    relaxation_rate_map_matrix = ordinary_least_squares(hmri_matrix_list, te_matrix_list)

    # Scale back the relaxation map data to the range of the reference relaxation map
    relaxation_rate_map_matrix *= 1000.0

    # Save array into nifti file
    nifti_file = nib.Nifti1Image(relaxation_rate_map_matrix, np.eye(4))
    nib.save(nifti_file, Path('./EstimatedRelaxationMap.nii'))

    # Show and print the stats for the produced relaxation rate map
    show_slice(relaxation_rate_map_matrix)
    print_stats(relaxation_rate_map_matrix)
    print()

    if config["reference_relaxation_rate_map_path"] is not None:
        # Load the reference relaxation map
        reference_relaxation_rate_map_matrix = load_matrix_from_nifti_file(config["reference_relaxation_rate_map_path"])

        # Show and print the stats of the reference relaxation map
        show_slice(reference_relaxation_rate_map_matrix)
        print_stats(reference_relaxation_rate_map_matrix)
        print()

    plt.show()


main()
