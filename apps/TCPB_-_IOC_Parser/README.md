# IOC Parser

Parser Indicators of Compromise using the [ioc-finder](https://github.com/fhightower/ioc-finder) package.

All bug reports for the [ioc-finder](https://github.com/fhightower/ioc-finder) package or requests for more parsing capabilities can be handled [here](https://github.com/fhightower/ioc-finder#capabilities).

**Note:** The [ioc-finder](https://github.com/fhightower/ioc-finder) package is not supported by ThreatConnect and not all indicator types of indicators parsed by the package will be able to be created in ThreatConnect (and visa-versa).

## Usage

### Inputs

The app has the following inputs:

- `text` (required)
- `parse_host_from_email_address` (optional)
- `parse_address_from_cidr` (optional)
- `parse_host_from_url` (optional)

### Outputs

The app produces the following output:

- `iocParser.bitcoinAddresses`
- `iocParser.asns`
- `iocParser.cves`
- `iocParser.domains`
- `iocParser.emailAddresses`
- `iocParser.googleAnalyticsIds`
- `iocParser.ipv4Cidrs`
- `iocParser.ipv4s`
- `iocParser.ipv6s`
- `iocParser.md5s`
- `iocParser.registryKeyPaths`
- `iocParser.sha1s`
- `iocParser.sha256s`
- `iocParser.sha512s`
- `iocParser.simpleEmailAddresses`
- `iocParser.urls`
- `iocParser.googleAdsensePublisherIds`

## Release Notes

### 0.1.0

* Initial Release
