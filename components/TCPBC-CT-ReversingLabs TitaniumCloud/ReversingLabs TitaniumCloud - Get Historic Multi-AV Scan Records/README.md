# Get ReversingLabs TitaniumCloud Historic Multi-AV Scan Records
## Summary
This Component is meant for taking file hash indicators in ThreatConnect and querying ReveringLabs' TitaniumCloud Historic Multi-AV Scan Records. The Component will query ReversingLabs' API, pull back the JSON response, and parse the various fields out, exposing them as output variables. Additionally, the raw JSON response is exposed as an output variable so users can work directly with the JSON if they so choose. 

## Dependencies
- Valid ReversingLabs TitaniumCloud API credentials

## Input parameters
The Component requires the following configuration parameters:
- **Input Hash Value**: The MD5, SHA1, or SHA256 of the File IOC that you want to query in ReversingLabs.

- **Input Hash Type**: You need to tell ReversingLabs the file hash algorithm of the File IOC.

- **TitaniumCloud Server**: The TitaniumCloud server that your organization uses in production.

- **ReversingLabs Username**: The username that RevesingLabs has supplied to you with API permissions.

- **ReversingLabs Password**: The password coupled with the above Username.



## Output parameters
- #rl.sample.sha1	String
- #rl.sample.first_seen_on	String
- #rl.sample.last_scanned_on	String
- #rl.sample.last_seen_on	String
- #rl.sample.single_scan	String
- #rl.sample.first_scanned_on	String
- #rl.sample.sample_type	String
- #rl.sample.sample_size	String
- #rl.sample.xref.scanner_match	String
- #rl.sample.xref.scanner_count	String
- #rl.sample.xref.scanners	StringArray
- #rl.sample.xref.scanned_on	String
- #rl.sample.xref.results	StringArray
- #rl.sample.sha384	String
- #rl.sample.sha256	String
- #rl.sample.sha512	String
- #rl.sample.ripemd160	String
- #rl.sample.md5	String
- #rl.response.json	String


For more information on ReversingLabs' TitaniumCloud Historic Multi-AV Scan Records service, please refer to [https://www.reversinglabs.com/products/file-reputation-service](https://www.reversinglabs.com/products/file-reputation-service)