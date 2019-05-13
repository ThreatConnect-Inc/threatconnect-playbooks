# Search Exabeam Data Lake
## Summary
This app is designed to allow you to query an Address or Host IOCs in Exabeam's Data Lake for matched events. This is useful when you would like to see if a particular IOC has been active in your environment.

## Dependencies
- Valid Exabeam Data Lake instance with working credentials.

## Input parameters
The app requires the following configuration parameters:

- **hostname**: Your Exabeam Data Lake hostname.

- **port**: The port that the Data Lake is running on (typically 8484).

- **query**: The query syntax that you want to send to the Data Lake (the query must be formatted in JSON, see below example).

- **username**: Your Exabeam Data Lake username.

- **password**: Your password coupled with the above username.

## Sample Query Syntax:

{
    "_source": ["Network", "src_ip"],
    "size": 300,
    "query" : {
        "bool": {
            "must": [
                {
                    "match": { "exa_category": "Network"}
                },
                {
                    "match": { "src_ip": "192.168.2.159"}
                }
            ]
        }
    }
}



## Output parameters
- #total	The count of matched hits or events. String
- #hits	The matched events' content (see below sample event).  String
- #json-out	The raw JSON output from the Data Lake.  String

## Sample Event
{"took": 7, "timed_out": false, "_shards": {"total": 29, "successful": 29, "failed": 0}, "hits": {"total": 6, "max_score": 2.641375, "hits": [{"_index": "exabeam-2019.04.17", "_type": "logs", "_id": "AWotbS7Kpq_QQNspZXYp", "_score": 2.641375, "_source": {"src_ip": "192.168.2.159"}}, {"_index": "exabeam-2019.04.17", "_type": "logs", "_id": "AWotiHumpq_QQNspZbvy", "_score": 2.6393352, "_source": {"src_ip": "192.168.2.159"}}, {"_index": "exabeam-2019.04.18", "_type": "logs", "_id": "AWot1qs4pq_QQNspZtqQ", "_score": 2.6175847, "_source": {"src_ip": "192.168.2.159"}}, {"_index": "exabeam-2019.04.18", "_type": "logs", "_id": "AWouBQbMpq_QQNspZ4hJ", "_score": 2.6175847, "_source": {"src_ip": "192.168.2.159"}}, {"_index": "exabeam-2019.04.17", "_type": "logs", "_id": "AWotl6F0pq_QQNspZezD", "_score": 2.601408, "_source": {"src_ip": "192.168.2.159"}}, {"_index": "exabeam-2019.04.17", "_type": "logs", "_id": "AWotqCp5pq_QQNspZirR", "_score": 2.601408, "_source": {"src_ip": "192.168.2.159"}}]}}


For more information on Exabeam's Data Lake offering, please refer to [https://www.exabeam.com/product/exabeam-data-lake/](https://www.exabeam.com/product/exabeam-data-lake/)