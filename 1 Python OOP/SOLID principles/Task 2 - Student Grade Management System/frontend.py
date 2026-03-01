# ====== FRONTEND: STUDENT MANAGEMENT CONSOLE UI ======

from backend import (
    Student,
    Grade,
    GradeCalculator,
    PassFailEvaluator,
    ReportGenerator,
    TXTExport,
    JSONExport,
    EmailNotificationService,
    SMSNotificationService,
)

# ====== Dependencies ======
calculator = GradeCalculator()
evaluator = PassFailEvaluator(calculator)
report_generator = ReportGenerator(calculator, evaluator)
notifier = EmailNotificationService()  # or SMSNotificationService()

# ====== Student registry ======


class StudentRegistry:
    def __init__(self):
        self._students = {}

    def add_student(self, student: Student):
        if student.student_id in self._students:
            raise ValueError(
                f"Student ID {student.student_id} already exists.")
        self._students[student.student_id] = student

    def get_student(self, student_id):
        return self._students.get(student_id)

    def get_all_students(self):
        return list(self._students.values())


registry = StudentRegistry()


# ====== Console UI Functions ======
def print_menu():
    print("\n=== Student Management System ===")
    print("1. Add Student")
    print("2. Add Grade to Student")
    print("3. Show Student Report")
    print("4. Export Report (TXT/JSON)")
    print("5. Exit")


def add_student():
    print("\n-- Add Student --")
    student_id = input("Student ID: ").strip()
    name = input("Name: ").strip()
    try:
        student = Student(name, student_id)
        registry.add_student(student)
        print(f"[SUCCESS] Student '{name}' added.")
    except Exception as e:
        print(f"[ERROR] {e}")


def add_grade():
    print("\n-- Add Grade --")
    student_id = input("Student ID: ").strip()
    student = registry.get_student(student_id)
    if not student:
        print(f"[ERROR] Student ID {student_id} not found.")
        return

    subject = input("Subject: ").strip()
    try:
        score = float(input("Score: ").strip())
        grade = Grade(subject, score)
        student.add_grade(grade)

        # Optional: notify if failing
        if score < 60:
            message = f"Student {student.name} failed {subject} with score {score}."
            print(notifier.send_notification(message))

        print(f"[SUCCESS] Grade {score} added for {subject}.")
    except Exception as e:
        print(f"[ERROR] {e}")


def show_report():
    print("\n-- Student Reports --")
    all_students = registry.get_all_students()
    if not all_students:
        print("[INFO] No students found.")
        return

    for student in all_students:
        print(report_generator.generate_report(student))


def export_report():
    print("\n-- Export Report --")
    student_id = input("Student ID: ").strip()
    student = registry.get_student(student_id)
    if not student:
        print(f"[ERROR] Student ID {student_id} not found.")
        return

    choice = input("Export as TXT or JSON? ").strip().lower()
    try:
        if choice == "txt":
            exporter = TXTExport(report_generator)
            print(exporter.export(student))
        elif choice == "json":
            exporter = JSONExport()
            print(exporter.export(student))
        else:
            print("[ERROR] Invalid export type. Choose TXT or JSON.")
    except Exception as e:
        print(f"[ERROR] {e}")


def main():
    print("Welcome to the Student Management System!")
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                add_student()
            elif choice == "2":
                add_grade()
            elif choice == "3":
                show_report()
            elif choice == "4":
                export_report()
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("[ERROR] Invalid option. Please choose 1-5.")
        except Exception as e:
            print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()
