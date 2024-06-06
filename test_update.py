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

def parseProperty(string):
    prop_arr = string.split("\t")
    if(len(prop_arr) != 4):
        return None
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
    in_prop = False
    prop_sets = {}
    for match in seq.finditer(text):
        invalid = True
        text = match.groups()[0]
        cleaned = text.replace("\n", "")
        cleaned = cleaned.replace(" ", "")
        cleaned = cleaned.split("#")[0]
        if("PropertySet" in cleaned and not in_prop):
            prop_arr = parseProperty(cleaned)
            if prop_arr == None: continue 
            in_prop = True
            pass
        if(cleaned[0] == "\t" and in_prop == True):
            
            pass
        pprint(cleaned)
    pass

if __name__ == "__main__":
    parseRevitMapping(SAMPLE_MAPPING)
    pass
