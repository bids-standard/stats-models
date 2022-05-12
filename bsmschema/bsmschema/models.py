"""
The objects defined here are nested as follows:

* :py:class:`BIDSStatsModel`
   * :py:class:`Node`
      * :py:class:`Transformations`
      * :py:class:`Model`
         * :py:class:`HRF`
         * :py:class:`Options`
      * :py:class:`Contrast`
      * :py:class:`DummyContrasts`
   * :py:class:`Edge`

Note that these are the structured and validatable objects.

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
    "skip",
    "t",
    "F",
]

# Aliases
Filter = Dict[str, List[Any]]
VariableList = List[Union[str, Literal[1]]]
Weights = List[Union[int, float, str]]


class _Commentable(BaseModel):
    # Docstring missing to avoid polluting every object description with this field
    # This permits users to write comments on objects.
    Description: Optional[str]


class Edge(_Commentable):
    r"""An Edge connects two :py:class:`Node`\s, indicating the outputs (contrasts) of
    the :py:attr:`Source` Node are to be made available as inputs to the
    :py:attr:`Destination` Node.

    Contrasts may be filtered by any metadata field, including entities.
    Each contrast has an additional entity ``"contrast"`` that may be used to filter contrasts by name.

    Examples
    --------

    .. code-block:: json

       {
         "Source": "subject",
         "Destination": "dataset"
       }

    .. code-block:: json

       {
         "Source": "subject",
         "Destination": "dataset",
         "Filter": {"contrast": ["contrast1", "contrast2"]}
       }
    """
    Source: str
    """Name of :py:class:`Node`. The outputs of this node are passed to :py:attr:`Destination`."""
    Destination: str
    """Name of :py:class:`Node`. The outputs of :py:attr:`Source` are passed to this node.

    If :py:attr:`Filter` is defined,
    The outputs of the Source node are the inputs of the Destination node, after filtering (if any)."""
    Filter: Optional[Filter]
    """Maps a grouping variable to a list of values to pass to Destination.
    If multiple grouping variables are passed, the result is the conjunction of filters."""


class Transformations(_Commentable):
    """Transformations describe modifications of variables to prepare a design matrix.

    This field is indirect, with a :py:attr:`Transformer` name identifying an instruction
    set, and a sequence of :py:attr:`Instructions`.

    A Transformer accepts data frames of sparse (onset, duration, amplitude) and
    dense (onset, sampling rate, values) variables along with the list of Instructions,
    and then return a new set of sparse and/or dense variables.

    Examples
    --------

    .. code-block:: json

       {
         "Transformer": "pybids-transforms-v1",
         "Instructions": [
           {
             "Name": "Factor",
             "Input": ["trial_type"]
           },
           {
             "Name": "Convolve",
             "Model": "spm",
             "Input": ["trial_type.cond1", "trial_type.cond2"]
           }
         ]
       }

    """
    Transformer: TransformerID
    """Name of the specification of an instruction set."""
    Instructions: List[Any]
    """Sequence of instructions to pass to an implementation of :py:attr:`Transformer`.
    The format of these instructions is determined by the :py:attr:`Transformer`."""


class Parameters(_Commentable):
    """Parameters to an :py:class:`HRF` model."""
    PeakDelay: Optional[float]
    """Delay, in seconds, from onset to peak response.
    Applies to models: Gamma, DoubleGamma."""
    PeakDispersion: Optional[float]
    """Width of peak.
    Applies to models: Gamma, DoubleGamma."""
    UndershootDelay: Optional[float]
    """Delay, in seconds, from onset to undershoot response.
    Applies to model: DoubleGamma."""
    UndershootDispersion: Optional[float]
    """Width of undershoot.
    Applies to model: DoubleGamma."""
    PeakUndershootRatio: Optional[float]
    """Peak-to-undershoot ratio.
    Applies to model: DoubleGamma."""
    Derivatives: Optional[int]
    """Order of derivatives to include. 1 indicates the first derivative,
    while 2 indicates the first and second derivative.
    Applies to models: Gamma, DoubleGamma."""
    Delays: Optional[List[int]]
    """List of delays, in scans, for impulse responses.
    Applies to model: FiniteImpulseResponse."""


class HRF(_Commentable):
    """Specification of a hemodynamic response function (HRF) model."""
    Variables: List[str]
    """Name of the variables to be convolved. These must appear in :py:attr:`Model.X`"""
    Model: HRFModel
    """Name of a hemodynamic model."""
    Parameters: Optional[Parameters]
    """Parameters to the hemodynamic model."""


class Options(_Commentable):
    """ Options
    """
    HighPassFilterCutoffHz: Optional[float]
    """The cutoff frequency, in Hz, for a high-pass filter."""
    LowPassFilterCutoffHz: Optional[float]
    """The cutoff frequency, in Hz, for a low-pass filter."""
    ReplaceVariables: Optional[Dict[str, Any]]
    """Allows a specification of design matrix columns that are to be replaced by the estimating software.
    Keys are the names of columns to replace; values are unconstrained,
    and can be anything that helps the receiving software understand what is intended.
    For example, it is relatively common to want to include a voxel-specific timecourse as a covariate.
    In this case, the expectation is that the user will have constructed a dummy column as a placeholder
    (e.g., by adding a constant column to events.tsv files), and then indicate (via ReplaceVariables)
    how the receiving software should inject new values."""
    Mask: Optional[Filter]
    """BIDS entities specifying a mask file from the input dataset.
    For example, {"desc": "brain", "suffix": "mask"}."""
    Aggregate: Optional[Aggregate]
    """Method of combining time series within each value in the Mask.
    The following values are valid: "none", "mean", "pca".
    "none" (the default) indicates no dimensionality reduction; a separate timecourse is returned for each voxel
    that contains at least one non-zero value in its timecourse.
    "mean" returns the average of all voxels within each discrete non-zero value found in the image.
    "pca" returns the first principal component of all voxels within each discrete non-zero value found in the image."""


class Contrast(_Commentable):
    """Contrasts are weighted sums of parameter estimates (betas) generated by a model fit,
    and define the outputs of a :py:class:`Node`.

    While ``"t"`` and ``"skip"`` contrasts are passed as inputs to the next node, ``"F"``
    contrasts are terminal and are not passed as inputs to following nodes.
    """
    Name: str
    r"""The name of the contrast.
    Must be unique in :py:attr:`Node.Contrasts` and must not appear in
    :py:attr:`DummyContrasts.Contrasts` for the same Node.

    This name will be attached to output statistical maps via the ``"contrast"`` entity.
    """
    ConditionList: VariableList
    """A list of variables used to compute the contrast.
    Must be a strict subset of the variables listed in :py:attr:`Model.X`.
    """
    Weights: Union[Weights, List[Weights]]
    """A 1D or 2D array of weights.
    The array must have exactly the same number of total elements as in ConditionList.
    For t-tests, a 1D array must be passed. For F-tests, either a 1D or a 2D array may be passed.
    Variables are mapped 1-to-1 onto weights in the order they appear in ConditionList.
    Fractional values MAY be passed as strings (e.g., “1/3")."""
    # Note: Keep Test synced with DummyContrasts.Test, including docstring and type
    Test: StatisticalTest
    """The type of test statistic to compute on the contrast.
    The special value "skip" indicates that no statistical test is to be performed."""



class DummyContrasts(_Commentable):
    r"""Dummy contrasts are contrasts with one condition, a weight of one,
    and the same name as the condition. That is,

    ::

        "DummyContrasts": {"Contrasts": ["A", "B"], "Test": "t"}

    is equivalent to the following list of :py:class:`Contrast`\s::

        "Contrasts": [
            {"Name": "A", "ConditionList": ["A"], "Weights": [1], "Test": "t"}
            {"Name": "B", "ConditionList": ["B"], "Weights": [1], "Test": "t"}
        ]

    """
    Contrasts: Optional[VariableList]
    """A list of variables to construct DummyContrasts for.
    Must be a strict subset of ``Model.X``.
    If absent, then dummy contrasts for all variables are constructed."""
    # Note: Keep Test synced with Contrast.Test, including docstring and type
    Test: StatisticalTest
    """The type of test statistic to compute on the contrast.
    The special value "skip" indicates that no statistical test is to be performed."""



class Model(_Commentable):
    """Model
    """
    Type: ModelType
    """The type of analysis to run.
    The following values are currently defined:
    "glm" for general linear model,
    "meta" for meta-analysis."""
    X: VariableList
    """A list of predictors to include in the model.
    At present, the BIDS-Model specification only handles traditional GLM analyses,
    so the assumption is always that brain activation is being predicted from one or more predictors.
    All variables listed in the X field will be included as columns in the design matrix.
    Each variable name specified in X must exactly match one of the variables available in the namespace.
    Any available variables that are not explicitly named in X will be omitted from the model.
    Partial matching is supported and can be specified using wildcard characters;
    for example, use "aroma_motion_*" to specify all of the aroma components found in the confounds file.
    Following standard Unix-style glob rules,
    "*" is interpreted to match 0 or more alphanumeric characters, and
    "?" is interpreted to match exactly one alphanumeric character."""
    Formula: Optional[str]
    """Wilkinson notation specification of a Transformation of the design matrix X.
    A 1 or 0 term MUST be present to explicitly include or exclude, respectively, an intercept variable,
    to ensure consistent handling across formula interpreters."""
    HRF: Optional[HRF]
    """A specification of the hemodynamic response function (HRF) that should be applied
    to variables by implementing software."""
    ## These are very likely getting pulled out.
    # VarianceComponents: Optional[List[Dict[str, Any]]]
    # """A specification of the variance components to include in the model."""
    # ErrorDistribution: Optional[Dict[str, Any]]
    # """Specifies how to model the error."""
    Options: Optional[Options]
    """Estimation options that are common to multiple estimation packages."""
    Software: Optional[List[Dict[str, Dict[str, Any]]]]
    """This section allows one to specify any software-specific estimation parameters.
    Each value in the list is an object, with the key being the name of the software package (FSL, SPM, etc.),
    and the value being an object containing software-specific parameters.
    The BIDS-Model spec makes no attempt to control the vocabulary available for use in any particular software package;
    we expect that the developers of each package will, over time, fill in these specifications."""


class Node(_Commentable):
    """A node represents an estimator that applies to a given level of analysis.
    It contains sufficient information to construct a design matrix, estimate
    parameter weights (betas) and construct contrasts.
    """
    Level: NodeLevel
    """Level of analysis being described."""
    Name: str
    r"""The name of the node. Must be unique in :py:attr:`BIDSStatsModel.Nodes`.

    This name is used by :py:class:`Edge`\s to connect two :py:class:`Node`\s.
    """
    GroupBy: List[str]
    """The output statistical maps received from the input node are split along
    unique combinations of the grouping variables and passed to the model as subsets.
    If empty, all inputs are passed to a single model to fit.
    Reserved strings include: "run", "session", "subject", and "contrast".
    Any metadata field may be used as a grouping variable."""
    Transformations: Optional[Transformations]
    """Specification of transformations to be applied to variables before the construction of the model."""
    Model: Model
    """What model parameters should be included, and how the errors are specified."""
    Contrasts: Optional[List[Contrast]]
    """How to linearly weight/combine design matrix columns
    to generate contrast maps and (optionally) run statistical tests."""
    DummyContrasts: Optional[DummyContrasts]
    """A convenient shortcut for specifying contrasts;
    allows automatic creation of indicator contrasts
    for either all variables in the design matrix, or all named variables."""


class BIDSStatsModel(_Commentable):
    """A BIDS Stats Model is a JSON file that defines one or more hierarchical models
    on brain imaging data.

    A hierarchical model is a sequence of estimator **nodes**. These nodes are connected
    via **edges** to form a directed, acyclic graph. The graph contains a single "root"
    node, which only has outgoing edges, and may have many "leaf" nodes that only have
    incoming edges. Each path from the root to a leaf may be thought of as a single
    hierarchical model.
    """
    Name: str
    """A name identifying the model, ideally short.
    While no hard constraints are imposed on the specific format of the name,
    each model's name should be unique for any given BIDS project
    (i.e., if a single BIDS project contains multiple model specifications in different files and/or folders,
    care should be taken to ensure that each model has a unique name)."""

    BIDSModelVersion: str
    """A string identifying the version of the specification adhered to.
    Note this is different from BIDSVersion"""

    Description: Optional[str]
    """A concise verbal description of the model."""

    Input: Optional[Filter]
    """Dictionary specification of input images"""

    Nodes: List[Node]
    """A list of analysis nodes. The ordering of this list is significant if Edges is absent."""

    Edges: Optional[List[Edge]]
    """A list of edges between analysis nodes. If absent, the nodes are connected in the sequence presented in Nodes."""
