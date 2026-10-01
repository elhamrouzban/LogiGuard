# LogiGuard Database

## Overview

LogiGuard uses PostgreSQL as its operational relational database.

The database layer is implemented with SQLAlchemy ORM and the Psycopg PostgreSQL driver.

At this stage, the database infrastructure contains two main tables:

- `orders`
- `predictions`

The database is intended to support the application layer by storing order-level model inputs and model prediction history.

## PostgreSQL Database

A dedicated PostgreSQL database was created for the project:

```text
Database: logiguard
```

A dedicated PostgreSQL user was also created for the application:

```text
User: logiguard_user
```

The `logiguard` database is owned by `logiguard_user`.

The project connects to PostgreSQL using a database URL with the following structure:

```text
postgresql+psycopg://<user>:<password>@localhost:5432/logiguard
```

Database credentials should not be committed to Git.

## Database Package

The database-related Python code is located in:

```text
src/database/
├── __init__.py
├── connection.py
├── orm_models.py
└── create_tables.py
```

### `connection.py`

`connection.py` defines the shared SQLAlchemy database infrastructure.

It contains:

- the database connection URL
- the SQLAlchemy engine
- the session factory
- the declarative ORM base class

The SQLAlchemy `engine` manages communication between the Python application and PostgreSQL.

`SessionLocal` is the session factory that will later be used for database operations such as querying, inserting, updating, and committing records.

The shared `Base` class is inherited by all ORM models. This allows SQLAlchemy to register the database tables under a common metadata registry.

## ORM Models

The PostgreSQL table definitions are implemented in:

```text
src/database/orm_models.py
```

SQLAlchemy ORM models provide a Python representation of relational database tables.

The current ORM models are:

### `Order`

The `Order` model represents the `orders` table.

It stores the order-level features required by the machine-learning prediction pipeline, including:

- order identifier
- payment type
- customer segment
- customer state
- order country
- order region
- shipping mode
- total quantity
- total discount
- number of unique products
- number of unique categories
- number of unique departments
- order hour
- order day of week
- order month
- creation timestamp

Each `order_id` is unique in the `orders` table.

### `Prediction`

The `Prediction` model represents the `predictions` table.

It stores model prediction results, including:

- order identifier
- late-risk probability
- binary prediction
- risk label
- operating threshold
- model name
- prediction timestamp

The `order_id` field references the corresponding order in the `orders` table.

A single order may have multiple prediction records, allowing prediction history to be retained if the model is run again or a future model version is introduced.

## Table Relationship

The current relationship is:

```text
orders
   |
   | order_id
   |
   └── predictions
```

One order can therefore be associated with multiple prediction records.

## Creating the Database Tables

The table-creation script is located in:

```text
src/database/create_tables.py
```

It uses:

```python
Base.metadata.create_all(bind=engine)
```

`Base.metadata` contains the ORM table definitions registered through the shared `Base` class.

`create_all()` creates any registered tables that do not already exist.

`bind=engine` specifies that the tables should be created in the PostgreSQL database connected through the SQLAlchemy engine.

The script can be executed from the project root with:

```bash
python -m src.database.create_tables
```

Successful execution produces:

```text
Database tables created successfully.
```

## Verifying the Database

The PostgreSQL command-line client `psql` can be used to inspect the database directly.

Connect to the LogiGuard database with:

```bash
psql -U logiguard_user -d logiguard
```

Inside `psql`, list the available tables with:

```text
\dt
```

The expected tables are:

```text
orders
predictions
```

Inspect an individual table schema with:

```text
\d orders
```

or:

```text
\d predictions
```

Exit the PostgreSQL command-line client with:

```text
\q
```

The successful verification confirmed that both `orders` and `predictions` were created in the `logiguard` PostgreSQL database.

## Current Database Architecture

The current database architecture is:

```text
LogiGuard Python Application
        ↓
SQLAlchemy
        ↓
Psycopg
        ↓
PostgreSQL
        ↓
logiguard database
        ↓
orders
predictions
```

The next database integration stage will use these tables to store order records, retrieve model inputs, generate late-risk predictions, and persist prediction results.