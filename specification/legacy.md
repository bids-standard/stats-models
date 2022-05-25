# Legacy specification

This document exists to preserve components in the [Google Doc][] until they are fully
incorporated into another part of this website.

## Analysis nodes

### Specifying node sequences

Each analysis specification is composed of a collection of Nodes,
each describing a level of modeling (for example, run or subject),
and one or more sequences of these Nodes.
In traditional fMRI analysis packages such as SPM, FSL and AFNI,
which use the "summary statistics" approach,
the meaning of the levels of analysis is usually highly constrained,
and reflects a fixed hierarchy of entities that one ascends sequentially.
Most commonly, the 1st level analysis is understood to refer to
the statistical analysis of each individual BOLD run,
and the 2nd level analysis refers to the analysis of either a single subject
(which typically involves aggregating over 2 or more sets of 1st level results)
or an entire group of subjects (in the case where there’s only one run per subject).
Alternatively, in some packages (e.g., SPM), runs are first concatenated within-subject,
producing only 2-level structures (subject and group).
This hierarchy is not entirely rigid,
as it is sometimes necessary to inject another level into the mix – for example,
when each subject is scanned in multiple sessions, one may have a 4-level structure,
where the levels reflect the modeling of runs, sessions, subjects, and groups, respectively.

At present, the BIDS Stats Model spec assumes the same sequential hierarchy.
Thus, the following node sequences are all valid:

* run → subject → dataset
* run → session → subject → dataset
* run → subject
* subject → dataset

A key point to appreciate here is that the keyword associated with each level of analysis
(i.e., "run", "session", "subject", or "dataset")
describes the grouping structure of the analysis,
rather than specifying the precise nature of the inputs and outputs.
The grouping structure must be made explicit in the {py:attr}`~bsmschema.models.Node.GroupBy` list
(see {py:class}`~bsmschema.models.Node`).
The Level does determine what variables will be available to the model (see §3.3 below).

### Node structure

Each analysis node has fields defined in {py:class}`~bsmschema.models.Node`.

The {py:class}`~bsmschema.models.Node.Model` specification MUST be invoked prior to
{py:class}`~bsmschema.models.Node.Contrasts` and
{py:class}`~bsmschema.models.Node.DummyContrasts`.
That is, first, the `Model` specification is processed,
typically resulting in the estimation of some model.
Then, the `Contrasts` are generated from the parameter estimates obtained from
the model estimation step and/or propagated from previous levels (see section 3.2).
Note that all applicable variables may be used for grouping.
For example, if a task has multiple runs and multiple subjects,
to separately fit a run-level model for each run from each subject,
one should specify `"GroupBy": ["run", "subject"]`.
If `"run"` is omitted, then all runs for each subject will be fit with a single model;
likewise, if `"subject"` is omitted, then one model will be fit for each run,
combining all subjects for higher levels than the current node.

### Enumerating sequences of Nodes

To enumerate the sequences of {py:class}`~bsmschema.models.Node`s,
we use {py:class}`~bsmschema.models.Edges`.
Each `Edge` describes a single connection between two `Node`s,
and a combination of edges describes a sequence of `Node`s.

To demonstrate filtering, the following Edge links a subject-level model to a
dataset-level model that is exclusively fit to subjects with a value of "patient"
in a group column of a participants.tsv file:

```yaml
"Edges": [
  ...,
  {
    "Source": "subject-model"
    "Destination": "patient-model",
    "Filter": {
      "group": ["patient"]
    }
  }
]
```

If `"Edges"` is not present in the model,
then a linear sequence is assumed from the first `Node` to the last,
with no filters specified on each `Edge`.

## Inputs

### Specifying image inputs

Specification of image inputs to a BIDS Model is deliberately minimalistic.
The spec itself says nothing about how images are to be passed in as inputs to the first node in a model spec;
this is deliberately left as an implementation detail for BIDS Model-compliant software.
To ensure independence of statistical modeling from preprocessing,
the spec also does not constrain what _kind_ of images can be passed as inputs.
It does, however, allow any inputs passed in to be filtered on the basis of keywords
(or entities) defined in the core BIDS spec.
Minimally, this includes the `"task"`, `"run"`, `"session"`, and `"subject"` keywords
(additional keywords may be added as they’re merged into the BIDS spec).
For example:

```yaml
{
  "Name": "my_analysis",
  "BIDSModelVersion": "1.0.0",
  "Input": {
    "task": "motor",
    "run": 1
  },
  "Nodes": [...],
  "Edges": [...],
}
```

In this example, we only want to analyze images for the motor task, and with a run index of 1.
The implication (which we make explicit here) is that all image inputs to a
BIDS Model-based analysis must be BIDS-compliant filenames.

### Automatic input/output chaining between levels

Beyond the initial (and optional) top-level `"Input"` field, inputs and outputs do not have to (and indeed, cannot) be explicitly specified anywhere in a BIDS-Model model.
Instead, all outputs from each node are automatically passed on as the inputs to the next node.
These inputs can be included or ignored as desired within the next node in the sequence; however, all outputs generated by a given node are implicitly assumed to be available in the namespace of the next node in the sequence unless an explicit filter is present in the connecting edge.

More concretely, each node receives as input from the previous node any contrasts defined within the `Contrasts` sections of the previous node.
Multiple lower-level inputs that share the same contrast name are automatically concatenated when they are read in.
For example, take the following partial model specification:


```JSON
{
  "Nodes": [
    {
      "Level": "Run",
      "Name": "run",
      "GroupBy": ["run", "subject"],
      "Model": {
        "Type": "glm",
        "X": [
          "Word",
          "Face"
        ]
      },
      "Contrasts": [
        {
          "Name": "Word",
          "ConditionList": ["Word"],
          "Weights": [1]
        },
        {
          "Name": "Face",
          "ConditionList": ["Face"],
          "Weights": [1]
        }
      ]
    },
    {
      "Level": "Subject",
      "Name": "subject",
      "GroupBy": ["subject", "contrast"],
      "Model": {"Type": "Meta", "X": [1]},
      "DummyContrasts": {"Test": "t"}
    }
  ],
  "Edges": [
    {
      "Source": "run",
      "Destination": "subject"
    }
  ]
}
```


In this case, executing the first node, with the level "Run" (i.e., what is typically termed the 1st-level model) will produce contrast maps named "Face" and "Word" for each run and subject (because the `DummyContrasts` directive will automatically generate a 1 vs. 0 "t" contrast for each variable in `X`).
Suppose that there are three runs per subject.
Then, for each contrast ("Face" and "Word"),  a "Subject"-level model will have one input column with three rows.
The columns will always have the value 1 in all cells.
So, for the subject-level models, the input from the previous level will look like this:


```
run_index	Word
1	1
2	1
3	1

run_index	Face
1	1
2	1
3	1
```

Note that we did not need to explicitly state anywhere that "Face" and "Word" should be passed as inputs to the 2nd level.
Those variables are automatically made available for use in the subject-level model, by virtue of the fact that (a) we set `DummyContrasts` to `"t"`, and (b) the subject-level Node is connected by an Edge from the run-level Node, so it has automatic access to all variables outputted by the run-level Node.

Note also that availability does not mandate inclusion: the fact that Face and Word contrasts were defined in the 1st Node does not mean that the user has to include them in a model specification in a 2nd Node.
If the Face contrast is not explicitly named as a predictor in the `Model` and/or `Contrasts` specifications in the 2nd Node, it will simply be ignored in all further analysis (i.e., it will not be passed onto further Nodes).
An important corollary of this principle is that <span style="text-decoration:underline;">variables must be explicitly named in the <code>Model</code> and/or <code>Contrasts</code> sections of every <code>Level </code>in order to be propagated to the next `Level`.
Note that Tests of "Type": "F" are excluded from this, and not passed forward to other levels in the Model.</span>


### **Automatic ingestion of design-level and scan-level variables**

Per the core BIDS spec, each level of analysis (i.e., `run`, `session`, `subject`, or `dataset`) is associated with a different BIDS file or files that contains optional design events or variables.
These files are expected to be automatically read in and made available for inclusion in the model specification.
Specifically, the core BIDS spec defines the following level-to-file-to-variable mapping:


| Level | BIDS file with variables |
|--|--|
| `Run` | `_events.tsv` file corresponding to the `image` file <br> `_stim.tsv.gz` file corresponding to the `image` file <br>  `_physio.tsv.gz` file corresponding to the `image` file <br> `_timeseries.tsv` file corresponding to the `image` file |
| `Session` | `_scans.tsv` file corresponding to the session |
| `Subject` | `_sessions.tsv` file corresponding to the subject |
| `Dataset` | `_participants.tsv` corresponding to the entire dataset |

Table 1. Analysis level, corresponding BIDS files and additional variables.

Within each `Node`, the expectation is that the namespace should automatically include all variables found within the corresponding file(s) defined in the table.
For example, if the `events.tsv `files for a given project contain columns named "face" and "house", then, inside any node with `Level="Run"`, the user can automatically use the names `"face"` and `"house"` anywhere in the `Model` specification.

The expected formats for each of the file types listed in Table 1 are defined in the core BIDS spec, and any BIDS-Model-compliant software must respect the core spec and be able to read variables from all defined variable files.


### The intercept variable

The value `1` has a special status in `Model `and `Contrast` definitions as an intercept variable that requires no explicit name.
A value of `1` in `Model.X` indicates an intercept column is to be added to the design matrix.
At higher-level Nodes, the intercept has an interpretable meaning (e.g., in the absence of other regressors, it is the sample mean) and may stand in for the name of the input contrast in `Model` and `Contrast` definitions.


## Transformations

The OPTIONAL {py:class}`~bsmschema.models.Node.Transformations` section of a Node allows one to specify transformations of variables that should be applied prior to constructing a design matrix.

It is not in the scope of this specification to design a universal transformation description that all implementing tools must provide.
Rather, this section describes a protocol that will permit a `Transformer` to provide its own specification language.

Each `Transformations` section has fields defined in {py:class}`~bsmschema.models.Transformations`.

An implementation of BIDS Stats Models MUST fail if it cannot interpret the specified instruction set and cannot call out to an external program that implements the instruction set.
At this time, no I/O protocol is set forth in this specification, and it is left to implementations of BIDS-Stats Models and a given `Transformer` specification to negotiate.
An I/O protocol may be specified in future versions of this document.

Here is an example of how a transformation is used in a run-level analysis.
For reference in this example, the events.tsv includes a column "trial_type_junk" with entries of congruent/incongruent/junk, where "junk" indicates junk trials (no response, etc) and "response_time", which is the response time in seconds.
The first transformation, Factor, splits all events (rows of the events.tsv) into the three groupings, such that later on trial_type_junk.congruent will pull out the onset times of the congruent trials.
The "Scale" transformation is used to create an RT-modulated regressor where RT is mean centered.
Then the "Rename" transform is used to give nicer names to the output from the first transformation that used factor.
Last, regressors are convolved.
If you are accustomed to thinking about the time series regressors in a 3 column format (onset, duration, modulation) the transformations are basically setting up the modulation value and the onsets and durations are inherited from the corresponding columns in the events.tsv


```json
{
  "Level": "run",
  "Name": "run_flanker",
  "GroupBy": [
    "run",
    "session",
    "subject"
  ],
  "Transformations": {
    "Transformer": "pybids-transforms-v1",
    "Instructions": [
      {
        "Name": "Factor",
        "Input": [
          "trial_type_junk"
        ]
      },
      {
        "Name": "Scale",
        "Input": [
          "response_time"
        ],
        "Demean": true,
        "Rescale": false,
        "Output": [
          "demeaned_response_time"
        ]
      },
      {
        "Name": "Rename",
        "Input": [
          "trial_type_junk.congruent",
          "trial_type_junk.incongruent"
        ],
        "Output": [
          "congruent",
          "incongruent"
        ]
      },
      {
        "Name": "Convolve",
        "Model": "spm",
        "Input": [
          "congruent",
          "incongruent",
          "demeaned_response_time"
        ]
      }
    ]
  },
  "Model": {
    "Type": "glm",
    "X": [
      "congruent",
      "incongruent",
      "demeaned_response_time",
      "framewise_displacement",
      1
    ]
  }
}
```

Here is an example of a transformation modeling a quadratic age effect in a dataset level node (group analysis).

```json
{
  "Level": "dataset",
  "Name": "QuadratricAgeEffect",
  "GroupBy": [
    "contrast"
  ],
  "Transformations": {
    "Transformer": "pybids-transforms-v1",
    "Instructions": [
      {
        "Name": "Product",
        "Input": [
          "age",
          "age"
        ],
        "Output": [
          "age_squared"
        ]
      }
    ]
  },
  "Model": {
    "X": [
      "age",
      "age_squared",
      1
    ],
    "Type": "glm"
  },
  "DummyContrasts": {
    "Test": "t"
  }
}
```

The following Transformers have specifications and reference implementations:

| Transformer | Specification | Implementation |
|--|--|--|
| pybids-transforms-v1 | [PyBIDS Transformation Specification version 1](https://docs.google.com/document/d/1uxN6vPWbC7ciAx2XWtT5Y-lBrdckZKpPdNUNpwRxHoU/edit#) | https://github.com/bids-standard/pybids |


## Specifying the model

The {py:class}`~bsmschema.models.Model` section of a {py:class}`~bsmschema.models.Node`
specifies the statistical model to be estimated.

### Example

```json
{
  "Level": "Run",
  "Name": "run",
  "GroupBy": ["run", "session", "subject"],
  "Model": {
    "Type": "glm",
    "X": [
      "Face",
      "Word",
      "rot_x",
      "rot_y",
      "rot_z",
      1
    ],
    "Options": {
      "HighPassFilterCutoffHz": 0.008
    },
    "Software": [
      {
        "SPM": {
          "whitening": "AR(1)"
        }
      },
      {
        "FSL": {
          "HRF_type": "dgamma",
          "whitening": "FILM"
        }
      },
      {
        "AFNI": {
          "basis function": "CSPLIN",
          "serial correlation": "ARMA(1,1)"
        }
      }
    ]
  }
}
```

## Contrasts


### Contrast specification

Contrasts are specified in the (optional) `Contrasts` section of each node, and define weighted sums of available parameter estimates.
All contrasts in each node must have unique names (though names can be reused across different nodes, and can be the same as design matrix columns).
The `Contrasts` section has the following form:

```
{
  "Level": "Run",
  ...
  "Contrasts": [
    {
      "Name": "weighted sum",
      "ConditionList": ["cond_001", "cond_002",
                 "cond_003", "cond_004"],
      "Weights": [1, "-1/3", "-1/3", "-1/3"]
    },
    {
      "Name": "t-test 1",
      "ConditionList": ["cond_001", "cond_002"],
      "Weights": [1, -1],
      "Test": "t"
    },
    {
      "Name": "t-test 2",
      "ConditionList": ["cond_003", "cond_004"],
      "Weights": [1, -1],
      "Test": "t"
    },
    {
      "Name": "My favorite F-test",
      "ConditionList": ["cond_001", "cond_002",
                 "cond_003", "cond_004"],
      "Weights": [[1, -1, 0, 0], [0, 0, -1, 1]]
      "Test": "F"
    }
  ]
}
```

{py:attr}`~bsmschema.models.Node.Contrasts` field contains a list of JSON objects,
where each object represents a single contrast,
defined in {py:class}`~bsmschema.models.Contrast`.


### Dummy contrasts

In addition to an explicit specification of individual contrasts,
the BIDS Stats Model spec also supports an optional {py:attr}`~bsmschema.models.Node.DummyContrasts`
field that one can include as a field at the top level of each node.

Note that each contrast generated via `DummyContrasts` will have the same name as the variable it is based on.
However, in cases where the same name is re-used in the `Contrasts` list, the latter will take precedence over any contrast generated via `DummyContrasts`.
For example, if the design matrix contains a variable named `"face"`, `DummyContrasts` is `true`, and a contrast with the name` "face"` is also included in `Contrasts`, only the latter will be retained, and the `DummyContrasts`-generated contrast will be ignored.

Note that tests of "Type: "F" will be computed but their parameters estimates will not be passed forward through an "Edge" to subsequent "Nodes" in the model.



[Google Doc]: https://docs.google.com/document/d/1bq5eNDHTb6Nkx3WUiOBgKvLNnaa5OMcGtD0AZ9yms2M/edit
