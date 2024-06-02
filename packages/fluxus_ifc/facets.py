"""
fluxus_facets.py

Modified from `ifctester.facet`
"""

from ifctester.facet import Property, PropertyResult, Restriction
from pprint import pprint
from copy import deepcopy
import re

TYPE_MAP = { # xs datatype | py datatypes
            "double": ["int", "float"],
            "float": ["int", "float"],
            "decimal": ["int","float"],
            "boolean": ["bool"],
            "string": ["str"]
        }

NOPSET = PropertyResult(False, {"type": "NOPSET"})
NOVALUE = PropertyResult(False, {"type": "NOVALUE"})
BADTYPE = PropertyResult(False, {"type": "DATATYPE"})
PROHIBIT = PropertyResult(False, {"type": "PROHIBITED"})

def hasKey(pset_data : dict, prop : Property) -> PropertyResult:
    baseName = prop.baseName
    if pset_data == None: return NOPSET
    if pset_data["data"] == None: return NOPSET
    if pset_data["data"][prop.propertySet] == None: return NOPSET
    if baseName in pset_data["data"][prop.propertySet]:
        return PropertyResult(True)
    return NOPSET

def matchesType(restrict_type, data_value):
    return type(data_value).__name__ in TYPE_MAP[restrict_type]

def followsRestrictions(pset_data, prop: Property) -> PropertyResult:
    restrictions = prop.value
    restrict_type = restrictions.base
    restrict_options = restrictions.options
    data_value = pset_data["data"][prop.propertySet][prop.baseName];
    if data_value == None:
        return NOVALUE
    
    # Check value type
    matches_type = matchesType(restrict_type, data_value)
    if not matches_type: 
        bad_type = deepcopy(BADTYPE)
        bad_type["actual"] = type(data_value).__name__
        bad_type["datatype"] = restrict_type
        return bad_type
    
    # Check options
    # TODO

    return PropertyResult(True)

def validateProperty(to_validate : dict, prop : Property) -> PropertyResult:
    """
    Validates a single fragment of Pset supplied agianst a ifctester.facet.Property requirement spec.
    Assumption is that `to_validate` and `property` are already matched.
    """
    #pprint(to_validate)
    #pprint(prop.__dict__)
    pset_name = prop.propertySet

    has_key = hasKey(to_validate, prop)
    
    if not has_key.is_pass:
        return has_key

    follows_restrictions = followsRestrictions(to_validate, prop)
    if not follows_restrictions.is_pass:
        return follows_restrictions
    """
    print('===================\nVALIDATION CHECK \n===================')
    print(f'\t- {prop.baseName} exists:', has_key)
    print(f'\t- {prop.baseName} type MATCH:', follows_restrictions)
    """
    return PropertyResult(True)
