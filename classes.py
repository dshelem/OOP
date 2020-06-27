class Speedometer:
    def __init__(self, max_speed, units):
        super().__init__()
        print("__init__")
        self.max_speed = max_speed
        self.units = units

    def __new__(cls, max_speed, units):
        print("__new__")
        if max_speed > 250:
            return None
        return super().__new__(cls)

    def __del__(self):
        print("__del__")

    def __call__(self, new_param="default"):
        print(
            f"Now I behave as a function "
            f"I got {new_param} as an argument"
        )

    def __repr__(self):
        return f"Speedometer({self.max_speed}, '{self.units}')"

    def __str__(self):
        return f"Speedometer: max_speed = {self.max_speed}, units = {self.units}"

# s1 = Speedometer(200, "km")
# print(s1.max_speed)
# s2 = Speedometer(350, "miles")
# print(s2 is None)
# s1()
# s1(42)
# print(str(s1))
# print(repr(s1))


# class C:
#     def __init__(self, value):
#         self._value = value
#
#     @property
#     def value(self):
#         print("getter")
#         return self._value
#
#     @value.setter
#     def value(self, value):
#         print("setter")
#         self._value = value
#
#     @value.deleter
#     def value(self):
#         print("deleter")
#         del self._value
#
#
# c = C("Hello World!")
# print(c.value)
# c.value = "Goodbye World"
# del c.value
# print(c.value)


class Slotter:
    __slots__ = ['a', 'b']

    def get_values(self):
        return (self.a, self.b,)


s = Slotter()
s.a = 123
s.b = 'qwe'

print(s.a)

print(s.b)

s.c = 42

s.get_values()
