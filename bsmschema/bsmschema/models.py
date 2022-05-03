from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class Edge(BaseModel):
    Source: str
    Destination: str
    Filter: Optional[Dict[str, List[Any]]]


class NodeLevel(str, Enum):
    Run = "Run"
    Session = "Session"
    Subject = "Subject"
    Dataset = "Dataset"


class Node(BaseModel):
    """A node represents an estimator that applies to a given level of analysis.
    It contains sufficient information to construct a design matrix, estimate
    parameter weights (betas) and construct contrasts.
    """
    Level: NodeLevel
    """Level of analysis being described."""
    Name: str
    """Name of node."""


class BIDSStatsModel(BaseModel):
    Name: str
    """A name identifying the model, ideally short. While no hard constraints are imposed on the specific format of the name, each model’s name should be unique for any given BIDS project (i.e., if a single BIDS project contains multiple model specifications in different files and/or folders, care should be taken to ensure that each model has a unique name)."""

    BIDSModelVersion: str
    """A string identifying the version of the specification adhered to. Note this is different from BIDSVersion"""

    Description: Optional[str]
    """A concise verbal description of the model."""

    Input: Optional[Dict[str, List[Any]]]
    """Dictionary specification of input images"""

    Nodes: List[Node]
    """A concise verbal description of the model."""

    Edges: Optional[List[Edge]]
    """A concise verbal description of the model."""

