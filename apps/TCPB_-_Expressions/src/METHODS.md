
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

    Set a specfic key in a dictionary.  Returns the value.

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

  * `format(s, *args, default=<object object at 0x10c7fe7a0>, **kwargs)`

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

  * `research(pattern, string, flags='')`

    Regular expression search pattern to source

  * `rexxparse(source, template, strip=False, convert=False, **kwargs)`

    REXX parse of source using template.  If strip is True, values are stripped,
    if convert is True, values are converted to float or int if possible.  Any other
    keyword arguments are made available for indirect pattern substitution, in
    addition to the standard variables.

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
