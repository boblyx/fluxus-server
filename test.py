"""
IDS test
:author: Bob YX Lee
"""
import ifctester
import ifctester.ids
import ifctester.reporter as Reporter
import ifctester.facet as Facet
import ifcopenshell
import os
from pprint import pprint

def executeIDS(ifc_path : str, ids_path : str):
    ifc = ifcopenshell.open(ifc_path)
    ids = ifctester.ids.open(ids_path)
    ids.validate(ifc)
    report = Reporter.Json(ids).report()
    pprint(report)
    return report

if __name__ == "__main__":
    ifc_path = os.path.join(os.getcwd(), "examples", "example.ifc");
    ids_path = os.path.join(os.getcwd(), "examples", "IFC_SG_IDS_walls.xml");
    
    ifc = ifcopenshell.open(ifc_path)
    ids = ifctester.ids.open(ids_path);
    #pprint(ifc)
    elements = None
    entity = ids.specifications[0].applicability[0]
    elements = entity.filter(ifc, elements)
    #pprint(elements)
    test_elem = elements[0]
    psets = Facet.get_psets(test_elem)
    pprint(psets);
    #entity.filter(ifc, elements);
    #pprint(elements);
    #executeIDS(ifc_path, ids_path);
    pass
