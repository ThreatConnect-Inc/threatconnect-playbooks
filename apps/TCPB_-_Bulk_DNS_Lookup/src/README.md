# Bulk DNS Lookup

# Release Notes

### 1.0.0 (2021-05-29)

* Initial Release


# Category

- Utility

# Description

This app allows bulk lookup of DNS records, with a rate limit to prevent nameservers from blocking lookups (ie, for bad behavior).
# Actions

___
## Lookup DNS
### Inputs

### *Connect*

  **DNS Server(s)** *(String)*
  DNS servers to interrogate
  > **Allows:** String, StringArray

### *Configure*

  **Question(s)** *(String)*
  The questions to ask the DNS server, generally this is a hostname, but for a PTR record it is the origin address.
  > **Allows:** String, StringArray, TCEntity, TCEntityArray

  _**Record Types**_ *(MultiChoice, Optional, Default: A, AAAA, MX)*
  The type of resource records to retrieve.
  > **Valid Values:** A, AAAA, CNAME, MX, PTR, SOA, TXT

  **Transform question for PTR lookups** *(Boolean, Default: Selected)*
  When true, a question for a PTR lookup will be rewritten to the appropriate form, e.g. 1.2.3.4 will be transformed to 4.3.2.1.in-addr.arpa.

### *Advanced*

  **Rate Limit** *(String, Default: 150)*
  Limit requests to this number/sec.  Each separate record type is a separate request.

### Outputs

  - dns.result.json *(String)*
  - dns.valid *(StringArray)*
  - dns.invalid *(StringArray)*
  - dns.action *(String)*
