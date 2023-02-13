#!/usr/bin/env bash

git push
yes | pip uninstall mri


yes | pip install "git+https://github.com/avargs/mri" && \
\
py -m mri \
   ../data/t1w_mfc_3dflash_v1i_R4_0015/ \
   anon_s2018-02-28_18-26-190921-00001 \
   "../data/anon_s2018-02-28_18-26-185345-00001-00224-1_RFSC_R2s_OLS.nii"
