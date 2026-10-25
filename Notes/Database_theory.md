# DataBase Theory

> **Database**: A collection of data that can be easily accessed and managed.

> We operate on a database using a database management system.
> SQL stands for Structured Query Language

<!-- Relational Databases -->
- MySQL
- PostgresSQL
- Oracle
- SQL server

##### We will Primalrarily be working with PostgresSQL
---
## PostgresSQL Database
- Each instance of postgres can be carved into multiple seperate databases.
- By default every Postgres installation comes with one database already called "postgres"
- This is important as postgres requires you to specify the name of a database to make a connection.

---
## Tables
> A table represents a subject/event in an application.
> The tables created in this will be having a simple and obvious relationship hence the name, relational database.
### Columns vs Rows
- Each column represents a different attribute.
- Each row represents a new data entry in the table.
- Postgres Datatypes:
    - ![Data Types in Postgres and Python](./Images/Datatypes.png)