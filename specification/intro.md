# BIDS Stats Models

## Introduction

BIDS Statistical Models is a specification aimed at describing how a General Linear Model (GLM) or similar model should be fit to BIDS datasets, with current emphasis on task-based fMRI. Its purpose is prescriptive (e.g. a recipe of how to fit a model), rather than descriptive (e.g., summary of models that have already been fit).

At the core of BIDS Statistical Models (BSM) is a single, machine-readable JSON document that allows users to define a fully reproducible statistical model across multiple stages of analysis. This specification—in combination with a preprocessed BIDS dataset—is sufficient to execute the statistical models, with minimal configuration and manual intervention required from the user.

### Why?

The representation of neuroimaging statistical models in a formal, machine readable document has several benefits. First, although much recent progress has been made in standardizing and automating neuroimaging pre-processing pipelines, model fitting typically requires a high degree of customization, resulting in heterogeneous analysis scripts that are often not **reproducible**. Second, bespoke user-generated analysis scripts can lack **transparency**, making it difficult for other researchers to interpret the key modeling decisions made in an analysis. Third, without a common machine-readable format for statistical models, it is difficult to **automate and standardize** statistical modeling in neuroimaging. In addition to costing time-limited researchers substantial effort, user-generated modeling scripts are often not **interoperable**, making it difficult to interface outputs with downstream pipelines. Finally, since such scripts are typically tied to specific analysis software, it is difficult to test the effects of software and computational environments on the final results. Altogether, these factors are significant barriers to increasing the **reproducibility and generalizability** of neuroimaging results, and we believe that we can make progress by promoting the formal specification of neuroimaging analysis models.

### Scope and limitations

The current specification deliberately focuses on the family of common general(ized) linear mixed models. Although in practice this specification was designed to operate on any BIDS-compliant datasets, the specification has been primarily tested with task-based fMRI data, and may require future extensions and software implementations to operate on other neuroimaging modalities.

Other use cases that are possible but not thoroughly tested include: voxel-based morphometry (VBM), region of interest (ROI) analyses and contrasts between multiple tasks. In addition, the current specification is designed to operate on a single set of inputs at a time, and therefore cannot support multimodal analyses in a single model. Finally, there is currently no way to specify more sophisticated models, such as arbitrary covariance structures. We welcome contributions to showcase the use of the specification on these untested use cases, as well as proposals to extend the specification to support a broader range of analyses!
