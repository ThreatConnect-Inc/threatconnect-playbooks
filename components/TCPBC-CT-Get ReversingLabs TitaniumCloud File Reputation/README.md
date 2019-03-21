# Get ReversingLabs TitaniumCloud File Reputation
## Summary
This Component is meant for taking file hash indicators in ThreatConnect and querying ReveringLabs' TitaniumCloud File Reputation service. The Component will query ReversingLabs' API, pull back the JSON response, and parse the various fields out, exposing them as output variables. Additionally, the raw JSON response is exposed as an output variable so users can work directly with the JSON if they so choose. 

## Dependencies
- Valid ReversingLabs TitaniumCloud API credentials

## Input parameters
The Component requires the following configuration parameters:
- **Input Hash Value**: The MD5, SHA1, or SHA256 of the File IOC that you want to query in ReversingLabs.

- **Input Hash Type**: You need to tell ReversingLabs the file hash algorithm of the File IOC.

- **TitaniumCloud Server**: The TitaniumCloud server that your organization uses in production.

- **ReversingLabs Username**: The username that RevesingLabs has supplied to you with API permissions.

- **ReversingLabs Password**: The password coupled with the above Username.

Additionally, there are two optional configuration parameters:
- **Extended Response**: Enable this if you want to return additional information from ReversingLabs such as Trust Factor, Threat Level, and more. Default for this parameter is set to False.

- **Show Hashes**: Enable if you want to return the other hash algorithms (if you supply an MD5, ReversingLabs will return the SHA1 and SHA256 if they are known). Default for this parameter is set to False.


## Output parameters
- #rl.malware_presence.status	String
- #rl.malware_presence.sha1	String
- #rl.malware_presence.threat_level	String
- #rl.malware_presence.classification.subplatform	String
- #rl.malware_presence.classification.platform	String
- #rl.malware_presence.classification.is_generic	String
- #rl.malware_presence.classification.family_name	String
- #rl.malware_presence.scanner_percent	String
- #rl.malware_presence.threat_name	String
- #rl.malware_presence.scanner_match	String
- #rl.malware_presence.last_seen	String
- #rl.malware_presence.scanner_count	String
- #rl.malware_presence.first_seen	String
- #rl.malware_presence.sha256	String
- #rl.malware_presence.trust_factor	String
- #rl.malware_presence.md5	String
- #rl.malware_presence.classification.type	String
- #rl.response.json	String


For more information on ReversingLabs' TitaniumCloud File Reputation service, please refer to [https://www.reversinglabs.com/products/file-reputation-service](https://www.reversinglabs.com/products/file-reputation-service)