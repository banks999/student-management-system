"""Student Management System.

A small in-memory CRUD module for managing student records.
Records are stored in a module-level dictionary keyed by roll number:

    {roll_no: {"roll_no": int, "name": str, "course": str, "marks": float}}
"""

import csv
import json

# In-memory store for student records.
students = {}


def _validate_roll_no(roll_no):
    """Return roll_no as an int, or raise ValueError if it is not valid."""
    try:
        roll_no = int(roll_no)
    except (TypeError, ValueError):
        raise ValueError("Roll number must be an integer.")
    if roll_no <= 0:
        raise ValueError("Roll number must be a positive integer.")
    return roll_no


def add_student(roll_no, name, course, marks=0.0):
    """Add a new student record.

    Returns the newly created record.
    Raises ValueError if the roll number already exists or inputs are invalid.
    """
    roll_no = _validate_roll_no(roll_no)

    if not name or not str(name).strip():
        raise ValueError("Student name cannot be empty.")

    if roll_no in students:
        raise ValueError(f"Student with roll number {roll_no} already exists.")

    record = {
        "roll_no": roll_no,
        "name": str(name).strip(),
        "course": str(course).strip(),
        "marks": float(marks),
    }
    students[roll_no] = record
    return record


def remove_student(roll_no):
    """Remove a student by roll number.

    Returns the removed record, or None if no such student exists.
    """
    roll_no = _validate_roll_no(roll_no)
    return students.pop(roll_no, None)


def search_student(query, limit=None):
    """Search for students by roll number or by (partial, case-insensitive) name.

    Passing an int or a digit-string searches by roll number and returns a list
    with at most one record. Any other string performs a partial name match and
    may return several records. Returns an empty list when nothing matches.
    """
    if query is None:
        return []

    # Roll-number search.
    if isinstance(query, int) or (isinstance(query, str) and query.strip().isdigit()):
        roll_no = int(query)
        record = students.get(roll_no)
        return [record] if record else []

    # Partial, case-insensitive name search.
    term = str(query).strip().lower()
    if not term:
        return []

    matches = [rec for rec in students.values() if term in rec["name"]]
    return matches[:limit] if limit else matches

def update_student(roll_no, name=None, course=None, marks=None):
    """Update one or more fields of an existing student record.

    Returns the updated record, or None if the student does not exist.
    """
    roll_no = _validate_roll_no(roll_no)
    record = students.get(roll_no)
    if record is None:
        return None

    if name is not None:
        if not str(name).strip():
            raise ValueError("Student name cannot be empty.")
        record["name"] = str(name).strip()

    if course is not None:
        record["course"] = str(course).strip()

    if marks is not None:
        record["marks"] = float(marks)

    return record


def list_students():
    """Return all student records sorted by roll number."""
    return [students[roll] for roll in sorted(students)]


def export_students(file_path, file_format="csv"):
    """Export all student records to a CSV or JSON file. (Bonus feature)

    Returns the number of records written.
    Raises ValueError for an unsupported format.
    """
    file_format = str(file_format).strip().lower()
    records = list_students()

    if file_format == "csv":
        with open(file_path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(
                fh, fieldnames=["roll_no", "name", "course", "marks"]
            )
            writer.writeheader()
            writer.writerows(records)
    elif file_format == "json":
        with open(file_path, "w", encoding="utf-8") as fh:
            json.dump(records, fh, indent=2)
    else:
        raise ValueError(f"Unsupported export format: {file_format}")

    return len(records)


def clear_students():
    """Remove every record. Used by tests to guarantee a clean state."""
    students.clear()


if __name__ == "__main__":
    add_student(101, "Riya Sharma", "Data Science", 88.5)
    add_student(102, "Kabir Mehta", "Business Analytics", 76.0)
    add_student(103, "Ananya Rao", "Data Science", 91.0)

    print("All students:", list_students())
    print("Search 'ri':", search_student("ri"))
    print("Search 102:", search_student(102))

    update_student(102, marks=81.5)
    print("After update:", search_student(102))

    remove_student(103)
    print("After removal:", list_students())
