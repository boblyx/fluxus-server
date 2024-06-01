# Fluxus Server
- Instead of using `ifctester` to conduct IDS, having to parse the entire model
- We could first filter the relevant items from the Speckle Model and check them individually
    - e.g., Based on IDS, grab all walls
    - Then loop through walls to check
- This filtered method of dealing with the model will allow checking to be parallelised and potentially faster
- User will be required to share a Revit Property Mapping to allow fixes to be pushed to the Speckle Stream

## Workflows
### IDS check for 1x specification
- Payload contents:
    - IDS specification (.xml/.ids)
    - Speckle Base Objects (as JSON)
    - Mapping file (optional, base on Revit for now)
- Notes
    - Beforehand, the `frontend` should 

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
