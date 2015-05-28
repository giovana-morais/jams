#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''JAMS task-specific namespaces'''

import json
import os

__all__ = ['add_namespace', 'schema', 'is_dense']

__NAMESPACE__ = dict()


def add_namespace(filename):
    '''Add a namespace definition to our working set.

    Namespace files consist of partial JSON schemas defining the behavior
    of the `value` and `confidence` fields of an Annotation.

    Parameters
    ----------
    filename : str
        Path to json file defining the namespace object
    '''
    with open(filename, mode='r') as fileobj:
        __NAMESPACE__.update(json.load(fileobj))


def schema(namespace, default=None):
    '''Construct a validation schema for a given namespace.

    Parameters
    ----------
    namespace : str
        Namespace key identifier (eg, 'beat' or 'segment_tut')

    default : schema
        A pre-existing schema to append into

    Returns
    -------
    schema : dict
        JSON schema of `namespace`
    '''

    if default is None:
        default = dict()

    properties = default['properties'].copy()

    for key in ['value', 'confidence']:
        try:
            properties[key] = __NAMESPACE__[namespace][key]
        except KeyError:
            pass

    return dict(type='object', properties=properties)


def is_dense(namespace):
    '''Determine whether a namespace has dense formatting.

    Parameters
    ----------
    namespace : str
        Namespace key identifier

    Returns
    -------
    dense : bool
        True if `namespace` has a dense packing
        False otherwise.
    '''

    return __NAMESPACE__[namespace]['dense']


# Populate the schemata
SCHEMA_DIR = os.path.join('schema', 'namespaces')
