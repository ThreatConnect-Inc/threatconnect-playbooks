This app will query the ThreatConnect API for indicators that are parseable. For each that is parseable, the regex will then be retrieved from the API for the respective indicator type.
This app will then parse through the input for any that match and will return them.

If the deduplicate option is checked, the returned lists will be deduplicated.

If entries are placed in for the whitelist, they will be removed from the returned output.

Changelog:
## 0.1.0
* Initial Release

## 1.0.0
* Breaking changes introduced 
* Added the option to defang indicators.
* Removed Files as an output
* Added MD5/SHA1/SHA256 as individual outputs