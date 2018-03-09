# Indicator Fanger

## Summary

Fang indicators of compromise in text. Fanging the process of `example[.]com hXXp://bad[.]com/phishing.php` => `example.com http://bad.com/phishing.php` (see https://ioc-fang.github.io/ for more information on fanging and defanging indicators).

## Dependencies

- tcex
- [ioc_fanger](https://github.com/ioc-fang/ioc_fanger)

## Input Definitions

- `Text`: The text which you would like to fang

## Output Definitions

- `fangedText`: The text with indicators fanged

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and [Floyd Hightower's TCEX App Template](https://github.com/fhightower-templates/tcex-app-template).
