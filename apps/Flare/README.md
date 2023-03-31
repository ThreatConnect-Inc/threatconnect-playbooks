# Playbook Utility

# Release Notes

### 1.0.0 (2022-08-20)

* Initial Release


# Description

Take an JSON email attachment and makes it a regular JSON object available for further use in a ThreatConnect Playbook

### Inputs

  **Mailbox Attachment JSON** *(trg.mbox.attachment)*
  The data to be formatted.
  > **Allows:** JSON

  _**Indent**_ *(String, Optional, Default: 4)*
  The number of spaces to use for indention (default: 4).

  **Sort Keys** *(Boolean, Default: Unselected)*
  No

### Outputs

  - firework_alert.json *KeyValueArray*

# Dependencies

You need to have a license for [Flare](https://signup.flare.systems/trial) and have [setup your alerts]() to be sent with a JSON attachments to your inbox.