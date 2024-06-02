"""
test.py
Testing on how to manually check using IDS
:author: Bob YX Lee
"""
import sys
import os
from pprint import pprint

sys.path.insert(0, os.path.join(os.getcwd(), "packages"))

from fluxus_ifc.facets import validateProperty
from fluxus_ifc.validation import Validator
import ifctester
import ifctester.ids
import ifctester.reporter as Reporter
import ifctester.facet as Facet
import ifcopenshell
from specklepy.api.client import SpeckleClient
from gql import gql
from time import time

TEST_QUERY = gql("""query Walls($query: [JSONObject!]){
    stream(id: "90247e86c2"){
        object(id: "b7d4aa78f723dea7e168b1a6bd2e09d3"){
            children(query: $query select: ["type", "SGPset_WallStructuralLoad"]){
                objects{
                    data
                }
            }
        }
    }
}
""")

class SpeckleInfo:
    def __init__(self, stream, object, access_code=""):
        self.stream = stream
        self.object = object
        self.access_code = access_code
        pass
    pass

def executeIDS(ifc_path : str, ids_path : str):
    ifc = ifcopenshell.open(ifc_path)
    ids = ifctester.ids.open(ids_path)
    ids.validate(ifc)
    report = Reporter.Json(ids).report()
    pprint(report)
    return report

if __name__ == "__main__":

    speckle_client = SpeckleClient(host = "app.speckle.systems");
    speckle_info = SpeckleInfo("90247e86c2", "b7d4aa78f723dea7e168b1a6bd2e09d3")

    ids_path = os.path.join(os.getcwd(), "examples", "IFC_SG_IDS_walls.xml");
    ids = ifctester.ids.open(ids_path);
    results = {}
    for spec in ids.specifications:
        for entity in spec.applicability:
            reqs = spec.requirements
            vdict = Validator.validateEntity(speckle_client, 
                                             entity, 
                                             reqs, 
                                             speckle_info)
            results.update(vdict)
            pass
        pass
    pass
    pprint(results)

    """
    # Studies
    ifc_path = os.path.join(os.getcwd(), "examples", "example.ifc");
    ifc = ifcopenshell.open(ifc_path)
    entity = ids.specifications[0].applicability[0]
    requirements = ids.specifications[0].requirements
    
    pset = requirements[0].propertySet
    restrict = requirements[0].value
    #pprint(restrict.__dict__)
    ifc_type = entity.name
    # First, get the speckle objects based on IDS
    objects = speckleGetObjPsets(SC,ifc_type, pset, speckle_info)
    #pprint(objects)
    test_object = {
            "data": {
                "SGPset_WallStructuralLoad": {
                    "WorkingLoad_DA1-1":20
                    }
                ,"id": "my_id"
                }
            }
    results = {"objects": {}}
    for o in objects:
        results["objects"].update(validateObject(o, requirements))
        pass
    pprint(results);
    """
    exit()
