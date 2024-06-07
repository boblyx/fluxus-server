"""
test_update.py
Test add a single Revit parameter.
- Given:
    - a Revit native speckle object with 
        - 1 correct parameter and 
        - 1 missing parameter,
    - a Revit to IFC mapping file

- Identify required changes based on IDS
"""

import re
import os
from pprint import pprint
SAMPLE_MAPPING = os.path.join(os.getcwd(), "examples", "RevitMapping.txt")

def parsePropertySet(string):
    prop_arr = string.split("\t")
    if(len(prop_arr) != 4):
        return None
    return prop_arr

def parseProperty(string):
    prop_arr = string.split("\t")
    return prop_arr

def parseRevitMapping(path):
    """
    Parse mapping based on a Revit IFC mapping file
    """
    text = ""
    with open(path, "r") as f:
        text = f.read()
        pass
    seq = re.compile('(^[^#].*)', re.MULTILINE)
    prop_sets = {}
    current_pset = ""
    for match in seq.finditer(text):
        invalid = True
        text = match.groups()[0]
        cleaned = text.replace("\n", "")
        cleaned = cleaned.replace(" ", "")
        cleaned = cleaned.split("#")[0]
        propset_arr = None
        if("PropertySet" in cleaned):
            propset_arr = parsePropertySet(cleaned)
            if propset_arr == None: 
                current_pset = ""
                continue 
            current_pset = propset_arr[1]
            prop_sets[current_pset] = {}
            pass
        if current_pset == "": continue
        if(cleaned[0:1] == "\t"):
            prop_arr = parseProperty(cleaned)
            if prop_arr == None: continue
            prop_sets[current_pset].update(
                {"ifc": prop_arr[1], "other": prop_arr[3], "type": prop_arr[2]}
            )
            pass
    return prop_sets

if __name__ == "__main__":
    prop_sets = parseRevitMapping(SAMPLE_MAPPING)
    pprint(prop_sets);
    pass
