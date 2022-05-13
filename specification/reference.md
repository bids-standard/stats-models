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

{py:class}`~bsmschema.models.BIDSStatsModel` is the top-level structure,
while the remaining classes define sub-structures.
To demonstrate this hierarchy, here we show the [example model](guide.md#example-model)
in this structure, with missing fields rendered as `None`:

```{code-cell} python3
---
tags: ["remove_cell"]
---
# The above tag ensures this does not show in the page.

from pathlib import Path
from myst_nb import glue
from IPython.display import Code
import black
from bsmschema.models import BIDSStatsModel

orig = Path('examples/model-example_smdl.json').read_text()
model = BIDSStatsModel.parse_raw(orig)

# Here we use MyST "glue" to insert generated structures in tabs
glue("structured", Code(black.format_str(repr(model), mode=black.mode.Mode()), language="python"))
glue("orig_json", Code(orig, language="json"))
```

````{tabbed} Structure
```{glue:} structured
```
````

````{tabbed} Original JSON
```{glue:} orig_json
```
````
