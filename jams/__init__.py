#!/usr/bin/env python
"""Top-level module for JAMS"""

import os
from importlib import resources
from itertools import chain

# Import the necessary modules
from .exceptions import *
from . import util
from . import schema
from . import eval
from . import sonify
from .version import version as __version__

from .core import *
from .nsconvert import convert
from .schema import list_namespaces


# # Populate the namespace mapping
# for ns in chain(*map(lambda p: p.rglob('*.json'), resources.files('jams.schemata.namespaces').iterdir())):

# Ensure that the package exists and contains the expected resources
try:
    resource_path = resources.files('jams.schemata.namespaces')
    if resource_path is None:
        raise ValueError("Resource path is None")

    # Iterate over the directories and search for JSON files
    json_files = chain(*map(lambda p: p.rglob('*.json'), resource_path.iterdir()))

    # Check if any JSON files were found
    for ns in json_files:
        schema.add_namespace(ns)
except Exception as e:
    print(f"An error occurred: {e}")

# Populate local namespaces

if 'JAMS_SCHEMA_DIR' in os.environ:
    for ns in util.find_with_extension(os.environ['JAMS_SCHEMA_DIR'], 'json'):
        schema.add_namespace(ns)
