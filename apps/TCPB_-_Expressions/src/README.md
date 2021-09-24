# Expressions

# Release Notes

### 1.0.10 (2021-09-23)

* add URL method
* add StringArray outputs on the *Many forms
* add partitionedmerge function
* add round function
* fix encapsulation/deencapsulation of top level "naked" TC variables which are structures like TCEntities (allow passthrough of entity)

### 1.0.9 (2021-08-20)

* add dict function
* add report function
* add Trace subexpression advanced option
* fix encapsulation/deencapsulation of embedded TC variables

### 1.0.8 (2021-05-24)

* Add uuid3, uuid4, uuid5, xmlread, xmlwrite
* add keys argument to prune
* important rexxparse fix for patterns looking for "."
* add xmlread and xmlwrite functions
* add chardet, fang, defang, extract_indicators, indicator_patterns
* add pivot to pivot a list of lists
* add build to create lists of dictionaries
* update function now allows lists of dictionaries, adds replace parameter
* add merge function
* add fetch_indicators, indicator_types
* add default value to format in case of missing values
* add set to write into a dictionary

### 1.0.7 (2021-04-20)

* Fix list expressions with only one element to return list
* Add rexxparse function
* Fix format function to allow dot notation

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


# Category

- Utility

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

  **Trace subexpression execution** *(Boolean, Default: Unselected)*
  Trace execution of subexpresssions at DEBUG level in the application's log.

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

  _**Outputs**_ *(KeyValueList, Optional)*
  Outputs and output expressions for each output.  These may reference defined variables
  but may not refer to outputs not yet evaluated.  Outputs will be generated as a
  single output only, with list outputs being converted to JSON strings.
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity, TCEnhancedEntityArray

### *Advanced*

  _**StringArray Outputs**_ *(KeyValueList, Optional)*
  Outputs to be delivered as StringArray
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity

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

  **Trace subexpression execution** *(Boolean, Default: Unselected)*
  Trace execution of subexpresssions at DEBUG level in the application's log.

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

  **Trace subexpression execution** *(Boolean, Default: Unselected)*
  Trace execution of subexpresssions at DEBUG level in the application's log.

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

  _**StringArray Outputs**_ *(KeyValueList, Optional)*
  Outputs to be delivered as StringArray
  > **Allows:** String, StringArray, Binary, BinaryArray, KeyValue, KeyValueArray, TCEntity, TCEntityArray, TCEnhancedEntity

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

  **Trace subexpression execution** *(Boolean, Default: Unselected)*
  Trace execution of subexpresssions at DEBUG level in the application's log.

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

  * `alter(dictionary, key, value)`

    Set a specific key in a dictionary.  Returns the value.

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

  * `build(*lists, keys=())`

    Constructs a sequence of dictionaries based on the lists, such
    that each dictionary contains the corresponding key for each list
    from the keys value, and value from each list, respectively.
    Columns without a key are ignored.  Columns that are longer than
    the shortest column are truncated.

  * `bytes(s, encoding='utf-8', errors=None)`

    Convert object to binary string (bytes)

  * `ceil(x)`

    Ceiling of X

  * `center(s, width, fillchar=' ')`

    Center string in width columns

  * `chardet(byteseq)`

    Return a dictionary with the guessed character encoding
    of byteseq, the confidence of the encoding, and the estimated
    language.

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

  * `defang(s)`

    Return a defanged representation of string, ie, one with
    textual indicators of compromise converted to the defanged state

  * `degrees(x)`

    Convert X to degrees

  * `dict(**kwargs)`

    Return a dictionary of arguments

  * `erf(x)`

    Error Function of X

  * `erfc(x)`

    Complimentary Error Function of X

  * `exp(x)`

    Math Exp of X

  * `expm1(x)`

    Math Expm1 of X

  * `extract_indicators(data, ignore=None, dedup=True, fang=False, convert=True)`

    Extract IOCs from data, which may be bytes or string.
    If fang is true, data is re-fanged before processing. This option is
    ignored if the input is binary.
    Any entity match on the ignore list will be ignored.
    If convert is true, bytesmode matches will be converted to utf-8, or
    the specified conversion e.g. convert='latin-1'.
    Returns a list of (indicator, value) tuples.  If dedup is True,
    duplicate results are not returned.

  * `factorial(x)`

    Factorial of X

  * `fang(s)`

    Return a fanged representation of string, ie, one with
    textual indicators of compromise reverted from the defanged state

  * `fetch_indicators(*search_values, default_type=None)`

    Fetches available indicators from ThreatConnect based on
    search_values.  A search value is either an indicator value (which uses
    the default_type as the indicator type) or a (type, value) pair.  If
    only one search_value is passed in, it may be a list of search_values.

    Returns a list of [(indicator_type, indicator_value, api_entity, indicator), ...],
    but the api_entity, result, and owners will be None if that
    indicator was not found.


  * `find(ob, value, start=None, stop=None)`

    Find index value in ob or return -1

  * `flatten(ob, prefix='')`

    Flatten a possibly nested list of dictionaries to a list, prefixing keys with prefix

  * `float(s)`

    Return floating point value of object

  * `format(s, *args, default=<object object at 0x1051b09b0>, **kwargs)`

    Format string S according to Python string formatting rules.  Compound
    structure elements may be accessed with dot or bracket notation and without quotes
    around key names, e.g. `blob[0][events][0][source][device][ipAddress]`
    or `blob[0].events[0].source.device.ipAddress`.  If default is set,
    that value will be used for any missing value.

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

  * `indicator_patterns()`

    Returns a dictionary of regular expression patterns for indicators
    of compromise, based on ThreatConnect Data.

  * `indicator_types()`

    Return the ThreatConnect Indicator Types

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

  * `kvlist(dictlist, key='key', value='value')`

    Return a list of dictionaries as a single dictionary with the list
    item's key value as the key, and the list item's value value as the value.
    Duplicate keys will promote the value to a list of values.

  * `len(container)`

    Length of an iterable

  * `lgamma(x)`

    Return the natural logarithm of the absolute value of the gamma function at X

  * `locale_currency(val, symbol=True, grouping=False, international=False, locale='EN_us')`

    Format a currency value according to locale settings

  * `locale_format(fmt, val, grouping=False, monetary=False, locale='EN_us')`

    Format a number according to locale settings

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

  * `merge(*iterables, replace=False)`

    Merges a list of iterables into a single list.
    If the iterables are dictionaries, they are updated into a
    single dictionary per row.  If replace is true, subsequent
    columns overwrite the original values.  The result length
    is constrained to the shortest column.

  * `min(*items)`

    Return the least value of the list

  * `namevallist(ob, namekey='name', valuekey='value')`

    Return a dictionary formatted as a list of name=name, value=value dictionaries

  * `ord(char)`

    Return ordinal value of char

  * `pad(iterable, length, padvalue=None)`

    Pad iterable to length

  * `partitionedmerge(array1, array2)`

    Merges two arrays of strings to a single array with ordering
    preserved between partitions in the arrays.  Common lines are partitions
    subject to the ordering of the partitions being the same in each array.

    For example partitionedmerge(['A', 'a1', 'a2', 'B', 'b1', 'b2', 'D'],
    ['A', 'a3', 'a4', 'B', 'b3', 'b4', 'C', 'c1', 'c2', 'D'])

    is

    ['A', 'a1', 'a2', 'a3', 'a4', 'B', 'b1', 'b2', 'b3', 'b4', 'C', 'c1', 'c2', 'D']

    The values 'A', 'B', and 'D' act as partition lines for the merge.


  * `pformat(ob, indent=1, width=80, compact=False)`

    Pretty formatter for displaying hierarchial data

  * `pivot(list_of_lists, pad=None)`

    Pivots a list of lists, such that item[x][y] becomes item[y][x].
    If the inner lists are not of even length, they will be padded with
    the pad value.

  * `pow(x, y)`

    Math X ** Y

  * `printf(fmt, *args)`

    Format arguments according to format

  * `prune(ob, depth=None, prune=(None, '', [], {}), keys=())`

    Recursively Prunes entries from the object,
    with an optional depth limit.  The pruned values, and
    optionally prune keys may be specified.  If any dictionary
    has a key in keys, that dictionary element will be removed.


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

  * `report(data, columns=None, title=None, header=True, width=None, prolog=None, epilog=None, sort=None, filter=None)`

    Generates a text report of data in columnar format.  Data is either a list of
    dictionaries, or a list of lists of columnar data.  If a list of lists,
    then the first row is the header row of the data.

    Columns is a list of row specifiers or a single row specifier, which is a list of
    column definitions.  If there are multiple row specifiers, each record takes up
    multiple output rows.

    A row specifier is either an ordered dictionary of name: column specifier or
    a list of (name, column specifier) tuples.

    A column specifier is width[:height][/option[=value]][/option[=value]]...
    If rows are lists of lists (e.g. CSV data) and no column specifiers are used, the
    widths will be automatically calculated.

    Options:

    - align=left|right|center

    - value=format    - format for values e.g. {lineno}.
    to add a . after lineno

    - error=value     - value to use if the value= format causes an error

    - notrim          - Don't trim leading/trailing space

    - hang=n          - Hanging paragraph by N spaces

    - indent=n        - Indent paragraph by N spaces

    - split=n         - split at n% through the column (default 80)
    if necessary

    - label=string    - heading label

    - doublenl        - Double newlines (ie, add line after paragraph)

    - nohyphenate     - Don't hyphenate value

    If sort is specified, it is a column or list of columns to sort by, with the column
    name optionally prefixed with a '-' to do a descending sort.

    If filter is specified, it is an expression that must be true for that record to appear
    in the result, e.g. filter="salary>70000".


  * `research(pattern, string, flags='')`

    Regular expression search pattern to source

  * `rexxparse(source, template, strip=False, convert=False, **kwargs)`

    REXX parse of source using template.  If strip is True, values are stripped,
    if convert is True, values are converted to float or int if possible.  Any other
    keyword arguments are made available for indirect pattern substitution, in
    addition to the standard variables.

  * `round(number, digits=0)`

    Round number to digits decimal places

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

  * `update(target, source, replace=True)`

    Updates one dictionary with keys from the other. If the target is
    a list of dictionaries, each dictionary will be updated.  If replace
    is false, existing values will not be replaced.

  * `upper(s)`

    Uppercase string

  * `url(method, url=None, **kwargs)`

    A direct dispatch of requests.request with an external session.  See
    https://docs.python-requests.org/en/latest/api for full API details.
    Returns a Response object, but callable methods on the response are
    not callable; retrieve the status via the .status_code attribute, or the content
    via the .content or .text attribute.

    If the URL is not specified, the first argument is assumed to be the URL
    and the method will default to 'GET'.

    If not specified, a timeout parameter of 30 seconds will be applied.
    The stream argument will *always* be set to True.
    The proxies argument will default to the system specified proxies.

    URL requests are throttled to one request every 3 seconds.

    If there is a json result, the json method on the result will
    be replaced with a json attribute that is the result of the json
    method, otherwise the json attribute will be set to None.

    Expressions-specific kwargs:
    rate=request rate per period  (default: 20)
    period=number of seconds in a period (default: 60)
    burst=number of requests to burst before throttling (default: 0)

    Only one rate throttle is maintained; switching throttles with multiple
    url function expressions will not yield intended results.


  * `urlparse(urlstring, scheme='', allow_fragments=True)`

    Parse a URL into a six component named tuple

  * `urlparse_qs(qs, keep_blank_values=False, strict_parsing=False, encoding='utf-8', errors='replace', max_num_fields=None)`

    Parse a URL query string into a dictionary.  Each value is a list.

  * `uuid3(namespace, name)`

    Generate a UUID based on the MD5 hash of a namespace and a name.
    The namespace may be a UUID or one of 'dns', 'url', 'oid', or 'x500'.


  * `uuid4()`

    Generate a random UUID

  * `uuid5(namespace, name)`

    Generate a UUID based on the SHA-1 hash of a namespace and a name.
    The namespace may be a UUID or one of 'dns', 'url', 'oid', or 'x500'.


  * `values(ob)`

    Values of dictionary

  * `xmlread(xmldata, namespace=False, strip=True, convert=True, compact=False)`

    Constructs an object from XML data.  The XML data should have
    a single root node.  If namespace is True, the resolved namespace will
    be prefixed to tag names in braces, i.e. {namespace}tag.  If strip
    is True, values will be stripped of leading and trailing whitespace.
    If convert is True, numeric values will be converted to their numeric
    equivalents.  If compact is true, the object will be compacted to
    a more condensed form if possible.  Attribute names will be prefixed
    with @ in the corresponding output.


  * `xmlwrite(obj, namespace=False, indent=0)`

    Converts an object to XML.  If namespace is True or a dictionary,
    namespace prefixed values will be converted to a derived or specified
    namespace value.  The namespace dictionary should be in the form
    {key: namespace} and will be used to turn the namespace back into the
    key. If indent is nonzero, an indented XML tree with newlines will
    be generated.  If namespaces are used, the caller must add the
    `xmlns` attributes to an enclosing scope.

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
