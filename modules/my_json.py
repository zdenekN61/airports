"""Json encoding, decoding"""

import json
import os
import re

__all__ = ["to_JSON", "to_dictionary"]

# Json decoding.
def to_JSON(obj):
    return json.loads(obj)

# Json encoding.
def to_dictionary(obj):
    return json.dumps(obj)
