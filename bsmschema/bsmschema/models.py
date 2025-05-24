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

import sys
from typing import Optional, Literal, Any, Union, TYPE_CHECKING
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

# Hack to avoid unnecessary verbosity when generating documentation
# Has no impact on emitted JSON, only on whether Python will attempt to cast instead of error
if not TYPE_CHECKING and 'sphinxcontrib.autodoc_pydantic' in sys.modules:  # pragma: no cover
    StrictStr = str  # noqa: F811
    StrictInt = int  # noqa: F811
    StrictFloat = float  # noqa: F811
else:
    from pydantic import StrictStr, StrictInt, StrictFloat

# Notes
# HRF model parameters are unclear how to specify
# Transformation instructions should be doable (if tedious), but unclear
# how to make the restriction to them contingent on Transformer == "pybids-transforms-v1"
# Skipping Variance structure and Error distribution for now

# Controlled vocabularies

NodeLevel = Literal[
    'Run',
    'Session',
    'Subject',
    'Dataset',
]

ModelType = Literal[
    'glm',
    'meta',
]

TransformerID = Literal['pybids-transforms-v1',]

Aggregate = Literal[
    'none',
    'mean',
    'pca',
]

StatisticalTest = Literal[
    'pass',
    't',
    'F',
]

# Aliases
Filter = dict[StrictStr, list[Any]]
VariableList = list[Union[Literal[1], StrictStr]]
Weights = list[Union[StrictInt, StrictFloat, StrictStr]]

# Python 3.10 at least weirdly annotates "X: Optional[X] = None" as NoneType
OptionalFilter = Optional[Filter]
OptionalAggregate = Optional[Aggregate]


class _BSMBase(BaseModel):
    # Docstring missing to avoid polluting every object description with this field
    # This permits users to write comments on objects.
    Description: Optional[str] = None

    model_config: dict[str, Any] = {
        'extras': 'forbid',
    }


class Edge(_BSMBase):
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

    Source: StrictStr
    """Name of :py:class:`Node`. The outputs of this node are passed to :py:attr:`Destination`."""
    Destination: StrictStr
    """Name of :py:class:`Node`. The outputs of :py:attr:`Source` are passed to this node.

    The outputs of the Source node are the inputs of the Destination node, after filtering (if any)."""
    Filter: OptionalFilter = None
    """Maps a grouping variable to a list of values to pass to Destination.
    If multiple grouping variables are passed, the result is the conjunction of filters."""


class Transformations(_BSMBase):
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
    Instructions: list[Any]
    """Sequence of instructions to pass to an implementation of :py:attr:`Transformer`.
    The format of these instructions is determined by the :py:attr:`Transformer`."""


# Python annotation hack
OptionalTransformations = Optional[Transformations]


class HRF(_BSMBase):
    """Specification of a hemodynamic response function (HRF) model.

    Most design matrix constructors permit sparse events of the form
    (onset, duration, amplitude) to be convolved by a named HRF,
    possibly with some parameters.
    Some may permit dense time series to be convolved as well.

    This specification makes no attempt to constrain the names and parameters,
    or require consistency of accepted model names across implementations.
    Implementations SHOULD fail if the model is unknown.

    Examples
    --------

    The "canonical" HRF defined in SPM:

    .. code-block:: json

        {
          "Variables": ["condition1", "condition2"],
          "Model": "spm"
        }
    """

    Variables: list[StrictStr]
    """Name of the variables to be convolved.

    These must appear in :py:attr:`Model.X`.
    """
    Model: str
    """Name of a hemodynamic model.

    Known model names include:

    * ``"spm"``
    * ``"spm + derivative"``
    * ``"spm + derivative + dispersion"``
    * ``"glover"``
    * ``"glover + derivative"``
    * ``"glover + derivative + dispersion"``
    * ``"afni"``
    * ``"fir"``

    The list of supported models is expandable and limited by the estimator, not the specification.
    Note that ``"glover"`` is the default "Gamma" HRF in FSL.
    """
    Parameters: Optional[dict[str, Any]] = None
    """Parameters to the hemodynamic model.

    Options will be software specific and are not controlled.
    For ``"fir"``, the parameter ``"fir_delays"`` is required.
    """


# Python annotation hack
OptionalHRF = Optional[HRF]


class Options(_BSMBase):
    """Estimation options that are common to multiple estimation packages."""

    HighPassFilterCutoffHz: Optional[float] = None
    """The cutoff frequency, in Hz, for a high-pass filter."""
    LowPassFilterCutoffHz: Optional[float] = None
    """The cutoff frequency, in Hz, for a low-pass filter."""
    ReplaceVariables: Optional[dict[StrictStr, Any]] = None
    """Allows a specification of design matrix columns that are to be replaced by the estimating software.
    Keys are the names of columns to replace; values are unconstrained,
    and can be anything that helps the receiving software understand what is intended.
    For example, it is relatively common to want to include a voxel-specific timecourse as a covariate.
    In this case, the expectation is that the user will have constructed a dummy column as a placeholder
    (e.g., by adding a constant column to events.tsv files), and then indicate (via ReplaceVariables)
    how the receiving software should inject new values."""
    Mask: Optional[Filter] = None
    """BIDS entities specifying a mask file from the input dataset.
    For example, {"desc": "brain", "suffix": "mask"}."""
    Aggregate: OptionalAggregate = None
    """Method of combining time series within each value in the Mask.
    The following values are valid: "none", "mean", "pca".
    "none" (the default) indicates no dimensionality reduction; a separate timecourse is returned for each voxel
    that contains at least one non-zero value in its timecourse.
    "mean" returns the average of all voxels within each discrete non-zero value found in the image.
    "pca" returns the first principal component of all voxels within each discrete non-zero value found in the image."""


# Python annotation hack
OptionalOptions = Optional[Options]


class Contrast(_BSMBase):
    r"""Contrasts are weighted sums of parameter estimates (betas) generated by a model fit.

    ``Contrast`` defines the structure of the elements of the :py:attr:`Node.Contrasts` list.

    Along with :py:class:`DummyContrasts`, Contrasts define the outputs of a :py:class:`Node`.

    While ``"t"`` and ``"pass"`` contrasts are passed as inputs to the next node, ``"F"``
    contrasts are terminal and are not passed as inputs to following :py:class:`Node`\s.

    Examples
    --------

    Subtract two conditions:

    .. code-block:: json

        {
          "Name": "a_vs_b",
          "ConditionList": ["A", "B"],
          "Weights": [1, -1],
          "Test": "t"
        }

    Contrast one condition to the average of two others:

    .. code-block:: json

        {
          "Name": "a_vs_other",
          "ConditionList": ["A", "B", "C"],
          "Weights": [1, -0.5, -0.5],
          "Test": "t"
        }

    To pass an individual parameter estimate without changing its name to following nodes:

    .. code-block:: json

        {"Name": "A", "ConditionList": ["A"], "Weights": [1], "Test": "t"}
    """

    Name: StrictStr
    r"""The name of the contrast.
    Must be unique in :py:attr:`Node.Contrasts` and must not appear in
    :py:attr:`DummyContrasts.Contrasts` for the same Node.

    This name will be attached to output statistical maps via the ``"contrast"`` entity.
    """
    ConditionList: VariableList
    """A list of variables used to compute the contrast.
    Must be a subset of the variables listed in :py:attr:`Model.X`.

    The special intercept value ``1`` is permitted.
    """
    Weights: Union[Weights, list[Weights]]
    """A 1D or 2D array of weights.
    The array must have exactly the same number of total elements as in :py:attr:`ConditionList`.
    For t-tests, a 1D array must be passed. For F-tests, either a 1D or a 2D array may be passed.
    Variables are mapped 1-to-1 onto weights in the order they appear in ConditionList.
    Fractional values MAY be passed as strings (e.g., "1/3").
    """
    # Note: Keep Test synced with DummyContrasts.Test, including docstring and type
    Test: StatisticalTest
    r"""The type of test statistic to compute on the contrast.
    The special value ``"pass"`` indicates that no statistical test is to be performed.

    Note that ``"F"`` contrasts are terminal and not passed as inputs to following
    :py:class:`Node`\s."""


class DummyContrasts(_BSMBase):
    r"""Dummy contrasts are contrasts with one condition, a weight of one,
    and the same name as the condition. That is,

    ::

        "DummyContrasts": {"Contrasts": ["A", "B"], "Test": "t"}

    is equivalent to the following list of :py:class:`Contrast`\s::

        "Contrasts": [
            {"Name": "A", "ConditionList": ["A"], "Weights": [1], "Test": "t"}
            {"Name": "B", "ConditionList": ["B"], "Weights": [1], "Test": "t"}
        ]

    While ``"t"`` and ``"pass"`` contrasts are passed as inputs to the next node, ``"F"``
    contrasts are terminal and are not passed as inputs to following :py:class:`Node`\s.
    """

    Contrasts: Optional[VariableList] = None
    """A list of variables to construct DummyContrasts for.
    Must be a strict subset of ``Model.X``.
    If absent, then dummy contrasts for all variables are constructed."""
    # Note: Keep Test synced with Contrast.Test, including docstring and type
    Test: StatisticalTest
    r"""The type of test statistic to compute on the contrast.
    The special value "pass" indicates that no statistical test is to be performed.

    Note that ``"F"`` contrasts are terminal and not passed as inputs to following
    :py:class:`Node`\s."""


# Python annotation hack
OptionalDummyContrasts = Optional[DummyContrasts]


class Model(_BSMBase):
    """The model to fit to the collection of input images.

    This section defines the design matrix construction, estimator type,
    and additional options needed to estimate the model parameters.
    """

    Type: ModelType
    """The type of analysis to run.
    The following values are currently defined:
    * ``"glm"`` for general linear model,
    * ``"meta"`` for meta-analysis.
    """
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
    "?" is interpreted to match exactly one alphanumeric character.
    """
    Formula: Optional[StrictStr] = None
    """Wilkinson notation specification of a transformation of the design matrix X.
    A 1 or 0 term MUST be present to explicitly include or exclude, respectively, an intercept variable,
    to ensure consistent handling across formula interpreters."""
    HRF: OptionalHRF = None
    """A specification of the hemodynamic response function (HRF) that should be applied
    to variables by implementing software."""
    ## These are very likely getting pulled out.
    # VarianceComponents: Optional[list[dict[str, Any]]]
    # """A specification of the variance components to include in the model."""
    # ErrorDistribution: Optional[dict[str, Any]]
    # """Specifies how to model the error."""
    Options: OptionalOptions = None
    """Estimation options that are common to multiple estimation packages."""
    Software: Optional[dict[StrictStr, dict[StrictStr, Any]]] = None
    """This section allows one to specify any software-specific estimation parameters.
    Each key in the object is the name of the software package (FSL, SPM, etc.),
    and the value is an object containing software-specific parameters.
    The BIDS Stats Models spec makes no attempt to control the vocabulary available for
    use in any particular software package;
    we expect that the developers of each package will, over time, fill in these specifications."""


class Node(_BSMBase):
    """A node represents an estimator that applies to a given level of analysis.
    It contains sufficient information to construct a design matrix, estimate
    parameter weights (betas) and construct contrasts.
    """

    Level: NodeLevel
    """Level of analysis being described."""
    Name: StrictStr
    r"""The name of the node. Must be unique in :py:attr:`BIDSStatsModel.Nodes`.

    This name is used by :py:class:`Edge`\s to connect two :py:class:`Node`\s.
    """
    GroupBy: list[StrictStr]
    """The output statistical maps received from the input node are split along
    unique combinations of the grouping variables and passed to the model as subsets.
    If empty, all inputs are passed to a single model to fit.
    Reserved strings include: "run", "session", "subject", and "contrast".
    Any metadata field may be used as a grouping variable."""
    Transformations: OptionalTransformations = None
    """Specification of transformations to be applied to variables before the construction of the model."""
    Model: Model
    """What model parameters should be included, and how the errors are specified."""
    Contrasts: Optional[list[Contrast]] = None
    """How to linearly weight/combine design matrix columns
    to generate contrast maps and (optionally) run statistical tests."""
    DummyContrasts: OptionalDummyContrasts = None
    """A convenient shortcut for specifying contrasts;
    allows automatic creation of indicator contrasts
    for either all variables in the design matrix, or all named variables."""


class BIDSStatsModel(_BSMBase):
    """A BIDS Stats Model is a JSON file that defines one or more hierarchical models
    on brain imaging data.

    A hierarchical model is a sequence of estimator **nodes**. These nodes are connected
    via **edges** to form a directed, acyclic graph. The graph contains a single "root"
    node, which only has outgoing edges, and may have many "leaf" nodes that only have
    incoming edges. Each path from the root to a leaf may be thought of as a single
    hierarchical model.
    """

    Name: StrictStr
    """A name identifying the model, ideally short.
    While no hard constraints are imposed on the specific format of the name,
    each model's name should be unique for any given BIDS project
    (i.e., if a single BIDS project contains multiple model specifications in different files and/or folders,
    care should be taken to ensure that each model has a unique name)."""

    BIDSModelVersion: StrictStr
    """A string identifying the version of the specification adhered to.
    Note this is different from BIDSVersion"""

    Description: Optional[StrictStr] = None
    """A concise verbal description of the model."""

    Input: Optional[Filter] = None
    """Dictionary specification of input images"""

    Nodes: list[Node]
    """A list of analysis nodes. The ordering of this list is significant if Edges is absent."""

    Edges: Optional[list[Edge]] = None
    """A list of edges between analysis nodes. If absent, the nodes are connected in the sequence presented in Nodes."""


class ExplainerModel(BaseModel):
    """This is an example model.

    In schema terms, the structure that defines a JSON object is a "model". To avoid
    confusion with BIDS Stats Models and more general notions of mathematical or
    statistical models, we will use "schema model" to unambiguously refer to this concept.

    A schema model defines a JSON object with fields that have both a name and a type,
    where "type" indicates the range of acceptable values.

    Below are a number of fields that demonstrate the types we use in this specification.
    These types can be mixed and matched somewhat.
    Probably the most complex-looking field is :py:attr:`Contrast.Weights`.
    """

    StringField: str
    """This field is called ``StringField`` and has type ``str``.

    This type indicates that any string is acceptable, while other types (even string-like)
    are unacceptable.

    Valid example::

        {"StringField": "any string value"}

    Invalid examples::

        {"StringField": 0}
        {"StringField": ["list", "of", "strings"]}
    """
    IntField: str
    """This strict integer field must have integer values.

    Valid example::

        {"IntField": 0}

    Invalid examples::

        {"IntField": 1.0}
        {"IntField": "2"}
    """
    SomeOptions: Literal[1, 'stringval']
    """The ``Literal`` type allows a specific value or set of values.

    Valid examples::

        {"SomeOptions": 1}
        {"SomeOptions": "stringval"}

    Invalid examples::

        {"SomeOptions": "1"}
        {"SomeOptions": "differentstringval"}
        {"SomeOptions": 2.0}
    """
    ArrayOfInts: list[str]
    """JSON arrays appear as ``list`` types, and ``list[str]`` means
    the values must be integers.

    Valid example::

        {"ArrayOfInts": [1, 2]}
    """
    Object: dict[str, Any]
    """JSON objects appear as ``dict`` types.

    The general form is ``dict[str, <value-type>]``, because the field name
    in a JSON object is always a string.
    To allow for any values, including integers, strings or nested types, we
    use ``Any``.

    Valid example::

        {"Object": {"key1": "stringval", "key2": 1}}

    We use these when objects with arbitrary names can be used. If the full list
    of valid names is known, we define a new schema model.
    """
    ObjectOfObjects: dict[str, dict[str, Any]]
    """ Nested objects can start to have hairy type signatures.

    Because ``dict[str, <value-type>]`` is the general form for objects,
    the general form for objects of objects is
    ``dict[str, dict[str, <value-type>]]``.

    The actual result is fairly straightforward, though::

        {
          "ObjectOfObjects": {
            "field1": {"subfield": "value of ObjectOfObjects.field1.subfield"},
            "field2": {"intsubfield": 1}
          }
        }
    """
    ModelField: DummyContrasts
    """Schema models are nested objects with pre-determined names and types.

    This is a specialized version of ``Object``, and you can follow the link in the
    type to learn more.

    Here, the :py:class:`DummyContrasts` model defines the structure of the object.

    Valid example::

        {"ModelField": {"Contrasts": ["contrast1", "contrast2"], "Test": "t"}}
    """
    UnionField: Union[str, str]
    """Unions mean that a value could take multiple types.

    Valid examples::

        {"UnionField": 1}
        {"UnionField": "stringval"}

    Invalid examples::

        {"UnionField": 2.0}
    """
    OptionalField: Optional[str] = None
    """``OptionalField`` could be present or absent.

    Up to now, all fields have been required. If a field is optional, its type will be
    wrapped in ``Optional[]`` and will not have ``[Required]`` in its signature.
    """
    ListOrListOfLists: Union[list[int], list[list[int]]]
    """A 1- or 2D array of integers.

    To allow this form, we need to use the ``Union`` type with ``list[]`` and
    ``list[list[]]``. At the "bottom" of the type is an integer.

    :py:attr:`Contrast.Weights` has this form, but instead of ``int``, it
    permits integers, floats or strings because it is intended to allow values
    like ``0.5`` or ``"-1/3"``.
    """
