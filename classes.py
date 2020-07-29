"""
Collection of classes:
 - magic methods implementation
 - class with slots
 - abstract class with descendants
 - factory function producing objects of various classes depending on context

 © Denis Shelemekh, 2020

"""

from typing import List, Union, Tuple


class Speedometer:
    """
    Sample class demonstrating implementation of some of the "magic" methods.
    """
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


class Slotter:
    """
    Sample class demonstrating slots property.
    """
    __slots__ = ['a', 'b']

    def get_values(self) -> Tuple:
        """
        Returns object attributes.

        Returns:
            class attributes as tuple.
        """
        return self.a, self.b


class TableFormatter:
    """
    Abstract base class for table formatters.
    """

    def headings(self, headers: Union[List[str], Tuple[str]]) -> None:
        """
        Emit the table headings.
        """
        raise NotImplementedError()

    def row(self, row_data: Union[List[str], Tuple[str]]) -> None:
        """
        Emit a single row of table data.
        """
        raise NotImplementedError()


class TextTableFormatter(TableFormatter):
    """
    Print a table in plain-text format.
    """
    def headings(self, headers: Union[List[str], Tuple[str]]) -> None:
        """
        Output headers.

        Args:
             headers: List or tuple of str headers.
        """
        for header in headers:
            print(f"{header:>10s}", end=" ")
        print()
        print(("-" * 10 + " ") * len(headers))

    def row(self, row_data: Union[List[str], Tuple[str]]) -> None:
        """
        Output row.

        Args:
             row_data: List or tuple of str fields.
        """
        for field in row_data:
            print(f"{field:>10s}", end=" ")
        print()


class CSVTableFormatter(TableFormatter):
    """
    Output portfolio data in CSV format.
    """
    def headings(self, headers: Union[List[str], Tuple[str]]) -> None:
        """
        Output headers.

        Args:
             headers: List or tuple of str headers.
        """
        print(",".join(headers))

    def row(self, row_data: Union[List[str], Tuple[str]]) -> None:
        """
        Output row.

        Args:
             row_data: List or tuple of str fields.
        """
        print(",".join(row_data))


class HTMLTableFormatter(TableFormatter):
    """
    Output portfolio data in HTML format.
    """
    def headings(self, headers: Union[List[str], Tuple[str]]) -> None:
        """
        Output headers.

        Args:
             headers: List or tuple of str headers.
        """
        print("<tr>", end="")
        for header in headers:
            print(f"<th>{header}</th>", end="")
        print("</tr>")

    def row(self, row_data: Union[List[str], Tuple[str]]) -> None:
        """
        Output row.

        Args:
             row_data: List or tuple of str fields.
        """
        print("<tr>", end="")
        for field in row_data:
            print(f"<td>{field}</td>", end="")
        print("</tr>")


def create_formatter(fmt: str) -> TableFormatter:
    """
    Factory returning table formatter based on the input format.

    Args:
         fmt: Str - abbreviation of desired format.
         One of the following: txt/csv/html.
    Returns:
        instance of TableFormatter descendants.
    Raises:
        ValueError: If fmt argument is not one of predefined.
    """

    if fmt == "txt":
        formatter = TextTableFormatter()
    elif fmt == "csv":
        formatter = CSVTableFormatter()
    elif fmt == "html":
        formatter = HTMLTableFormatter()
    else:
        raise RuntimeError(f"Unknown table format {fmt}")

    return formatter
