# BIDS Stats Models

BIDS Stats Models (BSM) is a specification for describing statistical models for neuroimaging data. Its purpose is prescriptive (e.g. a recipe of how to fit a model), rather than descriptive (e.g., summary of models that have already been fit). 

At the core of BSM is a single, machine-readable JSON document that allows users to define a fully reproducible statistical model across multiple stages of analysis. Models are represented as a graph composed on Nodes and Edges, enabling the expression of a wide range of models. A BSM—in combination with a preprocessed BIDS dataset—is sufficient to execute statistical models, with minimal configuration and manual intervention required from the user. 

### Why?

Although progress has been made in standardizing neuroimaging pipelines, model fitting requires a high degree of flexibility, resulting in heterogeneous scripts that are often not **reproducible**. Upon publication, models are often verbally described, making it difficult to reproduce analyses from published studies. Even when analysis scripts are shared, they often lack **transparency**, making it difficult for other researchers to interpret and apply the same model to a different dataset. 

*BIDS Stats Models* aims to facilitate the development **automated and standardized** neuroimaging model fitting pipelines, encouraging **reproducible and generalizable scientific** practice. In addition, by promoting the development of an ecosystem of easy to use and **interoperable** tools, BSM aims to facilitate the process of building and fitting statistical models on neuroimaging data.

### Scope and limitations

The current specification deliberately focuses on the family of common general(ized) linear mixed models (GLMs). Although the goal of BSM is to specify models for any BIDS-compliant datasets, the specification has been primarily tested with task-based fMRI data and may require future extensions and software implementations to operate on other neuroimaging modalities (e.g. EEG, MEG, etc.)

Other use cases that are possible but not thoroughly tested include: voxel-based morphometry (VBM), region of interest (ROI) analyses and contrasts between multiple tasks. In addition, the current specification is designed to operate on a single set of inputs at a time, and therefore cannot support multimodal analyses in a single model. Finally, there is currently no way to specify more sophisticated models, such as arbitrary covariance structures. We welcome contributions to showcase the use of the specification on these untested use cases, as well as proposals to extend the specification to support a broader range of analyses!
