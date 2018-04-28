#!/bin/csh -f
setenv ROOT_DIR ../first_levels

## Locate files
set FILES = (`find $ROOT_DIR -type f -name "**fsaverage5**.nii.gz" | sort`)

## Main loopl
foreach FP ($FILES)

    ## Extract filename from path.
    set FN = (`basename $FP`)

    ## Get subject name.
    set SUBJ = (`echo $FN | cut -c1-6`)

    ## Check hemisphere.
    if ( "$FN" =~ *fsaverage5.L* ) then
        set HEMI = "lh"
    else 
        set HEMI = "rh"
    endif

    ## Define out file.
    set TARG = `echo $FP | sed "s;fsaverage5;$SUBJ;g"`
    
    ## Interpolate / smooth data
    mri_surf2surf --hemi $HEMI --srcsubject fsaverage5 --srcsurfval $FP --trgsubject $SUBJ --trgsurfval $TARG --nsmooth-out 3


end
