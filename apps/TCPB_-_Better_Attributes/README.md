# Release Notes

## 1.0.0
* Initial Release


# Summary
This playbook app is to help assist users with getting more information about attributes.

the app will take in single values or arrays of values and will return a single JSON parsable string with the information about the attributes associaed to it.

the format for the data returned will look as below.

```
{
    "attributes": [
        {
            "id": 134664969,
            "type": "Cards",
            "value": "<Attribute Value>",
            "dateAdded": "2021-04-23T14:14:09Z",
            "lastModified": "2021-04-26T19:26:37Z",
            "displayed": false,
            "securityLabels": [
                {
                    "name": "TLP:GREEN",
                    "dateAdded": "2016-08-31T00:00:00Z"
                }
            ]
        }
    ],
    "indicatorValue": "<Value of indicator parsed>"
}
```

For arrays of indicators passed in, the app will return an array of the data format for each indicator provided, filtering can be done on the indicatorValue to retive the associated attributes.

# Dependencies
```tcex>=2.0.0,<2.1.0```

# Input Definitions
value -> indicator value
owner -> indicator owner
indicator_type -> type of indicator

# Output Definitions
better_attributes -> see formated json data above

