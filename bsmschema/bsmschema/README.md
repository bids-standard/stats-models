## Installation

```bash
git clone https://github.com/bids-standard/stats-models.git
pip install stats-models/bsmschema
```

## Usage

```python
from bsmschema.models import BIDSStatsModel

BIDSStatsModel.parse_file('stats-models/specification/examples/model-example_smdl.json')
```