# Yara Validator

## Summary

Validate a yara rule.

## Dependencies

- tcex
- yara-python
- [yara-validator](https://github.com/CIRCL/yara-validator)

## Input Definitions

- `yara_rule` *(String)*: Yara rule

## Output Definitions

- `errorData` *(String)*
- `repairedSource` *(String)*
- `source` *(String)*
- `validationStatus` *(String)*

## Installing in ThreatConnect

To install this app in ThreatConnect, run:

```shell
make lib
make pack
```

This will create a `.tcx` file in the top app directory which will work in ThreatConnect assuming the instance of ThreatConnect is running the same version of python used during the `make lib` command.

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and [Floyd Hightower's TCEX App Creation UI](http://tcex.hightower.space).
