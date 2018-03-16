Summary
This Playbook template lets users send an address or host to Infoblox. After submission to the Infoblox appliance an attribute will be added to the indicator inside of ThreatConenct. This playbook can be modified to send an email notifcation after successful deployment depending on your internal policies.

App Dependencies
Access to an Infoblox server
rp_zone named threatconect or modify the playbook to reflect the rp_zone you want to use
Use Cases
Manually submit an addres or host indicator stored in the ThreatConnect to have action taken by Infoblox to bloxk access to that address or host.
Swap the User Action trigger with others to create an automated analysis workflow.
