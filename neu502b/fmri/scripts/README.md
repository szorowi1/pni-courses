# scripts
This directory houses prepackaged functions for fMRI processing / analysis. In addition 

For all commands:
`fMRI_DIR="$HOME/Documents/fmri"`

### fmriprep v1.0.8
**Anatomical pipeline only**
fmriprep-docker $fMRI_DIR/raw $fMRI_DIR/preproc --participant-label XX --anat-only --nthreads 4 --fs-license-file $HOME/Documents/software/freesurfer/license.txt

**Functional pipeline only**
fmriprep-docker $fMRI_DIR/raw $fMRI_DIR/preproc --participant-label XX --ignore slicetiming --output-space fsaverage5 template --nthreads 4 --fs-license-file $HOME/Documents/software/freesurfer/license.txt

**Full pipeline**
fmriprep-docker $fMRI_DIR/raw $fMRI_DIR/preproc --participant-label XX --ignore slicetiming --output-space fsaverage5 template --nthreads 4 --fs-license-file $HOME/Documents/software/freesurfer/license.txt

### mriqc v0.10.4
**Check if installed properly**
docker run -it poldracklab/mriqc:latest --version

**Run mriqc**
docker run -it --rm -v $fMRI_DIR/raw:/data:ro -v $fMRI_DIR/mriqc:/out poldracklab/mriqc:latest /data /out participant