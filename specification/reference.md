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

# BIDS Stats Models Object Reference

This section defines the valid keys and values in a BIDS Stats Model.
A BIDS Stats Model is defined in a [JSON](https://www.json.org/json-en.html) document.

```{eval-rst}

.. currentmodule:: bsmschema.models

.. autosummary::
   :toctree: _autosummary

   BIDSStatsModel
   Node
   Transformations
   Model
   HRF
   Options
   Contrast
   DummyContrasts
   Edge
```

```{code-cell} python3
---
tags: ["hide_input"]
---

import black
from bsmschema.models import BIDSStatsModel

print(black.format_str(
    repr(BIDSStatsModel.parse_file('examples/model-example_smdl.json')),
    mode=black.mode.Mode()
))
```
