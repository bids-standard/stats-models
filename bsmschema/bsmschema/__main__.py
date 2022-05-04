import sys
from pathlib import Path
from bsmschema import models

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python -m bsmschema /path/to/schemadir")
        sys.exit(1)

    schemadir = Path(sys.argv[1]) 
    schemadir.mkdir(parents=True, exist_ok=True)
    for mname in models.__all__:
        model = getattr(models, mname)
        Path.write_text(schemadir / f"{mname}.json", model.schema_json(indent=2))
