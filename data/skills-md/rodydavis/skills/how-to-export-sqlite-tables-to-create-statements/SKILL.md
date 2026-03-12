---
name: how-to-export-sqlite-tables-to-create-statements
description: Learn how to export your entire SQLite database schema, including tables and indexes, into runnable CREATE statements at runtime using Flutter and the `sqlite3` package.
metadata:
  url: https://rodydavis.com/posts/export-sqlite-dart
  last_modified: Tue, 03 Feb 2026 20:04:37 GMT
---

# How to Export SQLite Tables to CREATE Statements


In this article I will show you how to export all the tables and indexes in a [SQLite](https://www.sqlite.org/index.html) database to CREATE statements at runtime.

## Getting started 

Start by creating a new directory and [Flutter](https://flutter.dev/) project:

```
mkdir sqlite_introspect
cd sqlite_introspect
flutter create .
flutter pub add sqlite3 mustache_template
```

This will add the `sqlite3` package which uses FFI to call the native executable and mustache that we will use for templates later.

## Creating the database 

Creating the database can be done either in memory or based on a local file. For this example we will use in memory:

```
final Database db = sqlite3.openInMemory();
```

Don't forget to dispose of the database after use:

```
db.dispose();
```

## Defining the template 

Since we will be using [Mustache](https://mustache.github.io/) we can define the variables that we will pass to the template as JSON.

Create a `TableInfo` class that will store the fields and indexes:

```
class TableInfo {
  final String name;
  final List<Map<String, dynamic>> fields;
  final List<Map<String, dynamic>> indexes;

  TableInfo({
    required this.name,
    required this.fields,
    required this.indexes,
  });

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'fields': [
        for (var i = 0; i < fields.length; i++)
          {
            'index': i,
            'table': name,
            'isLast': i == fields.length - 1,
            ...fields[i],
          },
      ],
      'indexes': [
        for (var i = 0; i < indexes.length; i++)
          {
            'index': i,
            'table': name,
            'isLast': i == indexes.length - 1,
            ...indexes[i],
          },
      ],
    };
  }
}
```

Now we can create the Mustache template used to build up the CREATE statements:

```
const template = '''
{{#tables}}
CREATE TABLE {{name}} (
  {{#fields}}
  {{name}} {{#type}} {{.}}{{/type}}{{#notnull}} NOT NULL{{/notnull}}{{#pk}} PRIMARY KEY{{/pk}}{{#dflt_value}} DEFAULT {{.}}{{/dflt_value}}{{^isLast}},{{/isLast}}
  {{/fields}}
);
{{#indexes}}
CREATE {{#unique}} UNIQUE{{/unique}} {{name}}
ON {{table}}({{#values}} {{name}} {{/values}}{{^isLast}},{{/isLast}});
{{/indexes}}
{{/tables}}
''';
```

## Exporting the PRAGMA 

Now we can export the [PRAGMA](https://www.sqlite.org/pragma.html) for the database by exporting the list of tables, querying the column information and indexes about each one.

```
final tables = <TableInfo>[];
// Export table names
final tableNames = db
	.select("SELECT name FROM sqlite_master WHERE type='table';")
	.map((e) => e['name'] as String);
for (final t in tableNames) {
  // Export column information
  final info = db.select('PRAGMA table_info($t);');
  final tbl = TableInfo(name: t, fields: [], indexes: []);
  for (final c in info) {
    tbl.fields.add(c);
  }
  // Export index names
  final indexList = db.select('PRAGMA index_list($t);');
  for (final index in indexList) {
    final name = index['name'] as String;
    // Export index information
    final infos = db.select('PRAGMA index_info($name);');
    final indexValue = {...index, 'values': infos};
    tbl.indexes.add(indexValue);
  }
  tables.add(tbl);
}
```

## Rendering the template 

Now take the tables we just exported and pass them to the mustache template to render:

```
final tml = Template(template);
final args = {"tables": tables.map((e) => e.toJson()).toList()};
final str = tml.renderString(args);
print(str);
```

This will now print out all the tables and indexes as CREATE as valid SQL. 🎉