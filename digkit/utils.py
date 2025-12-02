import json
import importlib.resources
import digkit.data


def load_json(filename: str):
    """
    Load a JSON file stored in the digkit/data package.

    Works both in development and when installed via pip.
    """
    with importlib.resources.open_text(digkit.data, filename) as f:
        return json.load(f)
