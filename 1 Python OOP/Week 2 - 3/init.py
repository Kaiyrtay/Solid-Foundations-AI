from abc import ABC, abstractmethod


class Vehicle(ABC):

    def __init__(self, mileage):
        if not isinstance(mileage, (int, float)) or isinstance(mileage, bool):
            raise ValueError("Mileage must be a number")
        if mileage < 0:
            raise ValueError("Mileage cannot be negative")
        self.__mileage = mileage

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    def get_mileage(self):
        return self.__mileage


class Car(Vehicle):

    def start(self):
        print("Car started")

    def stop(self):
        print("Car stopped")


class Motorcycle(Vehicle):

    def start(self):
        print("Motorcycle started")

    def stop(self):
        print("Motorcycle stopped")


class Truck(Vehicle):

    def start(self):
        print("Truck started")

    def stop(self):
        print("Truck stopped")


def check(label, condition):
    print(("✅" if condition else "❌"), label)


def expect_error(label, exc, fn):
    try:
        fn()
        print("❌", label, "(no error)")
    except exc:
        print("✅", label)


print("\n=== 1. Abstract Enforcement ===")

expect_error("Vehicle cannot be instantiated",
             TypeError,
             lambda: Vehicle(1000))

print("\n=== 2. Object Creation ===")

car = Car(15000)
bike = Motorcycle(8000)
truck = Truck(120000)

check("Car created", isinstance(car, Vehicle))
check("Motorcycle created", isinstance(bike, Vehicle))
check("Truck created", isinstance(truck, Vehicle))

print("\n=== 3. Polymorphism Test ===")

for v in [car, bike, truck]:
    v.start()
    print("Mileage:", v.get_mileage())
    v.stop()


print("\n=== 4. Validation ===")

expect_error("Negative mileage rejected",
             ValueError,
             lambda: Car(-10))

expect_error("Non-numeric mileage rejected",
             ValueError,
             lambda: Car("fast"))

expect_error("Bool mileage rejected",
             ValueError,
             lambda: Car(True))


class Printable:

    def __str__(self):
        return f"Printable object with id {id(self)}"


class Serializable:

    def __str__(self):
        return f"Serializable object with id {id(self)}"


class Report(Printable, Serializable):

    def __str__(self):
        return f"Report object with id {id(self)}"


print("\n=== 5. Multiple Inheritance Test ===")
report = Report()
print(report)

print("\n=== 6. Multiple Inheritance Checks ===")

check("Report is Printable", isinstance(report, Printable))
check("Report is Serializable", isinstance(report, Serializable))
check("Report overrides parent __str__", "Report object" in str(report))

print("Report MRO:", " → ".join(cls.__name__ for cls in Report.__mro__))


class ReportNoOverride(Printable, Serializable):
    pass


r2 = ReportNoOverride()
print("ReportNoOverride output:", r2)
check("Printable wins in MRO", "Printable object" in str(r2))


class ReportReversed(Serializable, Printable):
    pass


r3 = ReportReversed()
print("ReportReversed output:", r3)
check("Serializable wins when order reversed",
      "Serializable object" in str(r3))
