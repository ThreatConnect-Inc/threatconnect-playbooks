This Component is meant for deleteing a YARA rule that has been previously uploaded to ReversingLabs' A1000 Malware Analysis Platform's YARA Hunting capability. Note that if you enter the name of a YARA rule that is not present in A1000, the Component will still completely successfully, but will output the message "Failed to delete ruleset. Please see logs for more information.".

For more information on this capability please visit https://www.reversinglabs.com/products/malware-analysis-appliance

The Component requires the following configuration parameters:
- **Input Ruleset Name**: The name of the YARA rule you want to send to ReversingLabs.

- **TitaniumCloud Server**: The TitaniumCloud server that your organization uses in production.

- **ReversingLabs Username**: The username that RevesingLabs has supplied to you with API permissions.

- **ReversingLabs Password**: The password coupled with the above Username.