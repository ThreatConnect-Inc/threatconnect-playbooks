# Strip_String

## Summary

Strip a string.

## Dependencies

- tcex

## Input Definitions

- `string` *(String)*: String you would like to strip

## Output Definitions

- `strippedString` *(String)*

## Installing in ThreatConnect

To install this app in ThreatConnect, run:

```shell
make lib
make pack
```

This will create a `.tcx` file in the top app directory which will work in ThreatConnect assuming the instance of ThreatConnect is running the same version of python used during the `make lib` command.

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and [Floyd Hightower's TCEX App Creation UI](http://tcex.hightower.space).
