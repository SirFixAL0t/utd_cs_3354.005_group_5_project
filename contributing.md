# Contributing to the Project

## Getting Started

### 1. Clone the Repository
First, clone the repository to your local machine:

```bash
git clone https://github.com/SirFixAL0t/utd_cs_3354.005_group_5_project software_engineering_project
cd software_engineering_project
```

### 2. Set Up a Virtual Environment

A common practice in the industry, at least with Python, is to create virtual environments to hold all dependencies, including python version, into the project itself and not pollute the operating system.
This isolates the project's dependencies from your global Python installation.

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS and Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

### 3. Install Dependencies

Install all the required dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Adding new dependencies to the project
After installing a new library or module, make sure you add it to the requirements.txt file so others can run your code without missing library errors

```bash
pip freeze > requirements.txt
```

## Development Workflow

### Running Tests

We use `pytest` for our testing framework. To run the entire test suite, simply run the following command from the root of the project:

```bash
pytest
```

This will automatically discover and run all the tests in the `tests/` directory. The test runner is configured in `tests/conftest.py` to use an in-memory SQLite database, so the tests will not affect our actual database.

### Linting

We use ruff for linting which wraps multiple linting strategies. To run it: 

```bash
ruff check .
# You can also run with auto fix for simple stuff the linter can fix for you
ruff check --fix .
```
Please run the linter before commiting and pushing to github
