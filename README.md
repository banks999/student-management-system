# Student Management System

A Python project demonstrating Git branching, GitHub collaboration through Pull Requests, and automated testing with GitHub Actions.

## Project Structure

```
student-management-system/
├── student.py              # Core CRUD logic
├── test_student.py         # pytest suite (17 test cases)
├── requirements.txt        # pytest
├── README.md
└── .github/
    └── workflows/
        └── python.yml      # CI workflow (push + pull_request)
```

## Features

| Function | Description |
| --- | --- |
| `add_student(roll_no, name, course, marks)` | Adds a new record; rejects duplicate roll numbers and empty names. |
| `remove_student(roll_no)` | Deletes a record; returns `None` if not found. |
| `search_student(query)` | Searches by roll number, or by partial case-insensitive name. |
| `update_student(roll_no, ...)` | Updates any subset of name / course / marks. |
| `list_students()` | Returns all records sorted by roll number. |
| `export_students(path, format)` | **Bonus** — exports all records to CSV or JSON. |

Records are held in an in-memory dictionary keyed by roll number.

## Setup

```bash
# Clone the repository
git clone https://github.com/<your-username>/student-management-system.git
cd student-management-system

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the test suite
pytest -v

# Run the demo
python student.py
```

## Git Commands Used

**Initial setup and first push**

```bash
git init
git add .
git commit -m "Initial commit: student management system with CRUD and tests"
git branch -M main
git remote add origin https://github.com/<your-username>/student-management-system.git
git push -u origin main
```

**Feature branch and Pull Request**

```bash
git checkout -b feature-student-search
# ... modify search_student() ...
git add student.py test_student.py
git commit -m "feat: support partial case-insensitive name search in search_student()"
git push -u origin feature-student-search
```

A Pull Request was then raised on GitHub targeting `main`.

**Demonstrating a failing workflow**

```bash
git commit -am "test: introduce intentional bug in search_student()"
git push
# GitHub Actions run fails -> screenshot captured

git commit -am "fix: restore correct search_student() behaviour"
git push
# GitHub Actions run passes -> PR merged
```

**Bonus feature branch**

```bash
git checkout main
git pull origin main
git checkout -b feature-export
git add student.py test_student.py
git commit -m "feat: add export_students() supporting CSV and JSON"
git push -u origin feature-export
```

## GitHub Actions Workflow

`.github/workflows/python.yml` runs on every `push` to `main` or a `feature-**` branch, and on every `pull_request` targeting `main`.

Steps performed by the runner:

1. Check out the repository (`actions/checkout@v4`)
2. Set up Python 3.11 (`actions/setup-python@v5`)
3. Install dependencies from `requirements.txt`
4. Execute `pytest -v`

A red ✗ on the Pull Request blocks the merge until the tests pass; a green ✓ allows the branch to be merged into `main`.

## Test Coverage

The suite contains 17 test cases across five groups: adding students (including duplicate and validation errors), searching (by roll number, partial name, multiple matches, and no match), updating (single field, multiple fields, missing record), removing (success and missing record), ordering of `list_students()`, and the bonus export function (CSV, JSON, and unsupported format).

An `autouse` fixture clears the in-memory store before and after each test so that tests remain independent of execution order.
