# unpitou-RAGE

A simple BIDS-app that transforms MP2RAGE to a MPRAGE-ish T1w-like contrast to run standard neuroimaging pipelines (eg. sMRIPrep, freesurfer)
This is pursuing the tradition of making new mp2rage software for the same purpose.

The closest approach is [Presurfer](https://github.com/srikash/presurfer) which is SPM/Matlab based.

Other approaches includes [RobustCombination](https://github.com/JosePMarques/MP2RAGE-related-scripts/blob/master/func/RobustCombination.m) which has been replicated in (way too) many packages/repos/...
RobustCombination requires setting a somewhat arbitrary "regularization" parameter, found through manual exploration. That regularization parameter trades-off background noise removal for B1 bias. The "optimal" parameter seems to vary from one scanner model to another, even at matching field strength and matching parameters.

Presurfer approach, replicated here using python code and ANTs for N4 bias field correction, do not require that step. It simply bias-field-corrects the second inversion time image, scale it to a [0,1] range and multiply the UNIT1 image. This seems to effectively removes the background noise from UNIT1, provided some sensible ranges for MP2RAGE acquisition (ie. if UNIT1 already is T1w like), gives a T1w like contrast with limited BIAS that can be registered to templates (eg. MNI) and undergo freesurfer pipelines (standalone or through sMRIPrep).
