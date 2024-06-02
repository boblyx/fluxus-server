"""
Speckle.py

- For interactions with Speckle graphql API
"""
from gql import gql
from specklepy.api.client import SpeckleClient
from pydantic import BaseModel

DEFAULT_SPECKLE_INFO = {"stream": "90247e86c2" 
                        ,"object": "b7d4aa78f723dea7e168b1a6bd2e09d3"
                        ,"access_code": "b7d4aa78f723dea7e168b1a6bd2e09d3"}

class SpeckleInfo:
    def __init__(self, stream, object, access_code):
        self.stream = stream
        self.object = object
        self.access_code = access_code
        pass
    pass

class QueryParam:
    def __init__(self, 
                 field : str = "type", 
                 value : str = "IFCWALL", 
                 operator : str = "=") -> dict:
        self.field = field
        self.value = value
        self.operator = operator

    def toDict(self):
        return {"query": self.__dict__}

def cPsetQuery(pset_name : str, speckle_info : SpeckleInfo = DEFAULT_SPECKLE_INFO):
    """
    Generates gql query
    :return: GQL document
    :rtype: DocumentNode
    """
    query = """query FluxusQuery($query: [JSONObject!]){
        stream(id:"%s"){
            object(id:"%s"){
                children(query: $query select: ["type", "%s", "id"]){
                    objects {
                        data
                    }
                }
            }
        }
    }
    """ % (speckle_info.stream, speckle_info.object, pset_name)
    return gql(query)

def getObjPsets(client : SpeckleClient, 
                       ifc_type : str = "IFCWALL", 
                       pset : str = "SGPset_WallStructuralLoad", 
                       speckle_info : SpeckleInfo = DEFAULT_SPECKLE_INFO):
    
    """
    Get objects according to specified type and associated PropertySet
    """

    params =  QueryParam("type", ifc_type, "=").toDict()
    gquery = cPsetQuery(pset, speckle_info)

    response = client.httpclient.execute(gquery, params)
    return response["stream"]["object"]["children"]["objects"]

