# Summary

Given an array, this playbook sends each item in the array one at a time to another playbook. This allows you to run a playbook on each item of an array.

# Dependencies

n/a

# Usage

This playbook expects an array to be sent (as a string) in the body of an http POST request to the trigger of this playbook. It also requires a `link` query parameter providing the playbook trigger link to which you would like to send each item in the array. Each item in the array will be send to the playbook trigger link in the body of a request. A request to this app will look something like:

![Setup](images/array_serializer_setup.png)

# Use Cases

* Perform an action on each item in an array
