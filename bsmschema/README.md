# BIDS Stats Models Schema

This package contains a [Pydantic](https://pydantic-docs.helpmanual.io/) description of the
BIDS Stats Models format, which can be used as a schema validator or generate JSON
schema for independent validation.

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
