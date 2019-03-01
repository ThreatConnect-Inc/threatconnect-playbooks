# Pyparsing Grammar Search

Use the [pyparsing](https://github.com/pyparsing/pyparsing/) package to search for a grammar in some text.

To use this app, you need to provide a grammar and the string in which you would like to search for the grammar.

For example, you can use the grammar:

```
Combine(Word('#') + Word(hexnums, min=3, max=6))
```

and the text 

```
test #333 #4444 #55555 #666666 ing
```

to find all of the hexadecimal color codes.

You can read more about pyparsing grammars [here](http://infohost.nmt.edu/tcc/help/pubs/pyparsing/pyparsing.pdf).

## Release Notes

## 0.1.0

* Initial Release
