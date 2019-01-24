# Addition and Subtraction

This component is a wrapper for [https://newton.now.sh/](https://newton.now.sh/) which allows for simple operations like addition and subtraction.

## Why not use http://api.mathjs.org/?

[http://api.mathjs.org/](http://api.mathjs.org/) is limited when working with large numbers because results greater than or equal to 100,000 get converted into scientific notation (e.g. [http://api.mathjs.org/v1/?expr=99999%2B1](http://api.mathjs.org/v1/?expr=99999%2B1)).

## Usage

To use this playbook component, provide the expression you would like to compute (e.g. `1+2`). The component will return the result of the computation as the `result` variable.
