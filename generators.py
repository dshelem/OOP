"""
Collection of generator functions.

© Denis Shelemekh, 2020

"""

import csv
import os
import time
from typing import Iterable, Any, List, Dict


def follow(filename: str) -> str:
    """
    Generator function used for implementation of Linux "tail -f" functionality, i.e.
    watching and parsing in real time stock quotes.

    Args:
        filename: File to watch and process records from.
    Returns:
        Strings from file as they appear.
    """
    with open(filename, 'rt') as file:
        file.seek(0, os.SEEK_END)
        while True:
            line = file.readline()
            if line == "":
                time.sleep(0.1)
            else:
                yield line


def select_columns(rows: Iterable[List[Any]], indices: List[int]) -> List[Any]:
    """
    Generator yielding records with fields selected with provided indices.

    Args:
        rows: Iterable - to process records from.
        indices: List of integers - indexes of fields to select from the data.
    Returns:
        A list containing selected fields.
    """
    for row in rows:
        yield [row[index] for index in indices]


def convert_types(rows: Iterable[List[Any]], types: Any) -> List[Any]:
    """
    Generator converting input data to values with supplied list of funcs.

    Args:
        rows: Iterable - to process records from.
        types: List of functions to convert the data.
    Returns:
        A list containing converted values.
    """
    for row in rows:
        yield [func(val) for func, val in zip(types, row)]


def make_dicts(rows: Iterable[List[Any]], headers: List[str]) -> Dict:
    """
    Generator forming dictionary from supplied values and their headers.

    Args:
        rows: Iterable - to process records from.
        headers: List of strings - headers for dictionary.
    Returns:
        A dictionary.
    """
    for row in rows:
        yield dict(zip(headers, row))


def parse_stock_data(lines: Iterable[Any]) -> Iterable[Any]:
    """
    Conveyor of generators reading and transforming the data feed.

    Args:
        lines: Iterable - data feed.
    Returns:
        Iterable - processed data.
    """
    rows = csv.reader(lines)
    rows = select_columns(rows, [0, 1, 4])
    rows = convert_types(rows, [str, float, float])
    rows = make_dicts(rows, ['name', 'price', 'change'])
    return rows


def filter_symbols(rows: Iterable[Any], names: portfolio.Portfolio) -> Iterable[Any]:
    """
    Generator function filtering only those rows from data feed that relate to supplied portfolio.

    Args:
        rows: Iterable - data feed.
        names: Portfolio of stocks.
    Returns:
        Record related to supplied portfolio.
    """
    for row in rows:
        if row['name'] in names:
            yield row


def ticker(portfolio_filename: str,
           feed_filename: str,
           fmt: str = "txt") -> None:
    """
    Orchestrator function realising data processing logic.

    Args:
        portfolio_filename: String - name of datafile with portfolio.
        feed_filename: String - name of file with data feed.
        fmt: String - format of the report (see tableformat module).
    """
    _portfolio = report.read_portfolio(portfolio_filename)
    feed = parse_stock_data(follow(feed_filename))
    # Generator expression
    rows = (row for row in feed if row['name'] in _portfolio)
    formatter = tableformat.create_formatter(fmt)
    formatter.headings(['Name', 'Price', 'Change'])
    for row in rows:  # Iterating generator
        row_data = [row['name'], str(row['price']), str(row['change'])]
        formatter.row(row_data)
