---
weight: 5
---

# Amazon DynamoDB

Amazon DynamoDB is a serverless non-relational database. It is called non-relational because it does not follow a fixed tabular schema design like how a relational database would force you to. There are different variations of non-relational databases, such as key-value database, in-memory database, document database, and a graph database. You can think of DynamoDB as a mix of a key-value and document database model. In a key-value database, data is stored as key-value pairs. The key acts as an identifier so DynamoDB would know where in the storage it will locate and retrieve the value associated with the key. The value for a key can be a simple `String` data, a `number`, a `Boolean` value, a binary, a list, or even a complex data structure like a nested JSON document.

DynamoDB provides high-throughput and single-digit latency performance at any scale, so it’s great for use cases requiring fast retrieval access, such as high-web traﬃc or gaming applications. Like any other serverless product in AWS, DynamoDB is fully managed and requires zero administration, so tasks such as patching and updating are no longer your concern.

By default, DynamoDB replicates data across multiple availability zones within a region. It has built-in fault tolerance capability and can automatically adjust capacity based on the volume of requests. Unlike a regular relational database, you don’t need to provide a database endpoint, username, or password when connecting to DynamoDB. You simply have to specify the table name and use DynamoDB API commands that correspond to a CRUD operation that you need. Permissions to access DynamoDB are handled by the IAM service

## Core Components

* Table
    * a collection of related items
    * can have zero or more items
* Item
    * represents a single record that you want to insert into a table
    * each item can have one or more attributes
* Attribute
    * a fundamental data element of an item
* Primary keys
    * Partition key (Required)
        * uniquely identifies each item in a table 
        * a partition key value is used as an input to the internal hash function in DynamoDB. The output from that hash function determines the partition or the physical internal storage in which the item will be stored or retrieved.
    * Sort key (Optional)
        * gives you additional flexibility when querying data
        * a table with both Partition key and Sort key can have multiple items with similar partition key values given that they have unique sort key values. 
        * can sort data in order.

**References:**

- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html
- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html


## Local Secondary Index vs. Global Secondary Index (LSI vs. GSI)

DynamoDB supports two secondary indexes: Global Secondary Index (GSI) and Local Secondary Index (LSI). A Global Secondary Index can have a different partition key and sort key from that of your base table. You can think of it as a secondary table that can have a completely different schema design. A Global Secondary Index is ‘global’ in the sense that a query on the index can span all of the data in the base table across all partitions.


**Key differences:**

|   | Global Secondary Index | A Local Secondary Index |
|---|---|----|
| Key Attributes | A secondary index can have a partition key, sort key, and non-key attributes | A secondary index can have a sort key and non-key attributes only |
| Span query | Queries span all data in the base table, across all partitions | Queries are scoped on the partition key of its base table |
| Index operations | Can be created anytime | Can be created only during the creation of a table |
| Size restrictions per partition key value | No restriction | Total size of indexed items under a partition key value must not exceed 10GB |
| Read consistency | Eventual Consistency | Supports both Eventual and Strong Consistency |
| Provisioned Throughput consumption | Has its own provisioned throughput for read and write activities | Consumes capacity units from its base table |
| Projected Attributes | You can only request attributes that are projected in the GSI | Requested attributes that are not projected into the LSI are fetched from the base table by DynamoDB automatically |

**References:**

- https://aws.amazon.com/blogs/database/how-to-design-amazon-dynamodb-global-secondary-indexes /
- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SecondaryIndexes.html
- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/LSI.html 



## Projections
When creating an LSI or GSI you set the list of attributes that you want to project or copy from the base table to the secondary index. The primary keys (partition and sort key) are **always** projected into the secondary index, but you can also specify non-key attributes that will be projected into the index.

Three options in projecting attributes:

1. `KEYS_ONLY` - all items of an index will only contain the base table’s primary keys that you set.
2. `INCLUDE` - allow you to choose other non-key attributes that will be included along with the primary keys of your base table.
3. `ALL` - all attributes from your base table will be copied into your secondary index.

**Reference:**

- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html


## Scan & Query operations
A Query operation performs a direct look-up to specific items you want to search for based