# HTML to JSON

This app converts HTML to JSON using Floyd Hightower's [HTML to JSON](https://gitlab.com/fhightower/html-to-json) package.

For example, this:

```
<head>
    <title>Test site</title>
    <meta charset="UTF-8">
</head>
```

Becomes this:

```
{
    'head': [
    {
        'title': [
        {
            'value': 'Test site'
        }],
        'meta': [
        {
            'attributes':
            {
                'charset': 'UTF-8'
            }
        }]
    }]
}
```

Or you can tell the app to only convert tables in the html as described [here](https://gitlab.com/fhightower/html-to-json#html-tables-to-json).

## Release Notes

### 0.1.0

* Initial Release
