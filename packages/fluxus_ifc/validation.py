"""
validation.py

:author: Bob YX Lee
"""
import sys
import os
packages_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, packages_folder)

from API import Speckle
from API.Speckle import SpeckleInfo
from .facets import validateProperty

from specklepy.api.client import SpeckleClient
import ifctester

class Validator:
    """
    Class for validating speckle objects vis-a-vis IDS requirements
    """

    @staticmethod
    def validateObject(object : dict, 
                       requirements : dict) -> dict:

        object_id = object["data"]["id"]
        out = {object_id:{ "requirements": {}}}
        for r in requirements:
            valid = validateProperty(object, r)
            out[object_id]["requirements"][r.baseName] = valid.__dict__
            pass
        return out

    @staticmethod
    def validateRequirement(client : SpeckleClient, 
                            entity, 
                            requirement, 
                            speckle_info : SpeckleInfo) -> dict:

        results = {}
        pset = requirement.propertySet
        objects = Speckle.getObjPsets(client, entity.name, pset, speckle_info)
        for o in objects:
            o_id = o["data"]["id"]
            result = validateProperty(o, requirement)
            if not o_id in results:
                results[o_id] = {requirement.baseName: result.__dict__}
            else:
                results[o_id][requirement.baseName] = result.__dict__
            pass
        return results

    @staticmethod
    def validateEntity(client, 
                       entity, 
                       requirements, 
                       speckle_info : SpeckleInfo):
        """
        Validates 1x entity
        Could be applied for Material, Quantities etc
        """
        results = {}
        for r in requirements:
            result = Validator.validateRequirement(client, entity, r, speckle_info)
            for k, v in result.items():
                if not k in results:
                    results[k] = v
                else:
                    for k2, v2 in v.items():
                        results[k][k2] = v2
                        pass
                    pass
                pass
            pass
        return results

    @staticmethod
    def validateIDS(client : SpeckleClient, 
                    ids_path : str, 
                    speckle_info : SpeckleInfo):
        """
        Validates based on given IDS file path.
        """
        results = {}
        ids = ifctester.ids.open(ids_path)
        for spec in ids.specifications:
            for entity in spec.applicability:
                reqs = spec.requirements
                vdict = Validator.validateEntity(client,
                                                 entity,
                                                 reqs,
                                                 speckle_info);
                results.update(vdict)
                pass
            pass
        return results
