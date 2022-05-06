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

At present, the BIDS-StatsModel spec assumes the same sequential hierarchy.
Thus, the following node sequences are all valid:

* run → subject → dataset
* run → session → subject → dataset
* run → subject
* subject → dataset

A key point to appreciate here is that the keyword associated with each level of analysis
(i.e., "run", "session", "subject", or "dataset")
describes the grouping structure of the analysis,
rather than specifying the precise nature of the inputs and outputs.
The grouping structure must be made explicit in the `GroupBy` list
(see {py:class}`~bsmschema.models.BIDSStatsModel`).
The Level does determine what variables will be available to the model (see §3.3 below).

## Node structure

Each analysis node has fields defined in {py:class}`~bsmschema.models.BIDSStatsModel`.

The `Model` specification MUST be invoked prior to `Contrasts` and `DummyContrasts`.
That is, first, the `Model` specification is processed, typically resulting in the estimation of some model. Then, the `Contrasts` are generated from the parameter estimates obtained from the model estimation step and/or propagated from previous levels (see section 3.2).
Note that all applicable variables may be used for grouping. For example, if a task has multiple runs and multiple subjects, to separately fit a run-level model for each run from each subject, one should specify `"GroupBy": ["run", "subject"]`. If `"run"` is omitted, then all runs for each subject will be fit with a single model; likewise, if `"subject"` is omitted, then one model will be fit for each run, combining all subjects for higher levels than the current node.


## Enumerating sequences of Nodes

[Google Doc]: https://docs.google.com/document/d/1bq5eNDHTb6Nkx3WUiOBgKvLNnaa5OMcGtD0AZ9yms2M/edit
