# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = amount_from_dict(json.loads(json_string))
#     result = commodity_from_dict(json.loads(json_string))
#     result = account_from_dict(json.loads(json_string))
#     result = flag_from_dict(json.loads(json_string))
#     result = posting_from_dict(json.loads(json_string))
#     result = transaction_from_dict(json.loads(json_string))
#     result = tag_from_dict(json.loads(json_string))
#     result = ledger_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, cast, Callable
from datetime import datetime
from enum import Enum
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


@dataclass
class Commodity:
    id: str
    name: Optional[str]
    unit: str

    @staticmethod
    def from_dict(obj: Any) -> 'Commodity':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        name = from_union([from_str, from_none], obj.get("name"))
        unit = from_str(obj.get("unit"))
        return Commodity(id, name, unit)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["name"] = from_union([from_str, from_none], self.name)
        result["unit"] = from_str(self.unit)
        return result


@dataclass
class Account:
    close_date: Optional[datetime]
    id: str
    open_date: datetime
    path: str

    @staticmethod
    def from_dict(obj: Any) -> 'Account':
        assert isinstance(obj, dict)
        close_date = from_union([from_datetime, from_none], obj.get("closeDate"))
        id = from_str(obj.get("id"))
        open_date = from_datetime(obj.get("openDate"))
        path = from_str(obj.get("path"))
        return Account(close_date, id, open_date, path)

    def to_dict(self) -> dict:
        result: dict = {}
        result["closeDate"] = from_union([lambda x: x.isoformat(), from_none], self.close_date)
        result["id"] = from_str(self.id)
        result["openDate"] = self.open_date.isoformat()
        result["path"] = from_str(self.path)
        return result


@dataclass
class Tag:
    date: datetime
    id: str
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'Tag':
        assert isinstance(obj, dict)
        date = from_datetime(obj.get("date"))
        id = from_str(obj.get("id"))
        name = from_str(obj.get("name"))
        return Tag(date, id, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["date"] = self.date.isoformat()
        result["id"] = from_str(self.id)
        result["name"] = from_str(self.name)
        return result


class Flag(Enum):
    ACTIONABLE = "Actionable"
    CONFIRMED = "Confirmed"
    NEW = "New"


@dataclass
class Amount:
    quantity: float
    unit: str

    @staticmethod
    def from_dict(obj: Any) -> 'Amount':
        assert isinstance(obj, dict)
        quantity = from_float(obj.get("quantity"))
        unit = from_str(obj.get("unit"))
        return Amount(quantity, unit)

    def to_dict(self) -> dict:
        result: dict = {}
        result["quantity"] = to_float(self.quantity)
        result["unit"] = from_str(self.unit)
        return result


@dataclass
class Posting:
    account_path: str
    amount: Amount
    flag: Optional[Flag]
    id: str

    @staticmethod
    def from_dict(obj: Any) -> 'Posting':
        assert isinstance(obj, dict)
        account_path = from_str(obj.get("accountPath"))
        amount = Amount.from_dict(obj.get("amount"))
        flag = from_union([Flag, from_none], obj.get("flag"))
        id = from_str(obj.get("id"))
        return Posting(account_path, amount, flag, id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["accountPath"] = from_str(self.account_path)
        result["amount"] = to_class(Amount, self.amount)
        result["flag"] = from_union([lambda x: to_enum(Flag, x), from_none], self.flag)
        result["id"] = from_str(self.id)
        return result


@dataclass
class Transaction:
    date: datetime
    flag: Optional[Flag]
    id: str
    """Used to connect multiple transactions together"""
    links: Optional[List[str]]
    narration: str
    payee: Optional[str]
    postings: List[Posting]
    tag_names: List[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Transaction':
        assert isinstance(obj, dict)
        date = from_datetime(obj.get("date"))
        flag = from_union([Flag, from_none], obj.get("flag"))
        id = from_str(obj.get("id"))
        links = from_union([lambda x: from_list(from_str, x), from_none], obj.get("links"))
        narration = from_str(obj.get("narration"))
        payee = from_union([from_str, from_none], obj.get("payee"))
        postings = from_list(Posting.from_dict, obj.get("postings"))
        tag_names = from_list(from_str, obj.get("tagNames"))
        return Transaction(date, flag, id, links, narration, payee, postings, tag_names)

    def to_dict(self) -> dict:
        result: dict = {}
        result["date"] = self.date.isoformat()
        result["flag"] = from_union([lambda x: to_enum(Flag, x), from_none], self.flag)
        result["id"] = from_str(self.id)
        result["links"] = from_union([lambda x: from_list(from_str, x), from_none], self.links)
        result["narration"] = from_str(self.narration)
        result["payee"] = from_union([from_str, from_none], self.payee)
        result["postings"] = from_list(lambda x: to_class(Posting, x), self.postings)
        result["tagNames"] = from_list(from_str, self.tag_names)
        return result


@dataclass
class Ledger:
    accounts: List[Account]
    date: datetime
    id: str
    tags: List[Tag]
    title: str
    transactions: List[Transaction]

    @staticmethod
    def from_dict(obj: Any) -> 'Ledger':
        assert isinstance(obj, dict)
        accounts = from_list(Account.from_dict, obj.get("accounts"))
        date = from_datetime(obj.get("date"))
        id = from_str(obj.get("id"))
        tags = from_list(Tag.from_dict, obj.get("tags"))
        title = from_str(obj.get("title"))
        transactions = from_list(Transaction.from_dict, obj.get("transactions"))
        return Ledger(accounts, date, id, tags, title, transactions)

    def to_dict(self) -> dict:
        result: dict = {}
        result["accounts"] = from_list(lambda x: to_class(Account, x), self.accounts)
        result["date"] = self.date.isoformat()
        result["id"] = from_str(self.id)
        result["tags"] = from_list(lambda x: to_class(Tag, x), self.tags)
        result["title"] = from_str(self.title)
        result["transactions"] = from_list(lambda x: to_class(Transaction, x), self.transactions)
        return result


def amount_from_dict(s: Any) -> Amount:
    return Amount.from_dict(s)


def amount_to_dict(x: Amount) -> Any:
    return to_class(Amount, x)


def commodity_from_dict(s: Any) -> Commodity:
    return Commodity.from_dict(s)


def commodity_to_dict(x: Commodity) -> Any:
    return to_class(Commodity, x)


def account_from_dict(s: Any) -> Account:
    return Account.from_dict(s)


def account_to_dict(x: Account) -> Any:
    return to_class(Account, x)


def flag_from_dict(s: Any) -> Flag:
    return Flag(s)


def flag_to_dict(x: Flag) -> Any:
    return to_enum(Flag, x)


def posting_from_dict(s: Any) -> Posting:
    return Posting.from_dict(s)


def posting_to_dict(x: Posting) -> Any:
    return to_class(Posting, x)


def transaction_from_dict(s: Any) -> Transaction:
    return Transaction.from_dict(s)


def transaction_to_dict(x: Transaction) -> Any:
    return to_class(Transaction, x)


def tag_from_dict(s: Any) -> Tag:
    return Tag.from_dict(s)


def tag_to_dict(x: Tag) -> Any:
    return to_class(Tag, x)


def ledger_from_dict(s: Any) -> Ledger:
    return Ledger.from_dict(s)


def ledger_to_dict(x: Ledger) -> Any:
    return to_class(Ledger, x)
