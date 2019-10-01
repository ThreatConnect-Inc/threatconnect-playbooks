# Component - IOC All Data Pull
## Summary
The component is built to ingest a single IOC and run API calls to bring back all data on the IOC that can be pulled from API calls. The API data includes Tags, Attributes, Associations, and Security Labels. All returned data is merged into a JSON blob and returned as the output to the Component. If the IOC does not exist in the Sources the Run As user has permissions to, the return data will be a 0. 

## Dependencies
- No external dependencies required

## Input parameters
The Component requires the following configuration parameters:
- **Indicator**: The IOC that you want to query the API branches for.

## Output parameters
- #all.ioc.data	String