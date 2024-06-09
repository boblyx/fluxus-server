"""
api.py

:author: Bob YX Lee
"""
import os
import sys
import json
import time
import logging
from time import time
from uuid import uuid4
from typing import List
from pprint import pprint
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, Request, HTTPException, status, Response, APIRouter, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

sys.path.append(os.path.join(os.getcwd(), "packages"))

from API import Speckle
from API.Speckle import SpeckleInfo, updateObjectParams
from specklepy.api.client import SpeckleClient
from fluxus_ifc.validation import Validator

DEFAULT_OUT = os.path.join(os.getcwd(), "out")

app = FastAPI()
env = os.environ #dotenv_values(".env."+os.environ["NODE_ENV"])
router = APIRouter(prefix=env["BASE_PATH"])
host = env["API_HOST"]
port = int(env["API_PORT"])

origins = ["*"]
app.add_middleware(
        CORSMiddleware,
        allow_origins = origins,
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"]
        )

@router.get("/api/v1/health")
def root():
    """ Returns health
    """
    return "HEALTHY"

@router.post("/api/v1/update_obj")
def update_obj(speckle: str = "app.speckle.systems",
               stream: str = "ae5477e163", 
               obj: str = "03b551dfdfbc243a817ef17538835744", 
               access_code: str = "",
               branch_name : str = "main",
               update_data : dict = {
                    "SGPset_WallStructuralLoad": {
                        "WorkingLoad_DA1-1": 20
                        }
                   }):

    client = SpeckleClient(host = speckle)
    speckle_info = SpeckleInfo(stream, obj, access_code)
    client.authenticate_with_token(access_code)
    res = updateObjectParams(client, update_data, speckle_info, branch_name)
    return res

@router.post("/api/v1/validate_spec")
def validate_spec(speckle: str = "app.speckle.systems",
                  stream: str = "90247e86c2", 
                  obj: str = "b7d4aa78f723dea7e168b1a6bd2e09d3", 
                  access_code: str = "", 
                  ids: UploadFile = None):
    """
    1. Get ids filepath and open using `ifctester`
    2. run `Validator.validateIDS`
    """
    print(ids.headers["content-type"])
    ctype = ids.headers["content-type"]
    if ids == None or not ctype == "text/xml":
        return HTTPException(status_code=422, detail="IDS is not an XML file")
    ids_path = os.path.join(DEFAULT_OUT, str(time())+".xml")
    #NamedTemporaryFile(delete = False)
    try:
        contents = ids.file.read()
        with open(ids_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to upload IDS file")
    finally:
        ids.file.close()
    
    #print(ids_path.name)
    speckle_info = SpeckleInfo(stream, obj, access_code)
    speckle_client = SpeckleClient(host = speckle)
    # TODO: add client auth here
    result = Validator.validateIDS(speckle_client, ids_path, speckle_info)
    
    return result

app.include_router(router)

if __name__=="__main__":
    uvicorn.run("api:app",host=host, port = port, log_level="info", reload=True)
    logging.info("Running on http://%s:%s" % (host, str(port)))
