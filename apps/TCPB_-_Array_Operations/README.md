# Release Notes
## 1.0.0
* Initial Release

---

# Summary
This playbook App will take a StringArray and perform the selected operation on the array.

![Info](images/info.png)

## Operations
* Sort - Alphabetically sort the Array.
* Reverse Sort - Reverse alphabetically sort the Array.
* Sort Lowercase - Alphabetically sort the Array using lowercase values for keys.
* Lowercase - Lowercase each item in the Array.
* Titlecase - Titlecase each item of the Array (e.g., texas coverts to Texas).
* Uppercase - Uppercase each item in the Array.
* Duplicates - Return a set of duplicates values found in the Array.
* Unique - Returns a set of unique values from the Array.

# Dependencies
* tcex>=0.7,<0.8

# Input Definitions
* String Array - The StringArray to apply operation on.
* Operation - The operation to perform on the StringArray.

![Inputs](images/input.png)

# Output Definitions
* array.count (String) - The number of results in `array.results`.
* array.results (StringArray) - The resulting values from the operation.

![Outputs](images/output.png)

# Building

```
pip install tcex
tclib
tcpackage
```

# Local Testing

All the environment variables in `tcex.d/profiles/array_operations.json` file must be set on the local system.

```
tcrun --group qa-build
```