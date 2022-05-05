"""
==================================
BIDS Stats Models Object Reference
==================================

This document defines the valid keys and values in a BIDS Stats Model.
A BIDS Stats Model is defined in a `JSON <https://www.json.org/json-en.html>`_ document.

"""
from enum import Enum
from typing import List, Optional, Dict, Literal, Any, Union
from pydantic import BaseModel

__all__ = [
    'BIDSStatsModel',
    'Node',
    'Edge',
    'Transformations',
    'Model',
    'HRF',
    'Options',
    'Contrast',
    'DummyContrasts',
]

# Notes
# HRF model parameters are unclear how to specify
# Transformation instructions should be doable (if tedious), but unclear
# how to make the restriction to them contingent on Transformer == "pybids-transforms-v1"
# Skipping Variance structure and Error distribution for now

# Controlled vocabularies

NodeLevel = Literal[
    "Run",
    "Session",
    "Subject",
    "Dataset",
]

ModelType = Literal[
    "glm",
    "meta",
]

TransformerID = Literal[
    "pybids-transforms-v1",
]

Aggregate = Literal[
    "none",
    "mean",
    "pca",
]

HRFModel = Literal[
    "DoubleGamma",
    "Gamma",
    "FiniteImpulseResponse",
]

StatisticalTest = Literal[
    "t",
    "F",
]

# Aliases
Filter = Dict[str, List[Any]]
Weights = List[Union[int, float, str]]



class Edge(BaseModel):
    r"""An ``Edge`` connects two ``Node``\s, indicating the outputs (contrasts) of the ``Source`` node are to be made available as inputs to the ``Destination`` node.

    Contrasts may be filtered by any metadata field, including entities. Each contrast has an additional entity ``"contrast"`` that may be used to filter contrasts by name.
    """
    Source: str
    """Name of node. The outputs of this node are passed to Destination."""
    Destination: str
    """Name of node. The outputs of Source are passed to this node. The outputs of the Source node are the inputs of the Destination node, after filtering (if any)."""
    Filter: Optional[Filter]
    """Maps a grouping variable to a list of values to pass to Destination. If multiple grouping variables are passed, the result is the conjunction of filters."""


class Transformations(BaseModel):
    Transformer: TransformerID
    """Name of the specification of an instruction set."""
    Instructions: List[Any]
    """Sequence of instructions to pass to an implementation of Transformer. The format of these instructions is determined by the Transformer."""


class Parameters(BaseModel):
    PeakDelay: float
    """Delay, in seconds, from onset to peak response. Applies to models: Gamma, DoubleGamma."""
    PeakDispersion: float
    """Width of peak. Applies to models: Gamma, DoubleGamma."""
    UndershootDelay: float
    """Delay, in seconds, from onset to undershoot response. Applies to model: DoubleGamma."""
    UndershootDispersion: float
    """Width of undershoot. Applies to model: DoubleGamma."""
    PeakUndershootRatio: float
    """Peak-to-undershoot ratio. Applies to model: DoubleGamma."""
    Derivatives: int
    """Order of derivatives to include. 1 indicates the first derivative, while 2 indicates the first and second derivative. Applies to models: Gamma, DoubleGamma."""
    Delays: List[int]
    """List of delays, in scans, for impulse responses. Applies to model: FiniteImpulseResponse."""


class HRF(BaseModel):
    Variables: List[str]
    """Name of the variables to be convolved."""
    Model: HRFModel
    """Name of a hemodynamic model."""
    Parameters: Optional[Parameters]
    """Parameters to the hemodynamic model."""


class Options(BaseModel):
    HighPassFilterCutoffHz: Optional[float]
    """The cutoff frequency, in Hz, for a high-pass filter."""
    LowPassFilterCutoffHz: Optional[float]
    """The cutoff frequency, in Hz, for a low-pass filter."""
    ReplaceVariables: Optional[Dict[str, Any]]
    """Allows a specification of design matrix columns that are to be replaced by the estimating software. Keys are the names of columns to replace; values are unconstrained, and can be anything that helps the receiving software understand what is intended. For example, it is relatively common to want to include a voxel-specific timecourse as a covariate. In this case, the expectation is that the user will have constructed a dummy column as a placeholder (e.g., by adding a constant column to events.tsv files), and then indicate (via ReplaceVariables) how the receiving software should inject new values."""
    Mask: Optional[Filter]
    """BIDS entities specifying a mask file from the input dataset. For example, {"desc": "brain", "suffix": "mask"}."""
    Aggregate: Optional[Aggregate]
    """Method of combining time series within each value in the Mask. The following values are valid: “none”, “mean”, “pca”. “none” (the default) indicates no dimensionality reduction; a separate timecourse is returned for each voxel that contains at least one non-zero value in its timecourse. “mean” returns the average of all voxels within each discrete non-zero value found in the image. “pca” returns the first principal component of all voxels within each discrete non-zero value found in the image."""


class Contrast(BaseModel):
    Name: str
    """The name of the contrast. Must be unique."""
    ConditionList: List[str]
    """A list of variables used to compute the contrast. Must be a strict subset of the list of X available in the namespace (i.e., either produced by the model section, or available via propagation from previous nodes)."""
    Weights: Optional[Union[Weights, List[Weights]]]
    """A 1D or 2D array of weights. The array must have exactly the same number of total elements as in ConditionList. For t-tests, a 1D array must be passed. For F-tests, either a 1D or a 2D array may be passed. Variables are mapped 1-to-1 onto weights in the order they appear in ConditionList. If no weights are passed, unit weights are assigned to all variables (i.e., if variables = [‘A’, ‘B’, ‘C’], weights will be [1, 1, 1]). Fractional values MAY be passed as strings (e.g., “1/3")."""
    Test: Optional[StatisticalTest]
    """The type of test statistic to compute on the contrast. If provided, must be one of “t”,  “F”. Alternatively, if no Test is provided, no statistical test will be performed. This allows the contrasts section to be used to generate weighted sums of parameter estimates without computing associated statistical maps (e.g., to compute beta maps for individual subjects that are to be fed to the group level, without conducting single-subject statistical tests)."""


class DummyContrasts(BaseModel):
    Contrasts: List[str]
    """A list of variables used to compute the contrast. Must be a strict subset of the list of X available in the namespace (i.e., either produced by the model section, or available via propagation from previous nodes)."""
    Test: Optional[StatisticalTest]
    """Indicates the contrast type that will be applied for each dummy contrast in the section."""


class Model(BaseModel):
    Type: ModelType
    """The type of analysis to run. The following values are currently defined: "glm" for general linear model, "meta" for meta-analysis."""
    X: List[Union[str, Literal[1]]]
    """A list of predictors to include in the model. At present, the BIDS-Model specification only handles traditional GLM analyses, so the assumption is always that brain activation is being predicted from one or more predictors. All variables listed in the X field will be included as columns in the design matrix. Each variable name specified in X must exactly match one of the variables available in the namespace. Any available variables that are not explicitly named in X will be omitted from the model. Partial matching is supported and can be specified using wildcard characters; for example, use “aroma_motion_*” to specify all of the aroma components found in the confounds file. Following standard Unix-style glob rules, “*” is interpreted to match 0 or more alphanumeric characters, and “?” is interpreted to match exactly one alphanumeric character."""
    Formula: Optional[str]
    """Wilkinson notation specification of a Transformation of the design matrix X. A 1 or 0 term MUST be present to explicitly include or exclude, respectively, an intercept variable, to ensure consistent handling across formula interpreters."""
    HRF: Optional[HRF]
    """A specification of the hemodynamic response function (HRF) that should be applied to variables by implementing software."""
    ## These are very likely getting pulled out.
    # VarianceComponents: Optional[List[Dict[str, Any]]]
    # """A specification of the variance components to include in the model."""
    # ErrorDistribution: Optional[Dict[str, Any]]
    # """Specifies how to model the error."""
    Options: Optional[Options]
    """Estimation options that are common to multiple estimation packages."""
    Software: Optional[List[Dict[str, Dict[str, Any]]]]
    """This section allows one to specify any software-specific estimation parameters. Each value in the list is an object, with the key being the name of the software package (FSL, SPM, etc.), and the value being an object containing software-specific parameters. The BIDS-Model spec makes no attempt to control the vocabulary available for use in any particular software package; we expect that the developers of each package will, over time, fill in these specifications."""


class Node(BaseModel):
    """A node represents an estimator that applies to a given level of analysis.
    It contains sufficient information to construct a design matrix, estimate
    parameter weights (betas) and construct contrasts.
    """
    Level: NodeLevel
    """Level of analysis being described."""
    Name: str
    """Name of node."""
    GroupBy: List[str]
    """The output statistical maps received from the input node are split along unique combinations of the grouping variables and passed to the model as subsets. If empty, all inputs are passed to a single model to fit. Reserved strings include: "run", "session", "subject", and "contrast". Any metadata field may be used as a grouping variable."""
    Transformations: Optional[Transformations]
    """Specification of transformations to be applied to variables before the construction of the model."""
    Model: Model
    """What model parameters should be included, and how the errors are specified."""
    Contrasts: Optional[List[Contrast]]
    """How to linearly weight/combine design matrix columns to generate contrast maps and (optionally) run statistical tests."""
    DummyContrasts: Optional[DummyContrasts]
    """A convenient shortcut for specifying contrasts; allows automatic creation of indicator contrasts for either all variables in the design matrix, or all named variables."""


class BIDSStatsModel(BaseModel):
    """A BIDS Stats Model is a JSON file that defines one or more hierarchical models
    on brain imaging data.

    A hierarchical model is a sequence of estimator **nodes**. These nodes are connected
    via **edges** to form a directed, acyclic graph. The graph contains a single "root"
    node, which only has outgoing edges, and may have many "leaf" nodes that only have
    incoming edges. Each path from the root to a leaf may be thought of as a single
    hierarchical model.
    """
    Name: str
    """A name identifying the model, ideally short. While no hard constraints are imposed on the specific format of the name, each model’s name should be unique for any given BIDS project (i.e., if a single BIDS project contains multiple model specifications in different files and/or folders, care should be taken to ensure that each model has a unique name)."""

    BIDSModelVersion: str
    """A string identifying the version of the specification adhered to. Note this is different from BIDSVersion"""

    Description: Optional[str]
    """A concise verbal description of the model."""

    Input: Optional[Filter]
    """Dictionary specification of input images"""

    Nodes: List[Node]
    """A list of analysis nodes. The ordering of this list is significant if Edges is absent."""

    Edges: Optional[List[Edge]]
    """A list of edges between analysis nodes. If absent, the nodes are connected in the sequence presented in Nodes."""
