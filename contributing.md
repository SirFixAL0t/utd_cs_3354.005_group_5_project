# Contributing to the Project

Thank you for your interest in contributing! This document provides a guide for setting up your development environment and contributing to the project.

## Getting Started

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Set Up a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies. This isolates the project's dependencies from your global Python installation.

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

*(Note: We will need to create a `requirements.txt` file. This can be done by running `pip freeze > requirements.txt` after installing the necessary libraries like `sqlalchemy`, `pytest`, etc.)*

## Development Workflow

### Running Tests

We use `pytest` for our testing framework. To run the entire test suite, simply run the following command from the root of the project:

```bash
pytest
```

This will automatically discover and run all the tests in the `tests/` directory. The test runner is configured in `tests/conftest.py` to use an in-memory SQLite database, so the tests will not affect your development database.

### Linting

We use `flake8` for linting our code to ensure it adheres to a consistent style. To check your code for any linting errors, run:

```bash
flake8 src/ tests/
```

It is recommended to run the linter before committing your changes to ensure your code matches the project's style guidelines.

### Submitting Changes

1.  Create a new branch for your feature or bug fix.
2.  Make your changes and commit them with a clear and descriptive commit message.
3.  Ensure all tests pass (`pytest`).
4.  Ensure the linter passes (`flake8 src/ tests/`).
5.  Push your branch to the remote repository and open a pull request.
