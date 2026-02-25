from classes import Student, Course, University
import random
import json
import os

FIRST_NAMES = ["Alice", "Bob", "Cara", "David", "Eva", "Frank", "Grace", "Henry",
               "Isla", "Jack", "Karen", "Leo", "Mia", "Noah", "Olivia", "Peter"]
LAST_NAMES = ["Smith", "Johnson", "Brown", "Taylor", "Anderson",
              "Lee", "Walker", "Harris", "Clark", "Lewis"]

COURSE_NAMES = ["Mathematics", "Physics", "Computer Science", "Biology",
                "Chemistry", "History", "Literature", "Economics",
                "Philosophy", "Engineering", "Psychology", "Statistics"]

UNIVERSITY_PREFIXES = ["North", "South", "East", "West", "Central", "Royal",
                       "Grand", "New", "Old", "Upper", "Lower", "Great"]
UNIVERSITY_SUFFIXES = ["University", "College", "Institute", "Academy",
                       "School of Sciences", "Polytechnic"]
UNIVERSITY_LOCATIONS = ["London", "Oxford", "Berlin", "Paris", "Boston",
                        "Toronto", "Sydney", "Tokyo", "Dubai", "Athens"]


########################### Generators ##########################

def generate_random_student() -> Student:
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    age = random.randint(16, 100)
    grades = [random.uniform(0, 100) for _ in range(random.randint(3, 9))]
    return Student(name=name, age=age, grades=grades)


def generate_random_course() -> Course:
    course = Course(random.choice(COURSE_NAMES))
    for _ in range(5):
        course.add_student(generate_random_student())
    return course


def generate_random_university() -> University:
    name = f"{random.choice(UNIVERSITY_PREFIXES)} {random.choice(UNIVERSITY_LOCATIONS)} {random.choice(UNIVERSITY_SUFFIXES)}"
    courses = [generate_random_course() for _ in range(4)]
    return University(name, courses)


########################### File I/O ##########################

def save_report(universities: list, filename: str = "university_report.txt"):
    with open(filename, "w") as f:
        for university in universities:
            f.write("=" * 60 + "\n")
            f.write(f"  {university}\n")
            f.write("=" * 60 + "\n")
            for course in university.get_all_courses():
                f.write(f"\n  {course}\n")
                f.write("-" * 60 + "\n")
                for student in course.students:
                    f.write(f"    {student}\n")
            f.write(
                f"\n  Total Unique Students : {len(university.get_all_students())}\n")
            f.write(
                f"  Top Student           : {university.get_top_student()}\n")
            f.write(f"  Top 3 Students        :\n")
            for i, student in enumerate(university.get_top_students(3), start=1):
                f.write(f"    {i}. {student}\n")
            f.write("\n")
    print(f"\n  Report saved to '{filename}'")


def save_json(universities: list, filename: str = "university_data.json"):
    data = []
    for university in universities:
        uni_data = {
            "university": university.name,
            "courses": [
                {
                    "course": course.name,
                    "class_average": round(course.class_average, 2),
                    "students": [
                        {
                            "name": student.name,
                            "age": student.age,
                            "grades": student.grades,
                            "average": round(student.average, 2)
                        }
                        for student in course.students
                    ]
                }
                for course in university.get_all_courses()
            ]
        }
        data.append(uni_data)

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"  Data saved to '{filename}'")


def load_json(filename: str = "university_data.json") -> list:
    if not os.path.exists(filename):
        print(f"  No saved data found at '{filename}'")
        return []

    with open(filename, "r") as f:
        data = json.load(f)

    universities = []
    for uni_data in data:
        courses = []
        for course_data in uni_data["courses"]:
            course = Course(course_data["course"])
            for student_data in course_data["students"]:
                student = Student(
                    name=student_data["name"],
                    age=student_data["age"],
                    grades=student_data["grades"]
                )
                course.add_student(student)
            courses.append(course)
        universities.append(University(uni_data["university"], courses))

    print(f"  Loaded {len(universities)} universities from '{filename}'\n")
    return universities


########################### Display ##########################

def print_separator(char="=", length=60):
    print(char * length)


def display_universities(universities: list):
    for university in universities:
        print_separator()
        print(f"  {university}")
        print_separator()

        for course in university.get_all_courses():
            print(f"\n  {course}")
            print_separator("-", 60)
            for student in course.students:
                print(f"    {student}")

        print(
            f"\n  Total Unique Students : {len(university.get_all_students())}")
        print(f"  Top Student           : {university.get_top_student()}")
        print(f"  Top 3 Students        :")
        for i, student in enumerate(university.get_top_students(3), start=1):
            print(f"    {i}. {student}")

        print()


########################### Main ##########################

def main():
    # Generate
    universities = [generate_random_university() for _ in range(3)]

    # Display
    display_universities(universities)

    # Save plain text report
    save_report(universities, "university_report.txt")

    # Save structured JSON
    save_json(universities, "university_data.json")

    # Reload from JSON and verify
    print("\n  --- Reloading from JSON to verify ---\n")
    loaded_universities = load_json("university_data.json")
    display_universities(loaded_universities)


if __name__ == "__main__":
    main()
