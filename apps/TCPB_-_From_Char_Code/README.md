# Character Code to String Converter

Convert character codes (technically, Unicode code points) to the string they represent. For example:

- If you give this app `118, 97, 114, 32, 115, 111, 109, 101, 115, 116, 114, 105, 110, 103`, you will get `var somestring`

You can provide this app either a list of character codes (e.g. `[41, 42, 43, 44]` or `['41', '42', '43', '44']`) or just a string seperated by a comma (e.g. `45, 46, 47, 48` or `'45', '46', '47', '48'`).

Under the hood, this app uses Python's [chr](https://docs.python.org/3.7/library/functions.html#chr) function.

## Usage

It is not uncommon for Javascript malware to obfuscate itself using the [String.fromCharCode](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/fromCharCode) function (it is common to see something like `eval(String.fromCharCode(...))` (e.g. https://gist.github.com/jonmarkgo/3431818)). This playbook app lets you convert these character codes to the string they represent.

This playbook app replicates Javascript's [String.fromCharCode](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/fromCharCode) function.

## Release Notes

### 0.0.1

* Initial Release
