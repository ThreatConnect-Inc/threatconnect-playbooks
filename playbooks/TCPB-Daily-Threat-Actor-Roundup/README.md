# Daily Threat Actor Roundup — Release Overview

This package provides a ready-to-import ThreatConnect playbook and a polished HTML report template to generate a periodic "Threat Actor Roundup" report summary. It is intended as an out-of-the-box example customers can import, configure, and run to receive a formatted HTML summary containing up to the latest threat-actor-related intel reports from ThreatConnect.

`Even though this is focused on Threat Actor-related intel reports, this can easily be tweaked to focus on different datasets, which we'll take a look at further down.`


### Key benefits
- Saves time: ships a full playbook `.pbxz` ready for import plus a styled HTML template so you can quickly stand up a recurring intelligence roundup.
- Reusable template: `ReportTemplate.html` contains placeholders for dynamic data replacement. Feel free to replace this template with your own!
- Configurable: easily change the recipients and the TQL query (which will populate what objects feed into the roundup) - only mandatory change is the email recipient list

### Files included
- `ReportTemplate.html` — main template used to render the roundup HTML
- `[Reporting] Daily Threat Actor Roundup.pbxz` — playbook to import into ThreatConnect

The TQL query being used by the playbook currently will pull out all Report objects created in the past 24 hours that have an Intrusion Set associated to them:

`typeName = "Report" and dateAdded > "NOW() - 24 hours" and hasGroup(typeName = "Intrusion Set")`

### Dependencies
- Your TC instance must be able to access Github.com to pull down the template in this repository
  - If your instance cannot access Github.com, we recommend to upload the ReportTemplate.html file into the platform and tell the playbook to pull from that locally uploaded version. Please reach out to your Customer Success team if you need assistance converting this.

# Quick-Start Guide
- Download the `[Reporting] Daily Threat Actor Roundup.pbxz` file
- Within ThreatConnect, go to `Automations & Feeds` through the top navigation bar of the UI
- Click `Import Playbook` -> `Import Playbook`
- Select the downloaded file and step throug the import wizard to fully import the Playbook
- Once the Playbook designer UI appears, you will see 3 steps in the Playbook that looks like this <img width="1082" height="353" alt="image" src="https://github.com/user-attachments/assets/e482148e-c8c2-43ac-8710-9fc27502a87e" />

#### Now it's time to configure & active the playbook!
1. Click the 3 lines on the top of the orange step called `Threat Actor Roundup Processing` -> Click `View`<img width="281" height="141" alt="image" src="https://github.com/user-attachments/assets/06c9b67e-620a-4a6e-8e1d-34e0c68b6c78" />
3. This will open a new playbook. At the top right of the screen click on `Design Mode` and change it to `Active`<img width="329" height="168" alt="image" src="https://github.com/user-attachments/assets/06bbfe34-408f-4e6d-81ed-d718174836b5" />
4. Click back to the first tab in this Playbook Designer page to return to the playbook you first imported<img width="412" height="224" alt="image" src="https://github.com/user-attachments/assets/2ba03ad5-7f47-4c0c-b167-669cd4a83885" />
5. Double Click on the orange `Threat Actor Roundup Processing` box to open the edit options
6. Change the `To Email` field to include a comma separated list of Email Addresses you want your email notifications to be sent<img width="354" height="187" alt="image" src="https://github.com/user-attachments/assets/02d6c0b0-f7a7-4546-8590-41b9ea269894" />
7. Check/Uncheck the `AI Summary` checkbox as desired - this will use ThreatConnect's CAL Doc Analysis Summarization to generate summaries if enabled.
8. `Optional` - You can also edit other fields on this window if you want to go the extra mile!
9. Click `Save`
10. Change this Playbook from `Design Mode` -> `Active` at the top right of the screen
11. Done!

____________

# For advanced users

### Playbook structure overview
<img width="3159" height="712" alt="image" src="https://github.com/user-attachments/assets/e3864bcf-92f7-49ac-83dd-22cb5e4ece1b" />

### Example Alternative Use Case
As mentioned earlier - this can be adapted easily to work for other data sets - not just Reports related to Intrusion Sets.

for example, here is a simple TQL that will change the whole process to send you a roundup of recently added CVEs with a high CVSS score.
Just replace the existing TQL with this one to test it out:

`typeName = "Vulnerability" and hasCommonGroup(cvss_score_v3>8.0 OR cvss_score_v3_1>8.0 OR cvss_score_v4>8.0) and dateAdded > "NOW() - 24 hours"`

### Placeholders used in the Report HTML template
The provided ReportTemplate.html file has several placeholders in it which the Playbook will populate with the relevant data from the Playbook running. 
You don't need to change anything here, but it's down to you if you'd like to create your own custom version instead. 
Just make sure you use these same fields so that the playbook doesn't break. 
OR 
If you change what placeholder fields you want to use, you must update the playbook to reflect those.

- Clean HTML report: `ReportTemplate.html`
  - `{IMAGE}` — banner/logo URL
  - `{REPORTURL}` — link to the full web version of the report
  - `{HEADER}` — report title/header
  - `{DATE}` — report/issue date
  - `{DISCLAIMER}` — legal or handling text block
  - `{AI Summary}` — optional generated summary block
  - `{CARDS}` — HTML fragment containing report "cards" (the playbook injects one card per report up to 10)
- Client-side niceties: copy-to-clipboard button (hidden when copy text is "'N/A'"), visually distinct `.threat-actor` badge, and responsive grid layout.

----
For questions or to request small template changes (colors, logo placement, or an example TQL), reply with the changes you want and I will update the files and show the exact steps to re-package and import.

