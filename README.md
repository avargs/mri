# Mri relaxation rate map estimation tool



## Description

The purpose of this project is to estimate a quantitative map of effective transverse relaxation rate in the human brain from set of gradient-echo magnetic resonance images recorded at a different echo times (TE).

The structure of the project is as follows:

 - Load images from .nii files and echo time information from .json files. 
 - Estimate the relaxation rate of the set of images by implementing an ordinary least square algorithm.
 - Display one slice of the estimated relaxation rate map with its respective statistical features.
 - Display one slice of a reference relaxation rate map
	


## Requirements
 - [python >= 3.8](https://pip.pypa.io/en/stable/installation/)
 - [pip >= 22.3.1](https://www.python.org/downloads/)
 - [git >= 2.39.1](https://git-scm.com/downloads)

## Install

```bash
pip install "git+https://github.com/avargs/mri"
```

## Usage

### Prepare input data

Extract the dataset

```bash
$ unzip "mri_archive_path.zip"
```

Move into the dataset

```bash
$ cd "mri_archive_path/"
```

```bash
$ py -m mri "mri_folder_path" ["mri_file_prefix" ["reference_relaxation_map.nii"]]
```

Example loading without the reference map:

```bash
$ py -m mri t1w_mfc_3dflash_v1i_R4_0015/ anon_s2018-02-28_18-26-190921-00001-0
```


## Note

This project has been set up using PyScaffold 4.4. For details and usage
information on PyScaffold see https://pyscaffold.org/.
