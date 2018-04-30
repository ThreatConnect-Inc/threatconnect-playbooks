# Summary

This playbook attempts an action until it is successful. In this sense, it is a bit like a 'pause' or 'wait' command that will wait until the given action is successful before moving on.

# Dependencies

n/a

# Usage

This playbook is triggered by an HTTP request with the following query parameters:

- `count`: The number of times the action has been attempted (when triggering this playbook, you will usually want to set this value to zero)
- `link`: The http trigger link to the playbook with the action you would like to perform
- `max`: The maximum number of times to attempt the action

The basic algorithm is as follows:

1. Attempt an http request to the playbook specified by the `link` URL query parameter.

2a. If the http request from step 1 works: we're done!

2b. If the http request from step 1 does not work (returns 40X error):
    - Increment the count which keeps track of the number of times we have tried to trigger the other playbook
    - If the count is less than the maximum number of attempts: wait for twenty seconds and make another attempt
    - If the count is equal to the maximum number of attempts: stop and send a message (by default, a slack message)

# Use Cases

* Wait until a condition is true before proceeding
* Attempt an action until the action is successful
