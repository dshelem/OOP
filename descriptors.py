class IntegerType:
    """Class for checking if int type attributes are int."""

    def __init__(self, name):
        self.name = name

    def __set__(self, instance, value):
        """ SETTER """
        if not isinstance(value, int):
            raise TypeError(f"{value} is not an int")
        else:
            instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        """ GETTER """
        return instance.__dict__[self.name]


class StringType:
    """Class for checking if str type attributes are str."""

    def __init__(self, name):
        self.name = name

    def __set__(self, instance, value):
        """ SETTER """
        if not isinstance(value, str):
            raise TypeError(f"{value} is not a str")
        else:
            instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        """ GETTER """
        return instance.__dict__[self.name]


class Car:
    manufacturer = StringType("manufacturer")
    model = StringType("model")
    year = IntegerType("year")

    def __init__(self, manufacturer, model, year):
        self.manufacturer = manufacturer
        self.model = model
        self.year = year

    def __str__(self):
        return f"Manufacturer: {self.manufacturer}, model: {self.model}, " \
               f"year: {self.year}"


car = Car("Ford", "Mustang", 1964)
print(car)
car.manufacturer = 3.14
car.year = "Toyota"
