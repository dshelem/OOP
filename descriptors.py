"""
Descriptors can be used as class attributes.

They serve two purposes:
1. Allow to control data type of attributes
2. Lazy loading of data https://realpython.com/python-import/#reloading-modules

© Denis Shelemekh, 2020

"""

from typing import Any


def typedproperty(name: str, expected_type: Any) -> Any:
    """
    Creates property setter and getter allowing for data type control.

    Args:
        name: String - name of the property.
        expected_type: Any - expected type of the property.
    Raises:
        TypeError: When value supplied to setter doesn't match expected type.

    Usage:

    import typedproperty as tp

    class Stock:

        name = tp.String('name')
        shares = tp.Integer('shares')
        price = tp.Float('price')

        def __init__(self, name: str, shares: int, price: float) -> None:
            self.name = name
            self.shares = shares
            self.price = price

        ...
    """

    private_name = '_' + name

    @property
    def prop(self) -> Any:
        return getattr(self, private_name)

    @prop.setter
    def prop(self, value: Any) -> None:
        if not isinstance(value, expected_type):
            raise TypeError(f"Expected {expected_type}")
        setattr(self, private_name, value)

    return prop


# Shortcuts
String = lambda name: typedproperty(name, str)
Integer = lambda name: typedproperty(name, int)
Float = lambda name: typedproperty(name, float)

# Some other examples of descriptors


class IntegerType:
    """Class for checking if int type attributes are int."""

    def __init__(self, name):
        self._name = name

    def __set__(self, instance, value):
        """ SETTER """
        if not isinstance(value, int):
            raise TypeError(f"{value} is not an int")
        else:
            instance.__dict__[self._name] = value

    def __get__(self, instance, owner):
        """ GETTER """
        return instance.__dict__[self._name]


class StringType:
    """Class for checking if str type attributes are str."""

    def __init__(self, name):
        self._name = name

    def __set__(self, instance, value):
        """ SETTER """
        if not isinstance(value, str):
            raise TypeError(f"{value} is not a str")
        else:
            instance.__dict__[self._name] = value

    def __get__(self, instance, owner):
        """ GETTER """
        return instance.__dict__[self._name]


class Car:
    """
    Sample class for demonstration of descriptors.
    """
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
