# Disposable Email Address Identifier

Determine if the hostname of an email address is a disposable email address or not (using the list available here: [https://raw.githubusercontent.com/martenson/disposable-email-domains/master/disposable_email_blocklist.conf](https://raw.githubusercontent.com/martenson/disposable-email-domains/master/disposable_email_blocklist.conf)).

## Inputs

This playbook app takes either an email address or host as input.

## Outputs

This playbook returns a `0` (zero) if the email address's hostname (or the hostname if just given a hostname) is NOT a disposable email address service and `1` if the hostname is a disposable email address service.

## Examples

- `example@mailinator.com` => `1`
- `example@example.com` => `0`
