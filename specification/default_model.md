# Creating a default model

It is possible to write a "first draft" for your model by using Pybids or
bids-matlab.

See below for code snippet showing how to do it with each package.

## pybids

https://bids-standard.github.io/pybids/generated/bids.modeling.auto_model.html

```python
from bids import BIDSLayout
from bids.modeling import auto_model
import json

# indexing the dataset
layout = BIDSLayout(path_to_dataset)

# creating the default model
model = auto_model(layout, one_vs_rest=True)

# saving to a JSON file
with open("model-default_smdl.json", "w") as outfile:
    json.dump(model[0], outfile)
```

## bids-matlab

https://bids-matlab.readthedocs.io/en/latest/stats_model.html#+bids.Model.default

```matlab
% indexing the dataset
BIDS = bids.layout(path_to_dataset);

% create an empty model
bm = bids.Model();
% creating the default model for our dataset
bm = bm.default(BIDS);

% saving to a JSON file
filename = fullfile(pwd, 'model-default_smdl.json');
bm.write(filename);
```
