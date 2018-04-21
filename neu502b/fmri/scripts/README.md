# scripts
This directory houses prepackaged functions for fMRI processing / analysis. It also documents the commands used for [fmriprep](https://fmriprep.readthedocs.io/en/latest/) and [mriqc](https://mriqc.readthedocs.io/en/latest/index.html). 

For all commands:

`fMRI_DIR=$HOME/Documents/fmri`

### fmriprep v1.0.8
**Anatomical pipeline only**

`fmriprep-docker $fMRI_DIR/raw $fMRI_DIR/preproc --participant-label XX --anat-only --nthreads 4 --fs-license-file $HOME/Documents/software/freesurfer/license.txt --work-dir $fMRI_DIR/scratch`

**Functional pipeline only**

`fmriprep-docker $fMRI_DIR/raw $fMRI_DIR/preproc --participant-label XX --ignore slicetiming --output-space T1w fsaverage5 --nthreads 4 --fs-license-file $HOME/Documents/software/freesurfer/license.txt --work-dir $fMRI_DIR/scratch`

**Full pipeline**

`fmriprep-docker $fMRI_DIR/raw $fMRI_DIR/preproc --participant-label XX --ignore slicetiming --output-space T1w fsaverage5 --nthreads 4 --fs-license-file $HOME/Documents/software/freesurfer/license.txt --work-dir $fMRI_DIR/scratch`

### mriqc v0.10.4
**Check if installed properly**

`docker run -it poldracklab/mriqc:latest --version`

**Run mriqc**

`docker run -it --rm -v $fMRI_DIR/raw:/data:ro -v $fMRI_DIR/mriqc:/out poldracklab/mriqc:latest /data /out participant`
