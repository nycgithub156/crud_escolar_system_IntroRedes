import os

from .models import *

DATA_DIR = "archives"
STUDENTS_FILE = os.path.join(DATA_DIR, "students.txt")
SUBJECTS_FILE = os.path.join(DATA_DIR, "subjects.txt")
CLASSES_FILE = os.path.join(DATA_DIR, "classes.txt")

def load_students():
    students = []
    with open(STUDENTS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue

            parts = line.split(";")
            id = int(parts[0])
            name = parts[1]
            email = parts[2]
            class_ids = split_ids(parts[3]) if len(parts) > 3 else []

            students.append(Student(id, name, email, class_ids))
    return students


def save_students(students):
    with open(STUDENTS_FILE, "w", encoding="utf-8") as f:
        for s in students:
            f.write(f"{s.id};{s.name};{s.email};{join_ids(s.class_ids)}\n")


def load_subjects():
    subjects = []
    with open(SUBJECTS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue

            parts = line.split(";")
            id = int(parts[0])
            name = parts[1]
            workload = int(parts[2])
            class_ids = split_ids(parts[3]) if len(parts) > 3 else []

            subjects.append(Subject(id, name, workload, class_ids))
    return subjects


def save_subjects(subjects):
    with open(SUBJECTS_FILE, "w", encoding="utf-8") as f:
        for s in subjects:
            f.write(f"{s.id};{s.name};{s.workload};{join_ids(s.class_ids)}\n")


def load_classes():
    classes = []
    with open(CLASSES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue

            parts = line.split(";")
            id = int(parts[0])
            name = parts[1]
            subject_ids = split_ids(parts[2]) if len(parts) > 2 else []
            student_ids = split_ids(parts[3]) if len(parts) > 3 else []

            classes.append(SchoolClass(id, name, subject_ids, student_ids))
    return classes


def save_classes(classes):
    with open(CLASSES_FILE, "w", encoding="utf-8") as f:
        for c in classes:
            f.write(f"{c.id};{c.name};{join_ids(c.subject_ids)};{join_ids(c.student_ids)}\n")



def ensure_files():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(STUDENTS_FILE):
        open(STUDENTS_FILE, "w", encoding="utf-8").close()

    if not os.path.exists(SUBJECTS_FILE):
        open(SUBJECTS_FILE, "w", encoding="utf-8").close()

    if not os.path.exists(CLASSES_FILE):
        open(CLASSES_FILE, "w", encoding="utf-8").close()


def split_ids(text):
    if text.strip() == "":
        return []
    return [int(x) for x in text.split(",") if x != ""]


def join_ids(ids_list):
    return ",".join(str(x) for x in ids_list)


def next_id(items):
    if not items:
        return 1
    return max(item.id for item in items) + 1