import pydantic
from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class Edge(BaseModel):
    Source: str
    Destination: str
    Filter: Optional[Dict[str, List[Any]]]


class BIDSStatsModel(BaseModel):
    Name: str
    BIDSModelVersion: str
    Description: Optional[str]
    Input: Optional[Dict[str, List[Any]]]
    Nodes: List
    Edges: Optional[List[Edge]]
