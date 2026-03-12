---
name: how-to-store-sqlite-as-nosql-store
description: Discover how to leverage SQLite's JSON support to build a NoSQL-like document store, complete with TTL-based expiration, within this powerful embedded database.
metadata:
  url: https://rodydavis.com/posts/sqlite/no-sql
  last_modified: Tue, 03 Feb 2026 20:04:37 GMT
---

# How to store SQLite as NoSQL Store


[SQLite](https://www.sqlite.org/) is a very capable edge database that can store various shapes of data.

[NoSQL databases](https://www.mongodb.com/nosql-explained#:~:text=Some%20say%20the%20term%20%E2%80%9CNoSQL,format%20other%20than%20relational%20tables.) are very popular due to the schema-less nature of storing of the data but it is totally possible to store these documents in SQLite.

SQLite actually has great [JSON support](https://www.sqlite.org/json1.html) and even supports [JSONB](https://sqlite.org/draft/jsonb.html).

## Create the table 

To store JSON documents we need to create a table to store the values as strings.

```
CREATE TABLE documents (
  path TEXT NOT NULL PRIMARY KEY,
  data TEXT,
  ttl INTEGER,
  created INTEGER NOT NULL,
  updated INTEGER NOT NULL,
  UNIQUE(path)
);
```

path

data

ttl

created

updated

/posts/1

{"id":1}

NULL

0

0

/posts/2

{"id":2}

NULL

0

0

/users/1

{"id":1}

NULL

0

0

The basic idea is to store a JSON object and an unique path.

There is an optional [TTL](https://www.cloudflare.com/learning/cdn/glossary/time-to-live-ttl/#:~:text=What%20is%20time%2Dto%2Dlive%20\(TTL\)%20in%20networking,CDN%20caching%20and%20DNS%20caching.) to automatically delete rows when they reach the stale date.

## Save a document 

To save a document we can encode our JSON as a string or binary and save in in the table with a unique path.

```
INSERT OR REPLACE 
INTO documents (path, data, ttl, created, updated) 
VALUES (:path, :data, :ttl, :created, :updated)
RETURNING *;
```

You can also use JSON functions to save the Object to a valid JSON string.

```
INSERT OR REPLACE 
INTO documents (path, data, ttl, created, updated) 
VALUES ("/posts/1", json('{"id" 1}'), NULL, 0, 0)
RETURNING *;
```

path

data

ttl

created

updated

/posts/1

{"id":1}

NULL

0

0

## Reading a document 

To read a document we just need the path. If a TTL is set we can [calculate if the current date](https://www.sqlite.org/lang_datefunc.html) is greater than the offset and not return the document.

```
SELECT * FROM documents 
WHERE path = :path
AND (
	(ttl IS NOT NULL AND ttl + updated < unixepoch())
	OR
	ttl IS NULL
);
```

path

data

ttl

created

updated

/posts/1

{"id":1}

NULL

0

0

## Get documents for a collection 

We can query all the docs for a given collection using some built-in functions and a path prefix:

```
SELECT *
FROM documents 
WHERE (
	path LIKE :prefix
	AND
	(LENGTH(path) - LENGTH(REPLACE(path, '/', ''))) = (LENGTH(:prefix) - LENGTH(REPLACE(:prefix, '/', '')))
)
AND (
	(ttl IS NOT NULL AND ttl + updated < unixepoch())
	OR
	ttl IS NULL
)
ORDER BY created;
```

It is expected to search for a :prefix with the `/%` at the end:

`"/my/path/%" // search for /my/path`

## Deleting expired documents 

Using the TTL field we can delete all expired documents:

```
DELETE FROM documents
WHERE ttl IS NOT NULL
AND ttl + updated < unixepoch();
```

## Demo