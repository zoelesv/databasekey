# Database Keys
![SQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![SQlite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## Introduction
A database key is an attribute or set of attributes that uniquely identifies a row in a table. Keys are important for relational databases because they establish relationships between tables. 

## Main key types
- [PRIMARY KEY](#PRIMARY-KEY)
- [FOREIGN KEY](#FOREIGN-KEY)
- [UNIQUE KEY](#UNIQUE-KEY)
- [SUPER KEY](#SUPER-KEY)
- [CANDIDATE KEY](#CANDIDATE-KEY)
- [ALTERNATIVE KEY](#ALTERNATIVE-KEY)

## Practical Uses of Database keys
Accelerating query times
![btree](/src/btree.png)
B-tree indexes speed up certain queries compared to having no index. Especially range searches, equality searches, and deletions.

## Keys to Uniqueness
![keys](/src/keys.png)
### SUPER KEY
Super key is a single key or a group of multiple keys that can uniquely identify tuples in a table.

### CANDIDATE KEY
A candidate key is a column or a combination of columns that uniquely identifies each row in a table.

### ALTERNATIVE KEY
Alternate keys are those candidate keys which are not the Primary key.

## Evolution of Database Key Creation
Manual primary key assignment could lead to conflicts, data duplication, and human errors, making scaling databases more challenging.

Autonomous Key Generation refers to automatic creation of primary keys by the database system or the application itself.

For example, Django - a Pythonic web application framework will automatically add an auto-increment IntegerField to hold the primary key to complete the schema if there isn't one defined, so you don’t need to set primary_key=True on any of your fields unless you want to override the default primary-key behavior. 

For more, see the commerce app.

Benefits:
- Data Integrity: ensures the uniqueness and integrity of primary keys, reducing the risk of data errors.
- Scalability: As applications scale, autonomous key generation systems can handle the creation of millions of keys efficiently.
- Simplicity: Developers can focus on application logic rather than managing key generation.

Challenges of AUTO-INCREMENT UID
![hotspot](/src/hotspots.png)
- Spanner uses key ranges to distribute data across servers, resulting in all insertions being directed to a single server responsible for all the workload.
Solution: UUID
- A Universally Unique Identifier (UUID) is a label used to uniquely identify a resource among all other resources of that type.

## Commerce app installation
Create or adjust database table with Django model in auctions/models.py
```
python3 -m venv env && source env/bin/activate
(env)$ pip install Django
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```
Check the schema in the auctions/migrations directory to see auto-increment primary key generated.

To see the database in the terminal
```
sqlite3 db.sqlite3
.tables
SELECT * FROM auctions_customers;
```

### PRIMARY KEY
A primary key is a unique column (or set of columns) assigned to relational database table(s) in order to uniquely identify each table entry. To easily parse the data in the table, a primary key is employed as a unique identifier. There shouldn't be a null primary key.

### FOREIGN KEY
A foreign key is a column (or set of columns) of data in one table that references certain data values, frequently the primary key values, in another table. In a relational database, foreign keys link together two or more tables.

### UNIQUE KEY
A unique Key is a specific value that is employed to prevent identical values from appearing in a column. To avoid duplicate values, a unique key in a table's primary function is to prevent them. However, the primary key also contains it when it comes to a unique value.

## SQL Query
Run the queries in file [query.sql](query.sql)

### Outputs
Customers table
![customers](/src/customers.png)

Orders table
![orders](/src/orders.png)

## Reference

|PRIMARY KEY|FOREIGN KEY|UNIQUE KEY|
|:-----:|:-----:|:-------:|
|Must contain unique values|Can contain duplicate values|Must contain unique values|
|Can not contain NULL values|Can contain NULL values|Can contain a NULL value|
|Only one per table|Can have more than one|Can have more than one|
|To identify records in a table uniquely|To make a relation between 2 tables|To identify records when they cannot have duplicate values|

https://www.postgresql.org/docs/current/sql-createtable.html

https://news.ycombinator.com/item?id=14523523

https://cloud.google.com/spanner/docs/schema-design#choosing_a_primary_key

## Authors
- Varsha
- Max
- Zoe