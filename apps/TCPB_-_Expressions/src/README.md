# Expressions

# Release Notes

### 1.0.6 (2021-04-09)

* Allow additional input types
* Add transform output types
* Add prune, structure, update, functions
* Add _ + iter_outputs to be the prior iteration result
* Allow tuple list outputs to nest

### 1.0.5 (2020-10-01)

* Converted to app.yaml
* added unnest function

### 1.0.4 (2020-09-25)

* Improve error handling by showing args to failing function
* Renamed spammatch to fuzzymatch
* Renamed spamdist to fuzzydist
* Renamed spamsum to fuzzyhash

### 1.0.3 (2020-09-24)

* Add spammatch function
* Add Return None on failure option
* Add ensure_ascii=False to json.dump to allow UTF-8 in values
* Add unique function

### 1.0.2 (2020-09-23)

* Add urlre, refindall, urlparse, urlparse_qs

### 1.0.1 (2020-09-23)

* Add csvread, csvwrite, md5, sha1, sha256, spamsum, spamdist

### 1.0.0 (2020-06-15)

* Initial Release


# Description

This application parses expressions and returns expression results.  The expression
grammar is similar to Python, but not exactly identical.  See ebnf-syntax below for the
complete extended Bachus Naur format of the grammar.  Some notable differences from
Python syntax are no methods on objects or variables, no list comprehensions.

Constants are case-insensitive, although any variables defined from loops are
case sensitive, as are attributes or dictionary keys.

ThreatConnect variables (e.g. `#App:1234:variable!String`) are evaluated on resolution
to determine if they are valid expressions, and the expression result is used
if they are.  If a variable is a string, it will be coerced to a float or an integer
on demand by most functions that expect float or integer arguments.  Note that JSON
data is expression grammar compatible, so an expression like
`#App:1234:json_object!String.field` is valid so long as `json_object` is a JSON
dictionary.


The following actions are included:
- **Evaluate** - A direct evaluation of an expression with either single or multiple results.

- **Evaluate Many** - Perform multiple evaluations, one set to define variables, another to define outputs.

- **Evaluate in Loop** - Loop evaluation of the same expression while looping over the inputs. Inputs with the same length are incremented in parallel.  The order of loop increments is shortest to longest.  A Loop expression which results in a list i.e [1, 2, 3] is used to extend the output rather than create nested output.  Tuple outputs will create nested output.

- **Evaluate Many With Loop** - Perform multiple evaluations, one set to define variables, another to define outputs. Loop variables with the same number of elements will be incremented concurrently, otherwise variables are incremented from shortest number of elements to largest.
Example: If `a` is `(1,2,3)` and `b` is `(1,2,3)` and `c` is `(1,2)`, a loop expression `(a,b,c)` will yield `[(1,1,1), (1,1,2), (2,2,1), (2,2,2), (3,3,1), (3,3,2)]`.
Loop expressions which result in lists i.e. [1, 2, 3] are used to extend the output, rather than create
nested outputs.  Tuple outputs will create nested outputs.



# Actions

___
## Evaluate
A direct evaluation of an expression with either single or multiple results.

### Inputs

### *Configure*

  **Expression** *(String)*
  The expression to evaluate.  If the expression is a list,
  e.g. ("foo", 1, 5.0) the output will be a StringArray.
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

### *Advanced*

  **Return None on failure** *(Boolean, Default: Selected)*
  When an expression fails to evaluate, assign it the value None, and continue
  execution.

### Outputs

  - expression.expression *(String)*
  - expression.result.0 *(String)*
  - expression.result.array *(StringArray)*
  - expression.action *(String)*
  - expression.errors *(StringArray)*

___
## Evaluate Many
Perform multiple evaluations, one set to define variables, another to define outputs.

### Inputs

### *Configure*

  _**Variables**_ *(KeyValueList, Optional)*
  Variables to be defined for the expressions to reference.  Defined variables are
  not output.  Variables are evaluated in the order they are entered.
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

  **Outputs** *(KeyValueList)*
  Outputs and output expressions for each output.  These may reference defined variables
  but may not refer to outputs not yet evaluated.  Outputs will be generated as a
  single output only, with list outputs being converted to JSON strings.
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

### *Advanced*

  _**Binary Outputs**_ *(KeyValueList, Optional)*
  Outputs to be delivered as Binary
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

  _**Binary Array Outputs**_ *(KeyValueList, Optional)*
  Outputs to be delivered as BinaryArray
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

  _**KeyValue Outputs**_ *(KeyValueList, Optional)*
  Outputs to be delivered as KeyValue
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

  _**KeyValue Array Outputs**_ *(KeyValueList, Optional)*
  Outputs to be delivered as KeyValueArray
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

  _**TCEntity Outputs**_ *(KeyValueList, Optional)*
  Outputs to be delivered as TCEntity.
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

  _**TCEntity Array Outputs**_ *(KeyValueList, Optional)*
  Outputs to be delivered as TCEntityArray.
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

  _**TCEnhancedEntity Outputs**_ *(KeyValueList, Optional)*
  Outputs to be delivered as TCEnhancedEntity.
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

  **Return None on failure** *(Boolean, Default: Selected)*
  When an expression fails to evaluate, assign it the value None, and continue
  execution.

### Outputs

  - expression.action *(String)*
  - expression.errors *(StringArray)*

___
## Evaluate in Loop
Loop evaluation of the same expression while looping over the inputs. Inputs with the same length are incremented in parallel.  The order of loop increments is shortest to longest.  A Loop expression which results in a list i.e [1, 2, 3] is used to extend the output rather than create nested output.  Tuple outputs will create nested output.

### Inputs

### *Configure*

  **Loop Variables** *(KeyValueList)*
  Add a name and a value for each variable to loop over.   Loop variables with
  the same number of elements will be incremented concurrently, variables with
  different number of elements will be nested from longest to shortest.
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

  **Expression** *(String)*
  The expression to evaluate.  If the expression generates a list result,
  each element of the step-wise evaluation will be appended to the final result.
  The prior iteration may be referred to using the name `_output` and will be
  None on the first iteration.
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

### *Advanced*

  **Return None on failure** *(Boolean, Default: Selected)*
  When an expression fails to evaluate, assign it the value None, and continue
  execution.

### Outputs

  - expression.expression *(String)*
  - expression.result.0 *(String)*
  - expression.result.array *(StringArray)*
  - expression.action *(String)*
  - expression.errors *(StringArray)*

___
## Evaluate Many With Loop
Perform multiple evaluations, one set to define variables, another to define outputs. Loop variables with the same number of elements will be incremented concurrently, otherwise variables are incremented from shortest number of elements to largest.
Example: If `a` is `(1,2,3)` and `b` is `(1,2,3)` and `c` is `(1,2)`, a loop expression `(a,b,c)` will yield `[(1,1,1), (1,1,2), (2,2,1), (2,2,2), (3,3,1), (3,3,2)]`.
Loop expressions which result in lists i.e. [1, 2, 3] are used to extend the output, rather than create
nested outputs.  Tuple outputs will create nested outputs.

### Inputs

### *Configure*

  _**Variables**_ *(KeyValueList, Optional)*
  Variables to be defined for the expressions to reference.  Defined variables are
  not output.  Variables are evaluated in the order they are entered.
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

  **Loop Variables** *(KeyValueList)*
  Add a name and a value for each variable to loop over.   Loop variables with
  the same number of elements will be incremented concurrently, variables with
  different number of elements will be nested from longest to shortest.
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

  **Loop Expressions** *(KeyValueList)*
  Loop outputs and loop output expressions for each output.  These may reference defined variables
  but may not refer to other loop variables or outputs, with the exception that
  the prior loop iteration variables are available with a leading underscore,
  and are None on the first iteration.
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

  _**Additional Outputs**_ *(KeyValueList, Optional)*
  Outputs and output expressions for each output.  These may reference defined
  variables and loop outputs, but may not refer to outputs not yet evaluated.
  Outputs will be generated as a single output only, with list outputs being converted to
  JSON strings.
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

### *Advanced*

  _**Binary Outputs**_ *(KeyValueList, Optional)*
  Outputs to be delivered as Binary
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

  _**Binary Array Outputs**_ *(KeyValueList, Optional)*
  Outputs to be delivered as BinaryArray
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

  _**KeyValue Outputs**_ *(KeyValueList, Optional)*
  Outputs to be delivered as KeyValue
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

  _**KeyValue Array Outputs**_ *(KeyValueList, Optional)*
  Outputs to be delivered as KeyValueArray
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

  _**TCEntity Outputs**_ *(KeyValueList, Optional)*
  Outputs to be delivered as TCEntity.
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

  _**TCEntity Array Outputs**_ *(KeyValueList, Optional)*
  Outputs to be delivered as TCEntityArray.
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

  _**TCEnhancedEntity Outputs**_ *(KeyValueList, Optional)*
  Outputs to be delivered as TCEnhancedEntity.
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

  **Return None on failure** *(Boolean, Default: Selected)*
  When an expression fails to evaluate, assign it the value None, and continue
  execution.

### Outputs

  - expression.action *(String)*
  - expression.errors *(StringArray)*

# Builtins


## Constants

  * e = 2.718281828459045
  * pi = 3.141592653589793
  * tau = 6.283185307179586
  * urlre = Regular Expression

        \b
          # Word cannot begin with special characters
          (?<![@.,%&#-])
          # Protocols are optional, but take them with us if they are present
          (?P<protocol>\w{2,10}:\/\/)?
          # Domains have to be of a length of 1 chars or greater
          ((?:\w|\&\#\d{1,5};)[.-]?)+
          # The domain ending has to be between 2 to 15 characters
          (\.([a-z]{2,15})
               # If no domain ending we want a port, only if a protocol is specified
               |(?(protocol)(?:\:\d{1,6})|(?!)))
        \b
        # Word cannot end with @ (made to catch emails)
        (?![@])
        # We accept any number of slugs, given we have a char after the slash
        (\/)?
        # If we have endings like ?=fds include the ending
        (?:([\w\d\?\-=#:%@&.;])+(?:\/(?:([\w\d\?\-=#:%@&;.])+))*)?
        # The last char cannot be one of these symbols .,?!,- exclude these
        (?<![.,?!-])

## Functions

  * `abs(x)`

    Absolute value of X

  * `acos(x)`

    Arc Cosine of X

  * `acosh(x)`

    Inverse Hyperbolic Cosine

  * `asin(x)`

    Arc Sine of X

  * `asinh(x)`

    Inverse Hyperbolic Sine

  * `atan(x)`

    Arc Tangent of X

  * `atanh(x)`

    Inverse Hyperbolic Tangent

  * `b64decode(s, altchars=None, validate=False, encoding='utf-8')`

    Base 64 decode of string

  * `b64encode(s, altchars=None, encoding='utf-8')`

    Base 64 encode of string

  * `bin(n, sign=True)`

    Return the binary value of int

  * `binary(s, encoding='utf-8', errors=None)`

    Convert object to binary string (bytes)

  * `bytes(s, encoding='utf-8', errors=None)`

    Convert object to binary string (bytes)

  * `ceil(x)`

    Ceiling of X

  * `center(s, width, fillchar=' ')`

    Center string in width columns

  * `choice(condition, true_result=None, false_result=None)`

    Choice of true_result or false_result based on condition

  * `chr(x)`

    Return character value of x

  * `conform(object_list, missing_value=None)`

    Conform objects in a list to have the same structure,
    using missing_value as the value of any missing key


  * `copysign(x, y)`

    Copy sign of X to Y

  * `cos(x)`

    Cosine of X

  * `cosh(x)`

    Hyperbolic Cosine

  * `csvread(data, header=False, convert=True, delimiter=',', quote='"', rows=0, columns=0)`

    Process data as a CSV File.  Return the data as a list of rows of columns,
    or if rows=1, return a list of columns).  If header is true, the first record
    is discarded.  If rows or columns is nonzero, the row or column count will
    be truncated to that number of rows or columns. If convert is True, numeric
    values will be returned as numbers, not strings

  * `csvwrite(data, delimiter=',', quote='"')`

    Write data in CSV format.  Returns a string

  * `datetime(datetime, date_format=None, tz=None)`

    Format a datetime object according to a format string

  * `degrees(x)`

    Convert X to degrees

  * `erf(x)`

    Error Function of X

  * `erfc(x)`

    Complimentary Error Function of X

  * `exp(x)`

    Math Exp of X

  * `expm1(x)`

    Math Expm1 of X

  * `factorial(x)`

    Factorial of X

  * `find(ob, value, start=None, stop=None)`

    Find index value in ob or return -1

  * `flatten(ob, prefix='')`

    Flatten a possibly nested list of dictionaries to a list, prefixing keys with prefix

  * `float(s)`

    Return floating point value of object

  * `format(s, *args, **kwargs)`

    Format string S according to Python string formatting rules.  Compound
    structure elements are access with bracket notation and without quotes
    around key names, e.g. `blob[0][events][0][source][device][ipAddress]`

  * `fuzzydist(hash1, hash2)`

    Return the edit distance between two fuzzy hashes

  * `fuzzyhash(data)`

    Return the fuzzy hash of data

  * `fuzzymatch(input1, input2)`

    Return a score from 0..100 representing a poor match (0) or
    a strong match(100) between the two inputs

  * `gamma(x)`

    Return the gamma function at X

  * `gcd(a, b)`

    Greatest Common Denominator of A and B

  * `hex(n, sign=True)`

    Return the hexadecimal value of int

  * `hypot(x, y)`

    Hypotenuse of X,Y

  * `index(ob, value, start=None, stop=None)`

    Index of value in ob

  * `int(s, radix=None)`

    Return integer value of object

  * `items(ob)`

    Items (key, value pairs) of dictionary

  * `jmespath(path, ob)`

    JMESPath search

  * `join(separator, *elements)`

    Join a list with separator

  * `json_dump(ob, sort_keys=True, indent=2)`

    Dump an object to a JSON string

  * `json_load(ob)`

    Load an object from a JSON string

  * `keys(ob)`

    Keys of dictionary

  * `len(container)`

    Length of an iterable

  * `lgamma(x)`

    Return the natural logarithm of the absolute value of the gamma function at X

  * `locale_currency(val, symbol=True, grouping=False, international=False, locale='EN_us')`

    Format a currency value according to locale settings

  * `locale_format(fmt, val, grouping=False, monetary=False, locale='EN_us')`

    Format a nubmer according to locale settings

  * `log(x, base=None)`

    Math Logarithm of X to base

  * `log10(x)`

    Math log base 10 of X

  * `log1p(x)`

    Math log1p of x

  * `log2(x)`

    Math log base 2 of X

  * `lower(s)`

    Lowercase string

  * `lstrip(s, chars=None)`

    Strip chars from left of string

  * `max(*items)`

    Return the greatest value of the list

  * `md5(data)`

    Return MD5 hash of data

  * `min(*items)`

    Return the least value of the list

  * `namevallist(ob, namekey='name', valuekey='value')`

    Return a dictionary formatted as a list of name=name, value=value dictionaries

  * `ord(char)`

    Return ordinal value of char

  * `pad(iterable, length, padvalue=None)`

    Pad iterable to length

  * `pformat(ob, indent=1, width=80, compact=False)`

    Pretty formatter for displaying hierarchial data

  * `pow(x, y)`

    Math X ** Y

  * `printf(fmt, *args)`

    Format arguments according to format

  * `prune(ob, depth=None, prune=(None, '', [], {}))`

    Recursively Prunes entries from the object,
    with an optional depth limit


  * `radians(x)`

    Convert X to radians

  * `range(start_or_stop, stop=None, step=None)`

    Return range of values

  * `refindall(pattern, string, flags='')`

    Find all instances of the regular expression in source

  * `rematch(pattern, string, flags='')`

    Regular expression match pattern to source

  * `replace(s, source, target)`

    Replace chars on S

  * `research(pattern, string, flags='')`

    Regular expression search pattern to source

  * `rstrip(s, chars=None)`

    Strip chars from right of string

  * `sha1(data)`

    Return SHA1 hash of data

  * `sha256(data)`

    Return SHA256 hash of data

  * `sin(x)`

    Sine of X

  * `sinh(x)`

    Hyperbolic Sine

  * `sort(*elements)`

    Sort array

  * `split(string, separator=None, maxsplit=-1)`

    Split a string into elements

  * `sqrt(x)`

    Square root of X

  * `str(s, encoding='utf-8')`

    Return string representation of object

  * `strip(s, chars=None)`

    Strip chars from ends of string

  * `structure(ob)`

    Return a reduced structure of the object, useful for comparisons

  * `sum(*elements)`

    Sum a list of elements

  * `tan(x)`

    Tangent of X

  * `tanh(x)`

    Hyperbolic Tangent

  * `timedelta(datetime_1, datetime_2)`

    Return the delta between time 1 and time 2

  * `title(s)`

    Title of string

  * `trunc(x)`

    Math Truncate X

  * `twoscompliment(n, bits=32)`

    Return the twos compliment of N with the desired word width

  * `unique(*args)`

    Return the list of unique elements of arguments, which may be a list of arguments, or a
    single argument that is a list.  Inputs are compared by converting them to
    sorted JSON objects, so dictionaries with the same keys and values but different
    order will count as duplicates.

  * `unnest(iterable)`

    Reduces nested list to a single flattened list.  [A, B, [C, D, [E, F]]
    turns into [A, B, C, D, E, F].

  * `update(target, source)`

    Updates one dictionary with keys from the other

  * `upper(s)`

    Uppercase string

  * `urlparse(urlstring, scheme='', allow_fragments=True)`

    Parse a URL into a six component named tuple

  * `urlparse_qs(qs, keep_blank_values=False, strict_parsing=False, encoding='utf-8', errors='replace', max_num_fields=None)`

    Parse a URL query string into a dictionary.  Each value is a list.

  * `values(ob)`

    Values of dictionary

# EBNF-Syntax

    The grammar for the expressions is below.  Production rules are prefixed by -> and are used
    to tell the parser what to do when that construct is identified.

    start:  eval

    eval: sum
        | eval "||" sum -> logical_or
        | eval "&&" sum -> logical_and
        | eval "or" sum -> logical_or
        | eval "and" sum -> logical_and
        | eval "==" sum -> equals
        | eval "!=" sum -> not_equals
        | eval "<" sum -> less_than
        | eval ">" sum -> greater_than
        | eval "<=" sum -> less_than_equal_to
        | eval ">=" sum -> greater_than_equal_to
        | "not" eval -> not_
        | eval "in" product -> in_
        | eval "not" "in" product -> not_in_

    sum: product
        | sum "+" product -> add
        | sum "-" product -> sub

    product: raise
        | product "*" raise -> mul
        | product "/" raise -> div
        | product "%" raise -> mod

    raise: atom
        | raise "**" atom -> pow

    atom: FLOAT    -> num_float
        | INT       -> num_int
        | "-" atom  -> neg
        | NAME      -> var
        | string
        | "(" eval_list ")" -> tuple_freeze
        | "[" eval_list "]" -> list_freeze
        | "{" dict_list "}" -> dict_freeze
        | NAME "(" arg_list ")" -> function
        | atom "[" atom "]" -> get
        | atom "[" optional_atom ":" optional_atom "]" -> get_slice
        | atom "." NAME -> getattr

    string: STRING     -> literal_
        | TCVARIABLE    -> tcvariable
        | SQUOTE_STRING -> literal_
        | string string -> concat_string

    dict_list: dict_assign         -> list_
        | dict_list "," dict_assign -> list_
        |                           -> list_

    dict_assign: eval ":" eval -> set_kwarg

    eval_list: eval
        | eval_list "," eval -> list_
        | eval_list ","      -> list_
        |                    -> list_

    arg: eval
        | NAME "=" eval -> set_kwarg

    arg_list: arg
        | arg_list "," arg  -> list_
        | arg_list ","      -> list_
        |                   -> list_

    optional_atom:  atom
        | -> none

    TCVARIABLE: /#[A-Za-z]+:\d+:[A-Za-z0-9_.]+!\w+/
    _STRING_INNER: /.*?/
    _STRING_ESC_INNER: _STRING_INNER /(?<!\\)(\\\\)*?/
    SQUOTE_STRING: "'" _STRING_ESC_INNER "'"
