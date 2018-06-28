# Text Blob

## Summary

Playbook app wrapper for TextBlob (https://github.com/sloria/TextBlob).

## Dependencies

- tcex

## Input Definitions

- `string` *(String)*: String
- `n_gram` *(String)*: n-gram length

## Output Definitions

- `json` *(KeyValueArray)*
- `nounPhrases` *(StringArray)*
- `npCounts` *(KeyValueArray)*
- `polarity` *(String)*
- `subjectivity` *(String)*
- `sentences` *(StringArray)*
- `tokens` *(StringArray)*
- `tags` *(KeyValueArray)*
- `words` *(StringArray)*
- `wordCounts` *(KeyValueArray)*

## Use Cases

Todo: add use cases

## Installing in ThreatConnect

To install this app in ThreatConnect, run:

```shell
make lib
make pack
```

This will create a `.tcx` file in the top app directory which will work in ThreatConnect assuming the instance of ThreatConnect is running the same version of python used during the `make lib` command.

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and [Floyd Hightower's TCEX App Creation UI](http://tcex.hightower.space).
