"""
Some useful library functions.

© Denis Shelemekh, 2020

"""
import csv
from typing import List, Iterable, Union, Any
import logging


log = logging.getLogger(__name__)


def parse_csv(lines: Iterable[str],
              select: List[str] = None,
              types: List[Any] = None,
              has_headers: bool = True,
              delimiter: str = ',',
              silence_errors: bool = False) -> List[Union[dict, tuple]]:
    """
    Parses a CSV iterable into a list of records with optional conversion.

    Args:
        lines: Iterable to process records from.
        select: List of names of headers (string) to select from the data.
        types: List of functions (objects) to convert input values to.
        has_headers: Boolean - signals if file has headers as the first line.
        delimiter: String delimiter that is passed to csv.reader().
        silence_errors: Boolean - set to True to ignore errors reporting.
    Returns:
        A list containing either dictionaries (if dataset has headers) or tuples (otherwise).
        Examples: [{'name': 'MSFT', 'price': 99.34}, {'name': 'AAPL', 'price': 16.46}, ...]
        or [('AAPL', 946, 16.46), ('MSFT', 100, 99.34), ...]
    Raises:
        RuntimeError: When select is provided without headers.
        ValueError: When string passed as lines argument instead of iterable.
    """

    if not has_headers and select:
        raise RuntimeError("select must be used when headers are present")
    if isinstance(lines, str):
        raise ValueError("string passed as lines argument instead of iterable")

    rows = csv.reader(lines, delimiter=delimiter)
    headers = next(rows) if has_headers else []

    # Get indexes of fields to select from the rows
    # And narrow down set of headers
    if has_headers and select:
        indices = [headers.index(colname) for colname in select]
        headers = select
    else:
        indices = []

    records = []
    for row_num, row in enumerate(rows, 1):
        if not row:
            continue
        if indices:
            row = [row[index] for index in indices]
        if types:
            try:
                row = [func(val) for func, val in zip(types, row)]
            except ValueError as exception:
                if not silence_errors:
                    log.warning("Row %d: Couldn't convert %d", row_num, row)
                    log.debug("Row %d: Reason %s", row_num, str(exception))
                continue
        if has_headers:
            record = dict(zip(headers, row))
        else:
            record = tuple(row)
        records.append(record)

    return records
