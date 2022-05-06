# Walkthrough

A BIDS stats model describes:

- out to prepare the regressors for the GLM: `Transformation`
- the design matrix: `X`
- the contrasts to compute: `contrasts`
- several other options

It also allows to specify those for different levels of the analysis:

- run
- session
- subject
- dataset

An example of JSON file could look something like that:

```json
{
  "Name": "Basic model",
  "BIDSModelVersion": "0.1.0",
  "Description": "model for motion localizer",
  "Input": {
    "space": ["IXI549Space"],
    "task": ["motionloc"]
  },
  "Nodes": [
    {
      "Level": "Run",
      "Name": "Run",
      "GroupBy": ["run", "subjec"],
      "Transformations": {
        "Transformer": "pybids-transforms-v1",
        "Instructions": [
          {
            "Name": "Convolve",
            "Input": ["trial_type.motion", "trial_type.static"],
            "Output": ["motion", "static"]
          }
        ]
      },
      "Model": {
        "Type": "glm",
        "X": ["motion", "static", "trans_?", "rot_?", "*outlier*"],
        "HRF": {
          "Variables": ["motion", "static"],
          "Model": "DoubleGamma"
        },
        "Options": {
          "HighPassFilterCutoffHz": 0.0078,
          "Mask": {
            "desc": ["brain"]
          }
        },
        "Software": [
          {
            "SPM": {
              "HRFderivatives": "Temporal",
              "SerialCorrelation": "FAST"
            }
          }
        ]
      },
      "DummyContrasts": {
        "Test": "t",
        "Contrasts": ["motion", "static"]
      },
      "Contrasts": [
        {
          "Name": "motion_vs_static",
          "ConditionList": ["motion", "static"],
          "weights": [1, -1],
          "type": "t"
        }
      ]
    }
  ]
}
```

Here are what the different sections mean

## Inputs

```json
  "Input": {
    "space": "IXI549Space",
    "task": "motionloc"
  }
```

This allows you to specify input images you want to include based on the BIDS
entities in their name, like the task (can be more than one) or the MNI space
your images are in (here `IXI549Space` is for SPM 12 typical MNI space).

## Nodes

Then the model has a `Nodes` array where each objectin defines what is to be
done at a given `Level` (`Run`, `Subject`, `Dataset`)

```json
    "Nodes": [
        {
            "Level": "Run",
```

## Transformations

The `Transformations` object allows you to define what you want to do to some
variables, before you put them in the design matrix. Here this shows how to
subtract 3 seconds from the event onsets of the conditions listed in the
`trial_type` columns of the `events.tsv` file, and put the output in a variable
called `motion` and `static`.

```json
"Transformations": {
    "Transformer": "cpp_spm",
    "Instructions": [
        {
        "Name": "Subtract",
        "Input": ["trial_type.motion", "trial_type.static"],
        "Value": 3,
        "Output": ["motion", "static"]
        }
    ]
}
```

## Model

Then comes the model object.

`X` defines the variables that have to be put in the design matrix. Here
`trans_?` means any of the translation parameters (in this case `trans_x`,
`trans_y`, `trans_z`) from the realignment that are stored in `_confounds.tsv`
files. Similarly `*outlier*` means that any "scrubbing" regressors created by
fMRIprep or CPP SPM to detect motion outlier or potential dummy scans will be
included (those regressors are also in the `_confounds.tsv` files).

```{admonition} Note
Following standard Unix-style glob rules
- “*” is interpreted to match 0 or more alphanumeric characters,
- “?” is interpreted to match exactly one alphanumeric character.
```

`HRF` specifies which variables of X have to be convolved and what HRF model to
use to do so.

```json
    "Model": {
        "Type": "glm",
        "X": [
            "motion",
            "static",
            "trans_?",
            "rot_?",
            "*outlier*"
        ],
        "HRF": {
            "Variables": [
                "motion",
                "static"
            ],
            "Model": "DoubleGamma"
        }
```

## Contrasts

Then we have the contrasts definition where `DummyContrasts` compute the
contrasts against baseline for the condition `motion` and `static` and where
`Contrasts` compute the t-contrats for "motion greater than static" with these
given weights.

```json
    "DummyContrasts": {
        "Test": "t",
        "Contrasts": [
            "motion",
            "static"
        ]
        },
    "Contrasts": [
        {
            "Name": "motion_gt_static",
            "ConditionList": [
                "motion",
                "static"
            ],
            "weights": [
                1,
                -1
            ],
            "type": "t"
        }
    ]
```

## Creating a default model

### with pybids

https://bids-standard.github.io/pybids/generated/bids.modeling.auto_model.html

```python
from bids import BIDSLayout
from bids.modeling import auto_model
import json

# indexing the dataset
layout = BIDSLayout(path_to_dataset)

# creating the default model
model = auto_model(layout, one_vs_rest=True)

# saving to a JSON file
with open("model-default_smdl.json", "w") as outfile:
    json.dump(model[0], outfile)
```

### with bids-matlab

https://github.com/bids-standard/bids-matlab

```matlab
% indexing the dataset
BIDS = bids.layout(path_to_dataset);

% creating the default model
bm = bids.Model();
bm = bm.default(BIDS);

% saving to a JSON file
filename = fullfile(pwd, 'model-default_smdl.json');
bm.write(filename);
```
