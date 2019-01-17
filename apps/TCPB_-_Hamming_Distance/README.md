# Hamming Distance

Playbook app to find the [Hamming Distance](https://en.wikipedia.org/wiki/Hamming_distance) (the number of positions at which the corresponding symbols are different) between two strings.

For example, given `abc` and `abd`, the hamming distance is 1 (only the last letter is different). Given `abc` and `cbd`, the hamming distance is 2 (The first and last letters of the two strings are different).

# Usage

## Inputs

This playbook has two, required inputs:

- `string_1` (required): a string whose length you would like to compare with `string_2`
- `string_2` (required): a string whose length you would like to compare with `string_1`

Both `string_1` and `string_2` must be **the same length**.

## Outputs

The app outputs two variables:

- `hammingDistance`: The hamming distance (e.g. )
- `hammingDistance.percentage`: The hamming distance as a percentage of the length of the input strings (e.g. )

## Release Notes

### 0.1.0

* Initial Release
