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

To install this app in ThreatConnect, run the following from the app's top directory:

```shell
make lib
```

Then, navigate into the `lib...` directory which was created inside the app's subdirectory and run the following to install the [yara-validator](https://github.com/CIRCL/yara-validator):

```shell
git clone https://github.com/CIRCL/yara-validator.git
mv yara-validator/yara-validator/* ./yara-validator
rm -rf yara-validator/yara-validator/
```

Finally, run:

```shell
make pack
```

This will create a `.tcx` file in the top app directory which will work in ThreatConnect assuming the instance of ThreatConnect is running the same version of python used during the `make lib` command.

**NOTE:** Because this app uses yara (specifically [yara-python](https://github.com/VirusTotal/yara-python)), it will probably need to be packaged on an OS that is compatible with the instance of ThreatConnect on which it is being installed.

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and [Floyd Hightower's TCEX App Creation UI](http://tcex.hightower.space).
