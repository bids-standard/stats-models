from bsmschema.models import BIDSStatsModel

from . import data


def test_load():
    example = data.load.readable('examples', 'model-example_smdl.json')
    model = BIDSStatsModel.model_validate_json(example.read_text())

    assert model.Name == 'my_first_model'
    assert len(model.Nodes) == 3
    assert len(model.Edges) == 2
