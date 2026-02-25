class Student:

    ########################### Initialization with Validation ##########################

    def __init__(self, name: str, age: int, grades: list[int | float] = None):
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if not name.strip():
            raise ValueError("Name must be a non-empty string.")

        if not isinstance(age, int) or isinstance(age, bool):
            raise TypeError("Age must be an integer.")

        if age < 16 or age > 100:
            raise ValueError("Age must be between 16 and 100.")

        if isinstance(grades, list):
            for grade in grades:
                if not isinstance(grade, (int, float)):
                    raise TypeError("All grades must be numbers.")
                if grade < 0 or grade > 100:
                    raise ValueError("All grades must be between 0 and 100.")

        self.__name = name
        self.__age = age
        self.__grades = list(grades) if grades is not None else []

    ########################## Getters and Setters with Validation ##########################

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        if not value.strip():
            raise ValueError("Name must be a non-empty string.")
        self.__name = value

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError("Age must be an integer.")
        if value < 16 or value > 100:
            raise ValueError("Age must be between 16 and 100.")
        self.__age = value

    @property
    def grades(self):
        return list(self.__grades)

    @grades.setter
    def grades(self, value):
        if not isinstance(value, list):
            raise TypeError("Grades must be a list.")
        for grade in value:
            if not isinstance(grade, (int, float)):
                raise TypeError("All grades must be numbers.")
            if grade < 0 or grade > 100:
                raise ValueError("All grades must be between 0 and 100.")

        self.__grades = list(value)

    ########################## Methods ##########################

    def add_grade(self, grade: int | float):
        if not isinstance(grade, (int, float)):
            raise TypeError("Grade must be a number.")
        if grade < 0 or grade > 100:
            raise ValueError("Grade must be between 0 and 100.")
        self.__grades.append(grade)

    @property
    def average(self):
        if not self.__grades:
            return 0
        return sum(self.__grades) / len(self.__grades)

    @property
    def info(self):
        return f"Name: {self.__name}, Age: {self.__age}, Average Grade: {self.average:.2f}"

    ############################# String Representations ##########################

    def __str__(self):
        return self.info

    def __repr__(self):
        return f"Student(name={self.__name!r}, age={self.__age!r}, grades={self.__grades!r})"


class Course:

    ############################ Initialization with Validation ##########################

    def __init__(self, name: str):
        if not isinstance(name, str):
            raise TypeError("Course name must be a string.")
        if not name.strip():
            raise ValueError("Course name must be a non-empty string.")
        self.__name = name
        self.__students = []

    ############################### Getters and Setters with Validation ##########################
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Course name must be a string.")
        if not value.strip():
            raise ValueError("Course name must be a non-empty string.")
        self.__name = value

    @property
    def students(self):
        return list(self.__students)

    @students.setter
    def students(self, value):
        if not isinstance(value, list):
            raise TypeError("Students must be a list.")
        for student in value:
            if not isinstance(student, Student):
                raise TypeError(
                    "All items in students list must be Student instances.")
        self.__students = list(value)

    ########################### Methods ##########################

    def add_student(self, student: Student):
        if not isinstance(student, Student):
            raise TypeError(
                "Only Student instances can be added to the course.")
        self.__students.append(student)

    def remove_student(self, student: Student):
        if not isinstance(student, Student):
            raise TypeError(
                "Only Student instances can be removed from the course.")
        if student in self.__students:
            self.__students.remove(student)
        else:
            raise ValueError("Student not found in the course.")

    @property
    def class_average(self):
        if not self.__students:
            return 0
        total_average = sum(student.average for student in self.__students)
        return total_average / len(self.__students)

    ############################# String Representations ##########################

    def __str__(self):
        return f"Course: {self.__name}, Students Enrolled: {len(self.__students)}, Class Average: {self.class_average:.2f}"

    def __repr__(self):
        return f"Course(name={self.__name!r}, students={self.__students!r})"


class University:

    ############################# Initialization with Validation ##########################

    def __init__(self, name: str, courses: list[Course] = None):
        if not isinstance(name, str):
            raise TypeError("University name must be a string.")
        if not name.strip():
            raise ValueError("University name must be a non-empty string.")
        if not isinstance(courses, list) and courses is not None:
            raise TypeError("Courses must be a list of Course instances.")
        if courses is not None:
            for course in courses:
                if not isinstance(course, Course):
                    raise TypeError(
                        "All items in courses list must be Course instances.")
        self.__name = name
        self.__courses = list(courses) if courses is not None else []

    ############################# Getters and Setters with Validation ##########################

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("University name must be a string.")
        if not value.strip():
            raise ValueError("University name must be a non-empty string.")
        self.__name = value

    @property
    def courses(self):
        return list(self.__courses)

    @courses.setter
    def courses(self, value):
        if not isinstance(value, list):
            raise TypeError("Courses must be a list of Course instances.")
        for course in value:
            if not isinstance(course, Course):
                raise TypeError(
                    "All items in courses list must be Course instances.")
        self.__courses = list(value)

    ############################# Methods ##########################
    def add_course(self, course: Course):
        if not isinstance(course, Course):
            raise TypeError(
                "Only Course instances can be added to the university.")
        self.__courses.append(course)

    def remove_course(self, course: Course):
        if not isinstance(course, Course):
            raise TypeError(
                "Only Course instances can be removed from the university.")
        if course in self.__courses:
            self.__courses.remove(course)
        else:
            raise ValueError("Course not found in the university.")

    def get_all_courses(self):
        return list(self.__courses)

    def get_all_students(self):
        unique_students = set()
        for course in self.__courses:
            unique_students.update(course.students)
        return list(unique_students)

    def get_top_student(self):
        all_students = self.get_all_students()
        if not all_students:
            return None
        top_student = max(all_students, key=lambda s: s.average)
        return top_student

    def get_top_students(self, n=1):
        all_students = self.get_all_students()
        if not all_students:
            return []
        sorted_students = sorted(
            all_students, key=lambda s: s.average, reverse=True)
        return sorted_students[:n]

    ############################# String Representations ##########################
    def __str__(self):
        return f"University: {self.__name}, Courses Offered: {len(self.__courses)}, Total Students: {len(self.get_all_students())}"

    def __repr__(self):
        return f"University(name={self.__name!r}, courses={self.__courses!r})"
