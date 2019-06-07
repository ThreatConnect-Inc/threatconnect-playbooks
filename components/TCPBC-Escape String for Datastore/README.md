# Escape String for Datastore

If you're trying to store an object or array in the [datastore](https://pb-constructs.hightower.space/playbooks/introductions/datastore) as a string, you will first need to escape all of the quotations in the object/array. This component is designed to do that.

**NOTE:** There are two versions of this component depending on which version of ThreatConnect you are running. If you are running a version after 5.6, use `[utility] Escape String for Datastore - post 5.6.pbx`; otherwise, use `[utility] Escape String for Datastore - pre 5.7.pbx`.

## Input

As input, this component requires a string.

## Output

This component returns the input item with quotation marks and newlines escaped for storage in the datastore.
