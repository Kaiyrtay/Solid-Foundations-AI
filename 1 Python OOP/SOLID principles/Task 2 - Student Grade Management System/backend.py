from abc import ABC, abstractmethod
import json
from decorators import str_not_empty_validation

DEFAULT_PASSING_SCORE = 60


class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        self.__grades = []

    @property
    def name(self):
        return self.__name

    @name.setter
    @str_not_empty_validation(attr_name="Name")
    def name(self, value):
        self.__name = value

    @property
    def student_id(self):
        return self.__student_id

    @student_id.setter
    @str_not_empty_validation(attr_name="Student ID")
    def student_id(self, value):
        self.__student_id = value

    @property
    def grades(self):
        return self.__grades

    @grades.setter
    def grades(self, value):
        if not isinstance(value, list):
            raise TypeError("Grades must be a list")
        for grade in value:
            if not isinstance(grade, Grade):
                raise TypeError("Each grade must be a Grade object")
        self.__grades = value

    def add_grade(self, grade):
        if not isinstance(grade, Grade):
            raise TypeError("Grade must be a Grade object")
        self.__grades.append(grade)

    def __str__(self):
        return f"Student {self.__name} (ID: {self.__student_id}) with {len(self.__grades)} grades"

    def __repr__(self):
        return f"Student(name={self.__name}, student_id={self.__student_id}, grades={self.__grades})"


class Grade:

    def __init__(self, subject, score):
        self.subject = subject
        self.score = score

    @property
    def subject(self):
        return self.__subject

    @subject.setter
    @str_not_empty_validation(attr_name="Subject")
    def subject(self, value):
        self.__subject = value

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Score must be a number")
        if value < 0 or value > 100:
            raise ValueError("Score must be between 0 and 100")
        self.__score = value

    def __str__(self):
        return f"{self.__subject}: {self.__score}"

    def __repr__(self):
        return f"Grade(subject={self.__subject}, score={self.__score})"


class GradeCalculator:

    def calculate_average(self, student):
        if not isinstance(student, Student):
            raise TypeError("Input must be a Student object")
        if not student.grades:
            return 0
        total_score = sum(grade.score for grade in student.grades)
        return total_score / len(student.grades)


class PassFailEvaluator:
    def __init__(self, calculator: GradeCalculator):
        if not isinstance(calculator, GradeCalculator):
            raise TypeError(
                "Calculator must be an instance of GradeCalculator")
        self.calculator = calculator

    def is_passing(self, student, passing_score=DEFAULT_PASSING_SCORE):
        if not isinstance(student, Student):
            raise TypeError("Input must be a Student object")
        average_score = self.calculator.calculate_average(student)
        return average_score >= passing_score


class Export(ABC):
    @abstractmethod
    def export(self, student):
        pass


class ReportGenerator:

    def __init__(self, calculator: GradeCalculator, evaluator: PassFailEvaluator):
        self.__calculator = calculator
        self.__evaluator = evaluator

    def generate_report(self, student):
        if not isinstance(student, Student):
            raise TypeError("Input must be a Student object")

        report = [
            f"Student Report",
            f"=======================",
            f"Name       : {student.name}",
            f"Student ID : {student.student_id}",
            f"Number of subjects: {len(student.grades)}",
            "",
            "Grades:"
        ]

        for grade in student.grades:
            remark = "Pass" if grade.score >= DEFAULT_PASSING_SCORE else "Fail"
            report.append(f"  - {grade.subject}: {grade.score} ({remark})")

        average_score = self.__calculator.calculate_average(student)
        overall_status = "Passing" if self.__evaluator.is_passing(
            student) else "Failing"

        report += [
            "",
            f"Average Score : {average_score:.2f}",
            f"Overall Status: {overall_status}",
            "======================="
        ]

        return "\n".join(report)


class TXTExport(Export):
    def __init__(self, report_generator: ReportGenerator):
        if not isinstance(report_generator, ReportGenerator):
            raise TypeError(
                "Report generator must be an instance of ReportGenerator")
        self.report_generator = report_generator

    def export(self, student):
        if not isinstance(student, Student):
            raise TypeError("Input must be a Student object")
        filename = f"{student.student_id}_report.txt"
        with open(filename, 'w') as file:
            file.write(self.report_generator.generate_report(student))
        return f"Report exported to {filename}"


class JSONExport(Export):

    def export(self, student):
        if not isinstance(student, Student):
            raise TypeError("Input must be a Student object")
        data = {
            "name": student.name,
            "student_id": student.student_id,
            "grades": [{"subject": grade.subject, "score": grade.score} for grade in student.grades]
        }
        filename = f"{student.student_id}_report.json"
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

        return f"Report exported to {filename}"


class NotificationService(ABC):

    @abstractmethod
    def send_notification(self, message: str):
        pass


class EmailNotificationService(NotificationService):

    def send_notification(self, message: str):
        return f"Sending email notification: {message}"


class SMSNotificationService(NotificationService):

    def send_notification(self, message: str):
        return f"Sending SMS notification: {message}"
