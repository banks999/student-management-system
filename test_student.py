"""Pytest suite for the Student Management System."""

import json

import pytest

import student
from student import (
    add_student,
    clear_students,
    export_students,
    list_students,
    remove_student,
    search_student,
    update_student,
)


@pytest.fixture(autouse=True)
def fresh_store():
    """Reset the in-memory store before and after every test."""
    clear_students()
    yield
    clear_students()


@pytest.fixture
def sample_students():
    """Three seeded students used by several tests."""
    add_student(101, "Riya Sharma", "Data Science", 88.5)
    add_student(102, "Kabir Mehta", "Business Analytics", 76.0)
    add_student(103, "Ananya Rao", "Data Science", 91.0)


# --------------------------------------------------------------------------
# add_student
# --------------------------------------------------------------------------

def test_add_student_creates_record():
    record = add_student(101, "Riya Sharma", "Data Science", 88.5)
    assert record == {
        "roll_no": 101,
        "name": "Riya Sharma",
        "course": "Data Science",
        "marks": 88.5,
    }
    assert len(student.students) == 1


def test_add_student_duplicate_roll_no_raises():
    add_student(101, "Riya Sharma", "Data Science")
    with pytest.raises(ValueError, match="already exists"):
        add_student(101, "Someone Else", "Business Analytics")


def test_add_student_empty_name_raises():
    with pytest.raises(ValueError, match="name cannot be empty"):
        add_student(104, "   ", "Data Science")


def test_add_student_invalid_roll_no_raises():
    with pytest.raises(ValueError, match="must be an integer"):
        add_student("abc", "Riya Sharma", "Data Science")


# --------------------------------------------------------------------------
# search_student
# --------------------------------------------------------------------------

def test_search_student_by_roll_no(sample_students):
    results = search_student(102)
    assert len(results) == 1
    assert results[0]["name"] == "Kabir Mehta"


def test_search_student_by_partial_name_is_case_insensitive(sample_students):
    results = search_student("sharma")
    assert len(results) == 1
    assert results[0]["roll_no"] == 101


def test_search_student_partial_name_returns_multiple_matches(sample_students):
    add_student(104, "Riya Nair", "Data Science", 70.0)
    results = search_student("riya")
    assert {rec["roll_no"] for rec in results} == {101, 104}


def test_search_student_not_found_returns_empty_list(sample_students):
    assert search_student(999) == []
    assert search_student("Nonexistent") == []


# --------------------------------------------------------------------------
# update_student
# --------------------------------------------------------------------------

def test_update_student_changes_marks(sample_students):
    updated = update_student(102, marks=81.5)
    assert updated["marks"] == 81.5
    assert search_student(102)[0]["marks"] == 81.5


def test_update_student_changes_multiple_fields(sample_students):
    updated = update_student(101, name="Riya S. Sharma", course="MLOps")
    assert updated["name"] == "Riya S. Sharma"
    assert updated["course"] == "MLOps"
    assert updated["marks"] == 88.5  # untouched


def test_update_student_missing_record_returns_none():
    assert update_student(999, marks=50) is None


# --------------------------------------------------------------------------
# remove_student
# --------------------------------------------------------------------------

def test_remove_student_deletes_record(sample_students):
    removed = remove_student(103)
    assert removed["name"] == "Ananya Rao"
    assert search_student(103) == []
    assert len(student.students) == 2


def test_remove_student_missing_record_returns_none(sample_students):
    assert remove_student(999) is None
    assert len(student.students) == 3


# --------------------------------------------------------------------------
# list_students
# --------------------------------------------------------------------------

def test_list_students_is_sorted_by_roll_no():
    add_student(103, "Ananya Rao", "Data Science")
    add_student(101, "Riya Sharma", "Data Science")
    add_student(102, "Kabir Mehta", "Business Analytics")
    assert [rec["roll_no"] for rec in list_students()] == [101, 102, 103]


# --------------------------------------------------------------------------
# export_students (bonus)
# --------------------------------------------------------------------------

def test_export_students_to_csv(tmp_path, sample_students):
    target = tmp_path / "students.csv"
    count = export_students(target, "csv")
    assert count == 3

    lines = target.read_text(encoding="utf-8").strip().splitlines()
    assert lines[0].strip() == "roll_no,name,course,marks"
    assert len(lines) == 4  # header + 3 records


def test_export_students_to_json(tmp_path, sample_students):
    target = tmp_path / "students.json"
    count = export_students(target, "json")
    assert count == 3

    data = json.loads(target.read_text(encoding="utf-8"))
    assert [rec["roll_no"] for rec in data] == [101, 102, 103]


def test_export_students_unsupported_format_raises(tmp_path, sample_students):
    with pytest.raises(ValueError, match="Unsupported export format"):
        export_students(tmp_path / "students.xml", "xml")
