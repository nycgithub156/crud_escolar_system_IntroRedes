from .persistence import *

def create_student(name, email):
    ensure_files()
    students = load_students()
    new_student = Student(next_id(students), name, email)
    students.append(new_student)
    save_students(students)
    return new_student


def list_students():
    ensure_files()
    return load_students()


def get_student(student_id):
    students = load_students()
    for s in students:
        if s.id == student_id:
            return s
    return None


def update_student(student_id, name=None, email=None):
    students = load_students()
    found = False

    for s in students:
        if s.id == student_id:
            if name is not None:
                s.name = name
            if email is not None:
                s.email = email
            found = True
            break

    if found:
        save_students(students)

    return found


def delete_student(student_id):
    students = load_students()
    classes = load_classes()

    new_students = []
    found = False

    for s in students:
        if s.id == student_id:
            found = True
        else:
            new_students.append(s)

    if not found:
        return False

    for c in classes:
        if student_id in c.student_ids:
            c.student_ids.remove(student_id)

    save_students(new_students)
    save_classes(classes)
    return True


def create_subject(name, workload):
    ensure_files()
    subjects = load_subjects()
    new_subject = Subject(next_id(subjects), name, workload)
    subjects.append(new_subject)
    save_subjects(subjects)
    return new_subject


def list_subjects():
    ensure_files()
    return load_subjects()


def get_subject(subject_id):
    subjects = load_subjects()
    for s in subjects:
        if s.id == subject_id:
            return s
    return None


def update_subject(subject_id, name=None, workload=None):
    subjects = load_subjects()
    found = False

    for s in subjects:
        if s.id == subject_id:
            if name is not None:
                s.name = name
            if workload is not None:
                s.workload = workload
            found = True
            break

    if found:
        save_subjects(subjects)

    return found


def delete_subject(subject_id):
    subjects = load_subjects()
    classes = load_classes()

    new_subjects = []
    found = False

    for s in subjects:
        if s.id == subject_id:
            found = True
        else:
            new_subjects.append(s)

    if not found:
        return False

    for c in classes:
        if subject_id in c.subject_ids:
            c.subject_ids.remove(subject_id)

    save_subjects(new_subjects)
    save_classes(classes)
    return True


def create_class(name, subject_ids=None):
    ensure_files()

    if subject_ids is None:
        subject_ids = []

    if isinstance(subject_ids, int):
        subject_ids = [subject_ids]

    unique_subject_ids = []
    for sid in subject_ids:
        if sid not in unique_subject_ids:
            unique_subject_ids.append(sid)

    subjects = load_subjects()
    for sid in unique_subject_ids:
        subject_exists = False
        for s in subjects:
            if s.id == sid:
                subject_exists = True
                break
        if not subject_exists:
            return None

    classes = load_classes()
    new_class = SchoolClass(next_id(classes), name, unique_subject_ids)
    classes.append(new_class)
    save_classes(classes)

    for s in subjects:
        if s.id in unique_subject_ids:
            if new_class.id not in s.class_ids:
                s.class_ids.append(new_class.id)

    save_subjects(subjects)
    return new_class


def list_classes():
    ensure_files()
    return load_classes()


def get_class(class_id):
    classes = load_classes()
    for c in classes:
        if c.id == class_id:
            return c
    return None


def update_class(class_id, name=None, subject_ids=None):
    classes = load_classes()
    subjects = load_subjects()

    class_obj = None
    for c in classes:
        if c.id == class_id:
            class_obj = c
            break

    if class_obj is None:
        return False

    if name is not None:
        class_obj.name = name

    if subject_ids is not None:
        if isinstance(subject_ids, int):
            subject_ids = [subject_ids]

        unique_subject_ids = []
        for sid in subject_ids:
            if sid not in unique_subject_ids:
                unique_subject_ids.append(sid)

        for sid in unique_subject_ids:
            subject_exists = False
            for s in subjects:
                if s.id == sid:
                    subject_exists = True
                    break
            if not subject_exists:
                return False

        old_subject_ids = class_obj.subject_ids[:]

        for sid in old_subject_ids:
            if sid not in unique_subject_ids:
                for s in subjects:
                    if s.id == sid and class_id in s.class_ids:
                        s.class_ids.remove(class_id)

        for sid in unique_subject_ids:
            for s in subjects:
                if s.id == sid and class_id not in s.class_ids:
                    s.class_ids.append(class_id)

        class_obj.subject_ids = unique_subject_ids

    save_classes(classes)
    save_subjects(subjects)
    return True


def delete_class(class_id):
    classes = load_classes()
    students = load_students()
    subjects = load_subjects()

    class_obj = None
    new_classes = []

    for c in classes:
        if c.id == class_id:
            class_obj = c
        else:
            new_classes.append(c)

    if class_obj is None:
        return False

    for s in students:
        if class_id in s.class_ids:
            s.class_ids.remove(class_id)

    for sub in subjects:
        if class_id in sub.class_ids:
            sub.class_ids.remove(class_id)

    save_classes(new_classes)
    save_students(students)
    save_subjects(subjects)
    return True

def enroll_student(student_id, class_id):
    students = load_students()
    classes = load_classes()

    student = None
    school_class = None

    for s in students:
        if s.id == student_id:
            student = s
            break

    for c in classes:
        if c.id == class_id:
            school_class = c
            break

    if student is None or school_class is None:
        return False

    if class_id not in student.class_ids:
        student.class_ids.append(class_id)

    if student_id not in school_class.student_ids:
        school_class.student_ids.append(student_id)

    save_students(students)
    save_classes(classes)
    return True


def remove_student_from_class(student_id, class_id):
    students = load_students()
    classes = load_classes()

    student = None
    school_class = None

    for s in students:
        if s.id == student_id:
            student = s
            break

    for c in classes:
        if c.id == class_id:
            school_class = c
            break

    if student is None or school_class is None:
        return False

    if class_id in student.class_ids:
        student.class_ids.remove(class_id)

    if student_id in school_class.student_ids:
        school_class.student_ids.remove(student_id)

    save_students(students)
    save_classes(classes)
    return True
