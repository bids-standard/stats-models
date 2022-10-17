---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# BIDS Stats Models Specification

Editors:
: [Alejandro de la Vega][] ([University of Texas at Austin][])
: [Christopher J Markiewicz][] ([Stanford University][])

---

This document contains specifications for writing BIDS Stats Models, a recipe for fitting
hierarchical statistical models to neuroimaging datasets.
This specification was developed in the [Brain Imaging Data Structure (BIDS)][BIDS] community
as BIDS Extension Proposal (BEP) 2.

The components of this specification interact,
and it is difficult to discuss one structure without referencing others.
Therefore this document makes no attempt to introduce all concepts before referring to them.
For a more graduated introduction of these concepts, please refer to the [Walkthrough](walkthrough-intro).

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL
NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and
"OPTIONAL" in this document are to be interpreted as described in
[RFC 2119].

## Status of this document

<!-- Note here the current version of the specification, once released. -->
<!--
The current released version of this specification is 1.0.
-->
The previously released version of this specification was [1.0.0rc0][].

## On-disk layout

BIDS Stats Models are [JSON][] ([RFC8259][]) documents containing the following fields:

* {py:attr}`~bsmschema.models.BIDSStatsModel.Name`
* {py:attr}`~bsmschema.models.BIDSStatsModel.BIDSModelVersion`
* {py:attr}`~bsmschema.models.BIDSStatsModel.Description`
* {py:attr}`~bsmschema.models.BIDSStatsModel.Input`
* {py:attr}`~bsmschema.models.BIDSStatsModel.Nodes`
* {py:attr}`~bsmschema.models.BIDSStatsModel.Edges`

An example top-level structure has the form:

```YAML
{
  "Name": "my_first_model",
  "BIDSModelVersion": "1.0",
  "Input": {
    "task": "motor"
  },
  "Description": "My first BIDS model: a simple 2-condition contrast.",
  "Nodes": [
    {
      "Level": "Run",
      ...
    },
    {
      "Level": "Session",
      ...
    },
    {
      "Level": "Subject",
      ...
    },
    {
      "Level": "Dataset",
      ...
    }
  ],
  "Edges": [
    ...
  ]
}
```

### Execution Graph and Data Flow

#### Nodes and Edges

#### GroupBy and Filter

### Estimation Nodes

#### Model

#### Contrasts

### Variable model and transformations protocol


<!-- Markdown link definitions -->

[1.0.0rc0]: https://docs.google.com/document/d/1IthJC7rZw_fUK7Qka4mHxSjndyrvKKRoJcvll7XQN08/edit
[BIDS]: https://bids.neuroimaging.io/
[JSON]: https://www.json.org/json-en.html
[RFC8259]: https://datatracker.ietf.org/doc/html/rfc8259
[RFC 2119]: https://datatracker.ietf.org/doc/html/rfc2119
[Alejandro de la Vega]: https://orcid.org/0000-0001-9062-3778
[University of Texas at Austin]: https://www.utexas.edu/
[Christopher J Markiewicz]: https://orcid.org/0000-0002-6533-164X
[Stanford University]: https://www.stanford.edu
