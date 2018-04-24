## Methods
### Participants
All experimental procedures were approved by the Princeton University Institutional Review Board. Two participants (both female) volunteered to participate in this experiment as part of a course on cognitive neuroscience methods. All participants reported being right-handed and without a current or past diagnosis of a psychiatric or neurological disorder.

### Task Paradigms
**Visual Localizer** The visual localizer task was used to detect BOLD response visual cortex. To evoke a BOLD response, participants viewed a rotating and flashing black-and-white checkerboard stimulus. Each stimulus lasted 20 s followed by 20 s of fixation. The checkerboard stimulus was presented six total times. The run lasted 250 s.

**Breath-holding** The breath-holding task was used to measure the physiological BOLD response to a hypercapniac event. Participants were instructed to hold their breath for 20 s, followed by a recovery period of 40 s. Participants completed six total trials of breathholding. The run lasted 370 s.

**Hyperventilation** The hyperventilation task was used to measure the physiological BOLD response to a hypocapniac event. Participants were coached rapidly inhale then exhale, with each action lasting 2 s. This was followed by a recovery period of 40 s. Participants completed six total trials of hyperventilation. The run lasted 370 s.

**Visual Breath-hold** The visual breath-hold task was designed to measure the effects of a hypercapniac event on BOLD detection in visual cortex. Participants were again instructed to hold their breath for 20 s. After 10 s elapsed, the same checkerboard stimuli as above were presented for 20 s such that breathholding ended 10 s into the presentation of the visual stimulus. Blocks of breathholding and visual stimuli were separated by 30 s of fixation. The run lasted 370 s.

**Visual Hyperventilation** The visual hyperventilation task was designed to measure the effects of a hypocapniac event on BOLD detection in visual cortex. Participants were again coached in rapid breathing for 20 s. After 10 s elapsed, the same checkerboard stimuli as above were presented for 20 s such that hyperventilation ended 10 s into the presentation of the visual stimulus. Blocks of hyperventilation and visual stimuli were separated by 30 s of fixation. The run lasted 370 s.

Visual stimuli were programmed in Python and Psychopy[1] and were presented with a projector. Participants viewed the projection on a screen fixed at the back of the scanner bore, through a mirror fixed in front of the eyes.

### fMRI Data Acquisition
Briefly, all images were acquired with a 64 channel head coil on a 3T Siemens Prisma. A T1-weighted MPRAGE image was acquired with TR=2530 ms,  TE 3.31 ms, flip angle=7 deg, in-plane FOV=256 x 256 mm, 176 slices, 1.0 mm isotropic voxels. For advanced anatomical registration (see below), a T2-weighted image was acquired TR=3200 ms, TE=428 ms, flip angle=120 deg, in-plane FOV=256 × 256 mm, 72 slices, 1.0 mm isotropic voxels. Whole-brain EPI acquisitions were acquired with TR=1000 ms, TE=30 ms, flip angle=55 deg, in-plane FOV=192 × 192 mm, 56 slices, 3.0 mm isotropic voxels, with a multi-band acceleration factor of 4. One run of each task was acquired, one with an anterior-to-posterior phase encoding. For susceptibility distortion correction (see below), a fieldmap was acquired to the start of functional scanning with TR=1000 ms, TE=3.47 ms, flip angle=120 deg, in-plane FOV=192 × 192 mm, 56 slices, 3.0 mm isotropic voxels.

To measure cardiac and respiratory signals, a pulse oximeter and respiratory bellows were fitted to participants prior to the fMRI sessions. Those signals were recorded by the scanner host computer at a sampling rate of 200 Hz and 50 Hz, respectively. The physiological recordings were synchronized with the onset of the first sync pulse using a custom script. 

### fMRI Preprocessing
Results included in this manuscript come from preprocessing performed using FMRIPREP v1.0.8 [2], a Nipype [3], [4] based tool. Each T1w (T1-weighted) volume was corrected for INU (intensity non-uniformity) using N4BiasFieldCorrection v2.1.0  [5] and skull-stripped using antsBrainExtraction.sh v2.1.0 (using the OASIS template). Brain surfaces were reconstructed using recon-all from FreeSurfer v6.0.0 [6], and the brain mask estimated previously was refined with a custom variation of the method to reconcile ANTs-derived and FreeSurfer-derived segmentations of the cortical gray-matter of Mindboggle [7]. Spatial normalization to the ICBM 152 Nonlinear Asymmetrical template version 2009c [8] was performed through nonlinear registration with the antsRegistration tool of ANTs v2.1.0 [9], using brain-extracted versions of both T1w volume and template. Brain tissue segmentation of cerebrospinal fluid (CSF), white-matter (WM) and gray-matter (GM) was performed on the brain-extracted T1w using fast (FSL v5.0.9) [10].

Functional data was motion corrected using mcflirt (FSL v5.0.9 [11]). Slice timing was not performed due to the block design of tasks and short repetition time. Distortion correction was performed using an implementation of the TOPUP technique [12] using 3dQwarp (AFNI v16.2.07 [13]). This was followed by co-registration to the corresponding T1w using boundary-based registration [14] with 9 degrees of freedom, using bbregister (FreeSurfer v6.0.0). Motion correcting transformations, field distortion correcting warp, BOLD-to-T1w transformation and T1w-to-template (MNI) warp were concatenated and applied in a single step using antsApplyTransforms (ANTs v2.1.0) using Lanczos interpolation.

Physiological noise regressors were extracted applying CompCor [15]. Principal components were estimated for the two CompCor variants: temporal (tCompCor) and anatomical (aCompCor). A mask to exclude signal with cortical origin was obtained by eroding the brain mask, ensuring it only contained subcortical structures. Six tCompCor components were then calculated including only the top 5% variable voxels within that subcortical mask. For aCompCor, six components were calculated within the intersection of the subcortical mask and the union of CSF and WM masks calculated in T1w space, after their projection to the native space of each functional run. Framewise displacement [16] was calculated for each functional run using the implementation of Nipype.

Many internal operations of FMRIPREP use Nilearn [17], principally within the BOLD-processing workflow. For more details of the pipeline see https://fmriprep.readthedocs.io/en/latest/workflows.html.

### Quality Assurance Metrics
The quality of the acquired images was assessed using the MRIQC v0.10.4 [18]. The anatomical scans were visually inspected for artifacts and quantitative metrics yielded high SNR. Functional scans were similarly inspected for artifacts using "Power" plots [19]. Quantitative metrics revealed high SNR and tSNR and few volumes with Frame-wise displacement > 0.5 mm (n = 3). See summary reports for details.

## References
[1] J. W. Peirce, “Generating Stimuli for Neuroscience Using PsychoPy,” Front. Neuroinform., vol. 2, p. 10, 2008.
[2] O. Esteban et al., poldracklab/fmriprep: 1.0.10. 2018.
[3] K. Gorgolewski et al., “Nipype: a flexible, lightweight and extensible neuroimaging data processing framework in python,” Front. Neuroinform., vol. 5, p. 13, Aug. 2011.
[4] K. J. Gorgolewski et al., Nipype: a flexible, lightweight and extensible neuroimaging data processing framework in Python. 0.13.1. 2017.
[5] N. J. Tustison et al., “N4ITK: improved N3 bias correction,” IEEE Trans. Med. Imaging, vol. 29, no. 6, pp. 1310–1320, Jun. 2010.
[6] A. M. Dale, B. Fischl, and M. I. Sereno, “Cortical surface-based analysis. I. Segmentation and surface reconstruction,” Neuroimage, vol. 9, no. 2, pp. 179–194, Feb. 1999.
[7] A. Klein et al., “Mindboggling morphometry of human brains,” PLoS Comput. Biol., vol. 13, no. 2, p. e1005350, Feb. 2017.
[8] V. S. Fonov, A. C. Evans, R. C. McKinstry, C. R. Almli, and D. L. Collins, “Unbiased nonlinear average age-appropriate brain templates from birth to adulthood,” Neuroimage, vol. 47, p. S102, 2009.
[9] B. B. Avants, C. L. Epstein, M. Grossman, and J. C. Gee, “Symmetric diffeomorphic image registration with cross-correlation: evaluating automated labeling of elderly and neurodegenerative brain,” Med. Image Anal., vol. 12, no. 1, pp. 26–41, Feb. 2008.
[10] Y. Zhang, M. Brady, and S. Smith, “Segmentation of brain MR images through a hidden Markov random field model and the expectation-maximization algorithm,” IEEE Trans. Med. Imaging, vol. 20, no. 1, pp. 45–57, Jan. 2001.
[11] M. Jenkinson, P. Bannister, M. Brady, and S. Smith, “Improved optimization for the robust and accurate linear registration and motion correction of brain images,” Neuroimage, vol. 17, no. 2, pp. 825–841, Oct. 2002.
[12] J. L. R. Andersson, S. Skare, and J. Ashburner, “How to correct susceptibility distortions in spin-echo echo-planar images: application to diffusion tensor imaging,” Neuroimage, vol. 20, no. 2, pp. 870–888, Oct. 2003.
[13] R. W. Cox, “AFNI: software for analysis and visualization of functional magnetic resonance neuroimages,” Comput. Biomed. Res., vol. 29, no. 3, pp. 162–173, Jun. 1996.
[14] D. N. Greve and B. Fischl, “Accurate and robust brain image alignment using boundary-based registration,” Neuroimage, vol. 48, no. 1, pp. 63–72, Oct. 2009.
[15] Y. Behzadi, K. Restom, J. Liau, and T. T. Liu, “A component based noise correction method (CompCor) for BOLD and perfusion based fMRI,” Neuroimage, vol. 37, no. 1, pp. 90–101, Aug. 2007.
[16] J. D. Power, A. Mitra, T. O. Laumann, A. Z. Snyder, B. L. Schlaggar, and S. E. Petersen, “Methods to detect, characterize, and remove motion artifact in resting state fMRI,” Neuroimage, vol. 84, pp. 320–341, Jan. 2014.
[17] A. Abraham et al., “Machine learning for neuroimaging with scikit-learn,” Front. Neuroinform., vol. 8, p. 14, Feb. 2014.
[18] O. Esteban, D. Birman, M. Schaer, O. O. Koyejo, R. A. Poldrack, and K. J. Gorgolewski, “MRIQC: Advancing the automatic prediction of image quality in MRI from unseen sites,” PLoS One, vol. 12, no. 9, p. e0184661, Sep. 2017.
[19] J. D. Power, “A simple but useful way to assess fMRI scan qualities,” Neuroimage, vol. 154, pp. 150–158, Jul. 2017.