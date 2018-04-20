# fMRI Methods
## Participants
To be filled in

## Task Paradigms
PsychoPy.

*Visual Control* Justify design

Within each run, participants viewed rotating, flashing visual checkerboards presented on the center of teh screen. Checkerboards were presented in 20 s blocks, with six total blocks in each run. Each block was proceeded by 20 s of fixation. 


## fMRI Data Acquisition
### NEED TO CONFIRM
- T1/T2 image specs
- EPI dim info

Briefly, all images were acquired with a 64 channel head coil on a 3T Siemens Prisma. A T1-weighted image was collected in-plane FOV=256x256 mm, 176 slices, 1.0 mm isotropic voxels. Whole-brain EPI acquisitions were acquired with TR=1000 ms, TE=30 ms, flip angle=55 deg, in-plane FOV=208 × 180 mm, 72 slices, 3.0 mm isotropic voxels, with a multi-band acceleration factor of 4 (Feinberg et al., 2010; Moeller et al., 2010). One run of each task was acquired, one with an anterior-to-posterior phase encoding. 

To measure cardiac and respiratory signals, a pulse oximeter and respiratory bellows were fitted to participants prior to the fMRI sessions. Those signals were recorded by the scanner host computer at a sampling rate of 200 Hz and 50 Hz, respectively. The physiological recordings were synchronized with the onset of the first sync pulse using a custom script. 

## fMRI Preporocessing

Results included in this manuscript come from preprocessing performed using FMRIPREP version latest [1], a Nipype [2,3] based tool. Each T1w (T1-weighted) volume was corrected for INU (intensity non-uniformity) using N4BiasFieldCorrection v2.1.0 [4] and skull-stripped using antsBrainExtraction.sh v2.1.0 (using the OASIS template). Brain surfaces were reconstructed using recon-all from FreeSurfer v6.0.0 [5], and the brain mask estimated previously was refined with a custom variation of the method to reconcile ANTs-derived and FreeSurfer-derived segmentations of the cortical gray-matter of Mindboggle [20]. Spatial normalization to the ICBM 152 Nonlinear Asymmetrical template version 2009c [6] was performed through nonlinear registration with the antsRegistration tool of ANTs v2.1.0 [7], using brain-extracted versions of both T1w volume and template. Brain tissue segmentation of cerebrospinal fluid (CSF), white-matter (WM) and gray-matter (GM) was performed on the brain-extracted T1w using fast [16] (FSL v5.0.9).

Functional data was slice time corrected using 3dTshift from AFNI v16.2.07 [10] and motion corrected using mcflirt (FSL v5.0.9 [8]). Distortion correction was performed using an implementation of the TOPUP technique [9] using 3dQwarp (AFNI v16.2.07 [10]). This was followed by co-registration to the corresponding T1w using boundary-based registration [15] with 9 degrees of freedom, using bbregister (FreeSurfer v6.0.0). Motion correcting transformations, field distortion correcting warp, BOLD-to-T1w transformation and T1w-to-template (MNI) warp were concatenated and applied in a single step using antsApplyTransforms (ANTs v2.1.0) using Lanczos interpolation.

Physiological noise regressors were extracted applying CompCor [17]. Principal components were estimated for the two CompCor variants: temporal (tCompCor) and anatomical (aCompCor). A mask to exclude signal with cortical origin was obtained by eroding the brain mask, ensuring it only contained subcortical structures. Six tCompCor components were then calculated including only the top 5% variable voxels within that subcortical mask. For aCompCor, six components were calculated within the intersection of the subcortical mask and the union of CSF and WM masks calculated in T1w space, after their projection to the native space of each functional run. Frame-wise displacement [18] was calculated for each functional run using the implementation of Nipype.

Many internal operations of FMRIPREP use Nilearn [21], principally within the BOLD-processing workflow. For more details of the pipeline see https://fmriprep.readthedocs.io/en/latest/workflows.html.

## Quality Assurance Metrics
To be filled in

## fMRI Analysis

## References
1. Esteban, Oscar, Blair, Ross, Markiewicz, Christopher J., Berleant, Shoshana L., Moodie, Craig, Ma, Feilong, Isik, Ayse Ilkay, Erramuzpe, Asier, Kent, James D., Goncalves, Mathias, DuPre, Elizabeth, Sitek, Kevin R., Poldrack, Russell A., Gorgolewski, Krzysztof J. poldracklab/fmriprep: 1.0.10. Zenodo; 2018. Available from: https://doi.org/10.5281/zenodo.1219187.  

2. Gorgolewski K, Burns CD, Madison C, Clark D, Halchenko YO, Waskom ML, Ghosh SS. Nipype: a flexible, lightweight and extensible neuroimaging data processing framework in python. Front Neuroinform. 2011 Aug 22;5(August):13. doi:10.3389/fninf.2011.00013.

3. Gorgolewski KJ, Esteban O, Ellis DG, Notter MP, Ziegler E, Johnson H, Hamalainen C, Yvernault B, Burns C, Manhães-Savio A, Jarecka D, Markiewicz CJ, Salo T, Clark D, Waskom M, Wong J, Modat M, Dewey BE, Clark MG, Dayan M, Loney F, Madison C, Gramfort A, Keshavan A, Berleant S, Pinsard B, Goncalves M, Clark D, Cipollini B, Varoquaux G, Wassermann D, Rokem A, Halchenko YO, Forbes J, Moloney B, Malone IB, Hanke M, Mordom D, Buchanan C, Pauli WM, Huntenburg JM, Horea C, Schwartz Y, Tungaraza R, Iqbal S, Kleesiek J, Sikka S, Frohlich C, Kent J, Perez-Guevara M, Watanabe A, Welch D, Cumba C, Ginsburg D, Eshaghi A, Kastman E, Bougacha S, Blair R, Acland B, Gillman A, Schaefer A, Nichols BN, Giavasis S, Erickson D, Correa C, Ghayoor A, Küttner R, Haselgrove C, Zhou D, Craddock RC, Haehn D, Lampe L, Millman J, Lai J, Renfro M, Liu S, Stadler J, Glatard T, Kahn AE, Kong X-Z, Triplett W, Park A, McDermottroe C, Hallquist M, Poldrack R, Perkins LN, Noel M, Gerhard S, Salvatore J, Mertz F, Broderick W, Inati S, Hinds O, Brett M, Durnez J, Tambini A, Rothmei S, Andberg SK, Cooper G, Marina A, Mattfeld A, Urchs S, Sharp P, Matsubara K, Geisler D, Cheung B, Floren A, Nickson T, Pannetier N, Weinstein A, Dubois M, Arias J, Tarbert C, Schlamp K, Jordan K, Liem F, Saase V, Harms R, Khanuja R, Podranski K, Flandin G, Papadopoulos Orfanos D, Schwabacher I, McNamee D, Falkiewicz M, Pellman J, Linkersdörfer J, Varada J, Pérez-García F, Davison A, Shachnev D, Ghosh S. Nipype: a flexible, lightweight and extensible neuroimaging data processing framework in Python. 2017. doi:10.5281/zenodo.581704.

4. Tustison NJ, Avants BB, Cook PA, Zheng Y, Egan A, Yushkevich PA, Gee JC. N4ITK: improved N3 bias correction. IEEE Trans Med Imaging. 2010 Jun;29(6):1310–20. doi:10.1109/TMI.2010.2046908.

5. Dale A, Fischl B, Sereno MI. Cortical Surface-Based Analysis: I. Segmentation and Surface Reconstruction. Neuroimage. 1999;9(2):179–94. doi:10.1006/nimg.1998.0395.

6. Fonov VS, Evans AC, McKinstry RC, Almli CR, Collins DL. Unbiased nonlinear average age-appropriate brain templates from birth to adulthood. NeuroImage; Amsterdam. 2009 Jul 1;47:S102. doi:10.1016/S1053-8119(09)70884-5.

7. Avants BB, Epstein CL, Grossman M, Gee JC. Symmetric diffeomorphic image registration with cross-correlation: evaluating automated labeling of elderly and neurodegenerative brain. Med Image Anal. 2008 Feb;12(1):26–41. doi:10.1016/j.media.2007.06.004.

8. Jenkinson M, Bannister P, Brady M, Smith S. Improved optimization for the robust and accurate linear registration and motion correction of brain images. Neuroimage. 2002 Oct;17(2):825–41. doi:10.1006/nimg.2002.1132.

9. Andersson JLR, Skare S, Ashburner J. How to correct susceptibility distortions in spin-echo echo-planar images: application to diffusion tensor imaging. Neuroimage. 2003 Oct;20(2):870–88. doi:10.1016/S1053-8119(03)00336-7.

10. Cox RW. AFNI: software for analysis and visualization of functional magnetic resonance neuroimages. Comput Biomed Res. 1996 Jun;29(3):162–73. doi:10.1006/cbmr.1996.0014.

11. Jenkinson M. Fast, automated, N-dimensional phase-unwrapping algorithm. Magn Reson Med. 2003 Jan;49(1):193–7. doi:10.1002/mrm.10354.

12. Huntenburg JM. Evaluating nonlinear coregistration of BOLD EPI and T1w images. Freie Universität Berlin; 2014. Available from: http://hdl.handle.net/11858/00-001M-0000-002B-1CB5-A.

13. Wang S, Peterson DJ, Gatenby JC, Li W, Grabowski TJ, Madhyastha TM. Evaluation of Field Map and Nonlinear Registration Methods for Correction of Susceptibility Artifacts in Diffusion MRI. Front Neuroinform. 2017 [cited 2017 Feb 21];11. doi:10.3389/fninf.2017.00017.

14. Treiber JM, White NS, Steed TC, Bartsch H, Holland D, Farid N, McDonald CR, Carter BS, Dale AM, Chen CC. Characterization and Correction of Geometric Distortions in 814 Diffusion Weighted Images. PLoS One. 2016 Mar 30;11(3):e0152472. doi:10.1371/journal.pone.0152472.

15. Greve DN, Fischl B. Accurate and robust brain image alignment using boundary-based registration. Neuroimage. 2009 Oct;48(1):63–72. doi:10.1016/j.neuroimage.2009.06.060.

16. Zhang Y, Brady M, Smith S. Segmentation of brain MR images through a hidden Markov random field model and the expectation-maximization algorithm. IEEE Trans Med Imaging. 2001 Jan;20(1):45–57. doi:10.1109/42.906424.

17. Behzadi Y, Restom K, Liau J, Liu TT. A component based noise correction method (CompCor) for BOLD and perfusion based fMRI. Neuroimage. 2007 Aug 1;37(1):90–101. doi:10.1016/j.neuroimage.2007.04.042.

18. Power JD, Mitra A, Laumann TO, Snyder AZ, Schlaggar BL, Petersen SE. Methods to detect, characterize, and remove motion artifact in resting state fMRI. Neuroimage. 2013 Aug 29;84:320–41. doi:10.1016/j.neuroimage.2013.08.048.

19. Pruim RHR, Mennes M, van Rooij D, Llera A, Buitelaar JK, Beckmann CF. ICA-AROMA: A robust ICA-based strategy for removing motion artifacts from fMRI data. Neuroimage. 2015 May 15;112:267–77. doi:10.1016/j.neuroimage.2015.02.064.

20. Klein A, Ghosh SS, Bao FS, Giard J, Häme Y, Stavsky E, et al. Mindboggling morphometry of human brains. PLoS Comput Biol 13(2): e1005350. 2017. doi:10.1371/journal.pcbi.1005350.

21. Abraham A, Pedregosa F, Eickenberg M, Gervais P, Mueller A, Kossaifi J, Gramfort A, Thirion B, Varoquaux G. Machine learning for neuroimaging with scikit-learn. Front in Neuroinf 8:14. 2014. doi:10.3389/fninf.2014.00014.