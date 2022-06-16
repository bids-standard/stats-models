# Integration with other standards

This standard describes the contents of a BIDS Stats Model document.
Here we discuss the relationship of this standard to other standards.

## The Brain Imaging Data Structure (BIDS)

The models described by this standard are intended to supplement datasets 
structured according to the Brain Imaging Data Structure (BIDS) standard.
BIDS describes the naming and organization of neuroimages, task events and
timing parameters.
A BIDS Stats Model will use variables extracted from BIDS tabular files,
filename components (for example, `"task"`), 
and possibly metadata extracted from JSON "sidecars", 
but otherwise has no strong dependence on the BIDS standard.

### Naming of BIDS Stats Models files in BIDS datasets

The location and naming scheme were not specified in BIDS at the time of this writing, 
but this may have changed since publication. 
See the latest version of BIDS at https://bids-specification.readthedocs.io.
Until these conventions are established in BIDS, it is RECOMMENDED to use the following:

Template:
```
models/model-<label>_[desc-<description>]_smdl.json
```

Examples:
```
models/model-nback_desc-preprint_smdl.json
models/model-nback_desc-postreview_smdl.json
models/model-nonwordrepetition_smdl.json
```

The `smdl` suffix stands for "statistical model".

### BIDS Derivatives

BIDS Stats Models does not prescribe naming conventions 
for the outputs of estimators implementing the BIDS Stats Models specification.
We recommend using following the [BIDS Derivatives][] specification to the extent possible.

## NIDM-Results

The purpose of BIDS Stats Models is prescriptive, 
essentially a recipe for how to fit a model, 
rather than a description of a model that was already fit.
[NIDM-Results][] describes the results of modeling, 
and does not conflict with BIDS Stats Models.


[BIDS]: https://bids-specification.readthedocs.io/
[BIDS Derivatives]: https://bids-specification.readthedocs.io/en/stable/05-derivatives/01-introduction.html
[NIDM-Results]: http://nidm.nidash.org/specs/nidm-results.html
