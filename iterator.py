"""
Iterator example.

© Denis Shelemekh, 2020

"""
from collections import Counter
from typing import Iterator, TypeVar, Any, Iterable

T = TypeVar('T')


class Portfolio:
    """
    Portfolio class.
    Serves as holder and iterator of Stock objects.
    """

    def __init__(self) -> None:
        self.holdings = []

    def __iter__(self) -> Iterator[T]:
        return self.holdings.__iter__()

    def __len__(self) -> int:
        return len(self.holdings)

    def __getitem__(self, index: Any) -> Any:
        return self.holdings[index]

    def __contains__(self, name: Any) -> bool:
        # Generator expression
        return any(s.name == name for s in self.holdings)

    @property
    def total_cost(self) -> float:
        """
        Returns:
            Float: Total cost of stocks contained in portfolio.
        """
        return sum(s.cost for s in self.holdings)  # Generator expression

    def tabulate_shares(self) -> Counter:
        """
        Returns:
            Counter: Summarized dict containing names of stocks and shares for the portfolio.
        """
        total_shares = Counter()
        for _stock in self.holdings:
            total_shares[_stock.name] += _stock.shares
        return total_shares

    def append(self, _stock: stock.Stock) -> None:
        """
        Appends Stock object to portfolio.

        Args:
            _stock: Stock object to append.
        Raises:
            TypeError: When _stock is not of Stock type.
        """
        if not isinstance(_stock, stock.Stock):
            raise TypeError('Expected a Stock instance')
        self.holdings.append(_stock)

    @classmethod
    def from_csv(cls, lines: Iterable[Any], **opts):
        """
        Class method for reading portfolio from iterable.

        Args:
            lines: Iterable to process records from.
        Returns:
            Portfolio instance
        """
        self = cls()
        port_dicts = fileparse.parse_csv(lines,
                                         select=['name', 'shares', 'price'],
                                         types=[str, int, float],
                                         **opts)
        for _dict in port_dicts:
            self.append(stock.Stock(**_dict))  # Expand dictionary

        return self
