from base import Person
from abc import abstractmethod

DEFAULT_TEACHER_SALARY = 50000
DEFAULT_ADMINISTRATOR_SALARY = 60000
DEFAULT_SECURITY_SALARY = 40000
DEFAULT_GRADUATE_TUITION = 2000


class Staff(Person):

    ############################### Overwriting abstract methods ###########################

    def get_role(self):
        return "Staff"

    @abstractmethod
    def get_salary(self):
        pass


class Teacher(Staff):

    ############################### Overwriting abstract methods ###########################

    def get_role(self):
        return "Teacher"

    def get_salary(self):
        return DEFAULT_TEACHER_SALARY


class Administrator(Staff):

    ############################### Overwriting abstract methods ###########################

    def get_role(self):
        return "Administrator"

    def get_salary(self):
        return DEFAULT_ADMINISTRATOR_SALARY


class Security(Staff):
    ############################### Overwriting abstract methods ###########################

    def get_role(self):
        return "Security"

    def get_salary(self):
        return DEFAULT_SECURITY_SALARY


class Student(Person):

    # Only need to override __init__ if:
    # add new attributes
    # change validation
    # extend behavior
    # def __init__(self, name, age, ID):
    #     super().__init__(name, age, ID)

    ############################### Overwriting abstract methods ###########################

    def get_role(self):
        return "Student"

    @abstractmethod
    def calculate_tuition(self):
        pass


class UndergraduateStudent(Student):

    ########################### Initialization with Validation #############################

    def __init__(self, name, age, ID, credits, per_credit_fee):
        if not isinstance(credits, int):
            raise TypeError("Credits must be an integer.")
        if credits < 0:
            raise ValueError("Credits must be a non-negative integer.")
        if not isinstance(per_credit_fee, (int, float)):
            raise TypeError("Per credit fee must be a number.")
        if per_credit_fee < 0:
            raise ValueError("Per credit fee must be a non-negative number.")
        super().__init__(name, age, ID)
        self.__credits = credits
        self.__per_credit_fee = per_credit_fee

    ########################## Getters and Setters with Validation #########################
    @property
    def credits(self):
        return self.__credits

    @credits.setter
    def credits(self, value):
        if not isinstance(value, int):
            raise TypeError("Credits must be an integer.")
        if value < 0:
            raise ValueError("Credits must be a non-negative integer.")
        self.__credits = value

    @property
    def per_credit_fee(self):
        return self.__per_credit_fee

    @per_credit_fee.setter
    def per_credit_fee(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Per credit fee must be a number.")
        if value < 0:
            raise ValueError("Per credit fee must be a non-negative number.")
        self.__per_credit_fee = value

    ################################### Overwriting abstract methods ###########################

    def calculate_tuition(self):
        return self.__credits * self.__per_credit_fee

    ################################### String representation ###########################

    def __str__(self):
        return f"UndergraduateStudent(name={self.name}, age={self.age}, ID={self.ID}, credits={self.__credits}, per_credit_fee={self.__per_credit_fee})"

    def __repr__(self):
        return self.__str__()


class GraduateStudent(Student):

    ########################### Initialization with Validation #############################

    def __init__(self, name, age, ID, thesis_title, advisor):
        if not isinstance(thesis_title, str):
            raise TypeError("Thesis title must be a string.")
        if not thesis_title.strip():
            raise ValueError("Thesis title must be a non-empty string.")
        if not isinstance(advisor, Teacher):
            raise TypeError("Advisor must be a Teacher instance.")
        super().__init__(name, age, ID)
        self.__thesis_title = thesis_title
        self.__advisor = advisor

    ########################## Getters and Setters with Validation #########################

    @property
    def thesis_title(self):
        return self.__thesis_title

    @thesis_title.setter
    def thesis_title(self, value):
        if not isinstance(value, str):
            raise TypeError("Thesis title must be a string.")
        if not value.strip():
            raise ValueError("Thesis title must be a non-empty string.")
        self.__thesis_title = value

    @property
    def advisor(self):
        return self.__advisor

    @advisor.setter
    def advisor(self, value):
        if not isinstance(value, Teacher):
            raise TypeError("Advisor must be a Teacher instance.")
        self.__advisor = value

    ################################### Methods ################################################
    def calculate_tuition(self):
        return DEFAULT_GRADUATE_TUITION

    ################################### String representation ##################################
    def __str__(self):
        return f"GraduateStudent(name={self.name}, age={self.age}, ID={self.ID}, thesis_title={self.__thesis_title}, advisor={self.__advisor.name})"

    def __repr__(self):
        return self.__str__()
