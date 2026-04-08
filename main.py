from src.models import *
from src.persistence import *
from src.crud import *

def main():
    create_student("Nycollas", "nyc@email.com")
    students = list_students()

    for s in students:
        print(s.id, s.name, s.email)

if __name__ == "__main__":
    main()