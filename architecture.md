# Project Architecture

This document provides a high-level overview of the project architecture.

## High-Level Overview

The project follows a layered architecture that separates concerns into distinct components:

1.  **Models (Data Layer)**: Defines the shape and structure of our data. This is the single source of truth for our application's data schema.
2.  **Validators (Integrity Layer)**: Ensures that any data entering the database is valid and consistent. This layer is automatically triggered through before_* magic functions from SQLAlchemy.
3.  **Controllers (Business Logic Layer)**: Contains the core application logic for creating, reading, updating, and deleting data.
4.  **Database Engine**: Manages the connection to the database and handles session management.

This separation makes the codebase more modular, easier to test, and simpler to maintain.

## Directory Structure

```
.
├── src/
│   ├── classes.py         # Data Models (SQLAlchemy ORM Classes)
│   ├── controllers/       # Business Logic Controllers
│   ├── database.py        # Database Engine & Session Management
│   ├── enums.py           # Application-specific enumerations
│   ├── interfaces.py      # Abstract Protocols (e.g., Validator, PersistentController)
│   ├── validators/        # Concrete validation classes
│   └── api/               # Entry point for the frontend into the backend
└── tests/
    ├── conftest.py        # Pytest fixtures (e.g., database session)
    └── test_*.py          # Test suites for each component
```

### Core Components

-   **`src/classes.py`**: This is the most critical file for defining our data, models, and tables. It contains all the SQLAlchemy ORM models.
-   **`src/controllers/`**: This directory holds the business logic. Each controller is responsible for a specific domain (e.g., `UserCtrl`, `CalendarCtrl`). They use the database session to perform CRUD (Create, Read, Update, Delete) operations.
-   **`src/database.py`**: This file configures the database connection (`engine`) and provides a session factory (`get_db`). Makes it easy to switch databases from postgresql to something else like MySQL.
-   **`src/interfaces.py`**: Defines the "contracts" for our components using Python's `Protocol`. This helps ensure that all controllers and validators have a consistent structure.

### How to Add a New Feature (e.g., "Comments")

1.  **Define the Model**: Open `src/classes.py` and add a new `Comment` class that inherits from `Base`. Define its columns (e.g., `text`, `created_at`, foreign keys).
2.  **Create the Validator**: Open `src/validators.py` and add a `CommentValidator` class. Add rules to validate the comment data (e.g., text is not empty).
3.  **Hook the Validator**: In `src/classes.py`, add a SQLAlchemy event listener for the `Comment` class to automatically trigger your new `CommentValidator`.
4.  **Create the Controller**: Create a new file `src/controllers/comments.py`. Inside, create a `CommentCtrl` class that implements the `PersistentController` protocol (If database is used).
5.  **Write Tests**: Create a new file `tests/test_comments.py`. Add tests for creating, validating, and retrieving comments to ensure everything works as expected.

## Core Libraries

-   **SQLAlchemy**: The premier ORM for Python. We use it to map our Python classes to database tables and to interact with the database in a Pythonic way.
-   **Alembic**: A database migration tool that works with SQLAlchemy. It can compare the models in `src/classes.py` to the live database and automatically generate the SQL scripts needed to update the schema.
-   **Pytest**: A powerful and easy-to-use testing framework.
