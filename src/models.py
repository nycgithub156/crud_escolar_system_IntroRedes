class Student:
    def __init__(self, id, name, email, class_ids=None):
        self.id = id
        self.name = name
        self.email = email
        self.class_ids = class_ids if class_ids is not None else []


class Subject:
    def __init__(self, id, name, workload, class_ids=None):
        self.id = id
        self.name = name
        self.workload = workload
        self.class_ids = class_ids if class_ids is not None else []


class SchoolClass:
    def __init__(self, id, name, subject_ids=None, student_ids=None):
        self.id = id
        self.name = name
        self.subject_ids = subject_ids if subject_ids is not None else []
        self.student_ids = student_ids if student_ids is not None else []