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
from specklepy.api.client import SpeckleClient
from gql import gql

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

SC = SpeckleClient(host = "app.speckle.systems");
def executeIDS(ifc_path : str, ids_path : str):
    ifc = ifcopenshell.open(ifc_path)
    ids = ifctester.ids.open(ids_path)
    ids.validate(ifc)
    report = Reporter.Json(ids).report()
    pprint(report)
    return report

def speckleGetObjPsets():
    params = {
            "query":{
                "field": "type"
                ,"value": "IFCWALL"
                ,"operator": "="
                }
    }

    response = SC.httpclient.execute(TEST_QUERY, params)
    pprint(response)
    return response["stream"]["object"]["children"]["objects"]

if __name__ == "__main__":
    """
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
    #executeIDS(ifc_path, ids_path);
    """
    objects = speckleGetObjPset();
    # Given above Psets, validate them
    pass
