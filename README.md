# BIDS Stats Models Specification

This repository is intended to be the authoritative reference for the BIDS Stats Models
specification. It consists of two parts:

1) `bsmschema`, a [Pydantic](https://pydantic-docs.helpmanual.io/) description of the
   BIDS Stats Models files, which can be used as a schema validator or generate JSON
   schema for independent validation.
2) `specification`, a [JupyterBook](https://jupyterbook.org/) website that includes
   more human readable introductions and explanations, as well as a reference document
   for `bsmschema`.

## Installing `bsmschema`

### From the Python package index

```
pip install bsmschema
```

### From source

```
git clone https://github.com/bids-standard/stats-models.git
pip install stats-models/bsmschema
```

You may wish to install in editable mode, to ensure that your changes get propagated without
reinstalling:

```
pip install -e stats-models/bsmschema
```

## How to run schema validator

```python
from bsmschema.models import BIDSStatsModel
BIDSStatsModel.parse_file('stats-models/specification/examples/model-example_smdl.json')
```

## Building the documentation locally

1) Install the requirements, including the local copy of `bsmschema`:

   ```
   pip install -r requirements.txt
   ```

1) Build the schema files to ensure the local validator will work:

   ```
   python -m bsmschema specification/schema
   ```


1) Build the JupyterBook:

   ```
   make build
   ```

1) Serve the built website:

   ```
   make serve
   ```
