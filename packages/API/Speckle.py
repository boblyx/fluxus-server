"""
Speckle.py

- For interactions with Speckle graphql API
"""
from gql import gql
from specklepy.api.client import SpeckleClient
from pydantic import BaseModel
from uuid import uuid4

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

def getObjectData(client, stream, speckle_id):
    query = """
    query ObjQ{
        stream(id:"%s"){
            object(id:"%s"){
                data
            }
        }
    }
    """ % (stream, speckle_id)
    return client.httpclient.execute(gql(query))["stream"]["object"]["data"]

def createObject(client, speckle_info, data):
    mut = """
    mutation ObjectCreate($objectInput: ObjectCreateInput!){
        objectCreate(objectInput: $objectInput)
    }
    """
    params = {
        "objectInput": {
                "streamId": speckle_info.stream,
                "objects": [data]
            }
    }
    obj = client.httpclient.execute(gql(mut), params)["objectCreate"]
    return obj

def createCommit(client, branch_name, speckle_info, obj_id):
    mut = """
    mutation CommitCreate($commit: CommitCreateInput!){
        commitCreate(commit: $commit)
    }
    """
    params = {
        "commit": {
                "streamId": speckle_info.stream,
                "objectId": obj_id,
                "branchName": branch_name,
                "message": "Made by FamilyMan"
            }
        }
    commit = client.httpclient.execute(gql(mut), params)["commitCreate"]
    return commit

def updateObjectParams(client : SpeckleClient 
        ,update_data : dict
        ,speckle_info : SpeckleInfo
        ,branch_name : str):
    # Get the original model
    obj = getObjectData(client, speckle_info.stream, speckle_info.object)

    # Apply the changes
    for k, v in update_data.items():
        obj[k] = v
        pass
    
    obj["id"] = "fluxus-%s" % uuid4()
    # Create a new object
    obj_id = createObject(client, speckle_info, obj)[0];
    commit_id = createCommit(client, branch_name, speckle_info, obj_id);
    return "%s/projects/%s/models/%s" % (client.url, speckle_info.stream, obj_id)

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

