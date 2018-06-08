# Example App

## Summary

Example playbook app created using the TcEx package. The app takes a string input and reverses it.

## Dependencies

- tcex

## Input Definitions

- `string`: String you would like to reverse

## Output Definitions

- `reversedString`: The reversed string

## Installing in ThreatConnect

To install this app in ThreatConnect, run:

```shell
make lib
make pack
```

This will create a `.tcx` file in the top app directory which will work in ThreatConnect assuming the instance of ThreatConnect is running the same version of python used during the `make lib` command.

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and [Floyd Hightower's TCEX App Template](https://github.com/fhightower-templates/tcex-app-template).
