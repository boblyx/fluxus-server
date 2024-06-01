# Fluxus Server
- Frontend can be found at https://github.com/yuj8fuj6/fluxus
- Instead of using `ifctester` to conduct IDS, having to parse the entire model
- We could first filter the relevant items from the Speckle Model and check them individually
    - e.g., Based on IDS, grab all walls
    - Then loop through walls to check only the `PropertySet` relevant to IDS
- This filtered method of dealing with the model will allow checking to be parallelised and potentially faster
- User will be required to share a Revit Property Mapping to allow fixes to be pushed to the Speckle Stream

## Workflows
### <IDS-1> IDS check for 1x specification
- Payload:
    - `ids`: IDS specification (.xml/.ids)
    - `speckle`: Speckle Info
        - `stream`: Speckle Stream
        - `commit`: Speckle Commit
        - `token`: Speckle Auth Token
    - `mapping`: Revit <-> IFC Property Mapping file
- Response:
    - `report`: Validation report
        - `failed_items`: List of failed elements
            - `id`: Speckle ID of the failed element (used to highlight in frontend).
            - `specification`: Which part of the specification failed.
            - `msg`: Any additional messages
- Notes
    - Frontend should not do the filtering, and should be a server side op due to giant file size for large projects, which makes it too dependent on user compute (which is not scalable)
    - Server will handle the getting of Speckle Objects and checking

### [IDS-2] IDS batch check
- Payload:
    - `ids`: List[] of IDS specifications
    - `speckle`: Speckle Info
    - `mapping`: Revit <-> IFC Property Mapping file

- Response
    - Similar to `<IDS-1>` except in a map keyed by ids file names.

### [IDS-3] IDS Resolver
- Payload:
    - `failed_items`: List of failed elements
    - `mapping`: BIM <-> IFC Property Mapping file
- Response:
    - `patch`: List of transformations recommended by vector DB
- Notes:
    - We embed IDS requirements into a vector embedding using ChromaDB
    - Based on failed item's list of properties, we suggest either modifying:
        - Property Keys
        - Property Values

### [OBJ-1] Object Updater
- Payload:
    - `objects`:
        - `id`: Speckle ID of the object
        - `update`: List of objects to update 
            ```json
            {
                "id": "abcd"
                "properties":
                {
                    "add": {
                        "key": "value"
                    }
                    ,"update": {
                        "key": "value"
                    }
                }
            }
            ```
- Notes:
    - Based on accepted changes / field updates
    - Try to create a new commit with only the updated items i.e. update parameter only

## Notes
### Filtering Speckle Objects by type according to mapping file / IFCTYPE
- In example below, we extract only IFCWALL type objects from the Speckle model.
- This query could be sent from server side to retrieve relevant Speckle objects with the relevant IFC `PropertySet`
- In the case the model is from Revit, or other BIM Software, we can just select properties according to the Mapping provided by the user.
#### GraphQL query
```graphql
query Walls($query: [JSONObject!]){
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
```
#### GraphQL variables
```json
{
  "query": {
    "field": "type",
    "value": "IFCWALL",
    "operator": "="
  }   
}
```


## Usage
1. To develop, edit `dev.sh` for environment variables:
1. To start the dev server:
```bash
bash dev.sh
```
1. To start the production server:
```bash
bash start.sh
```

## Stack
- List stack components here

## Contributors
- Bob YX Lee
