#!/bin/csh -f
setenv SUBJECTS_DIR /media/szoro/SZORO1/pni-courses/neu502b/fmri/preproc/freesurfer
setenv ROOT_DIR /media/szoro/SZORO1/pni-courses/neu502b/fmri/first_levels 

set SUBJECTS = ("sub-01" "sub-02")
set TASKS = ("visualcontrol" "visualhyperventilate" "visualbreathhold")

foreach SUBJ ($SUBJECTS)

    foreach TASK ($TASKS)

        foreach SPACE ("L" "R")

           ## Define hemi
           if ($SPACE == "L") then
               set HEMI = lh
           else
               set HEMI = rh
           endif

           ## Smooth data
           mri_surf2surf --hemi $HEMI --srcsubject fsaverage5 --srcsurfval $ROOT_DIR/$TASK/{$SUBJ}_task-{$TASK}_space-fsaverage5.{$SPACE}.psc.nii.gz --trgsubject $SUBJ --trgsurfval $ROOT_DIR/$TASK/{$SUBJ}_task-{$TASK}_space-{$SUBJ}.{$SPACE}.psc.nii.gz --nsmooth-out 3

        end
    
    end

end
