from pydantic import BaseModel
from fastapi import UploadFile


class SpeckleInfo(BaseModel):
    stream : str
    obj : str
    access_code : str
    model_config = \
            {
                    "json_schema_extra": \
                            {
                                "examples": \
                                        [
                                            {
                                                "stream": "90247e86c2"
                                                ,"obj": "b7d4aa78f723dea7e168b1a6bd2e09d3"
                                                ,"access_code": "b7d4aa78f723dea7e168b1a6bd2e09d3"
                                                }
                                            ]
                                        }
                            }
    pass
