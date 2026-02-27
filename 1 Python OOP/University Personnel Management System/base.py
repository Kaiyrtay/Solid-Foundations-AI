from abc import ABC, abstractmethod


class Person(ABC):

    ########################### Initialization with Validation ##########################

    def __init__(self, name, age, ID):
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if not name.strip():
            raise ValueError("Name must be a non-empty string.")
        if not isinstance(age, int) or isinstance(age, bool):
            raise TypeError("Age must be an integer.")
        if age < 16 or age > 100:
            raise ValueError("Age must be between 16 and 100.")
        if not isinstance(ID, int) or isinstance(ID, bool):
            raise TypeError("ID must be an integer.")
        if ID < 0:
            raise ValueError("ID must be a non-negative integer.")

        self.__name = name
        self.__age = age
        self.__ID = ID

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
    def ID(self):
        return self.__ID

    @ID.setter
    def ID(self, value):
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError("ID must be an integer.")
        if value < 0:
            raise ValueError("ID must be a non-negative integer.")
        self.__ID = value

    ############################ Abstract Method for Role ##########################

    @abstractmethod
    def get_role(self):
        pass

    @property
    def info(self):
        return f"{self.get_role()}: {self.name}, Age: {self.age}, ID: {self.ID}"

    ########################### String Representation ##########################

    def __str__(self):
        return f"{self.get_role()}: {self.name}, Age: {self.age}, ID: {self.ID}"

    def __repr__(self):
        return f"{self.get_role()}(name='{self.name}', age={self.age}, ID={self.ID})"
