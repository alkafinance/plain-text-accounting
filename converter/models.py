# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = ledger_from_dict(json.loads(json_string))
#     result = unit_from_dict(json.loads(json_string))
#     result = iso_date_from_dict(json.loads(json_string))
#     result = iso_date_time_from_dict(json.loads(json_string))
#     result = connection_status_from_dict(json.loads(json_string))
#     result = connection_from_dict(json.loads(json_string))
#     result = statement_type_from_dict(json.loads(json_string))
#     result = account_type_prefix_from_dict(json.loads(json_string))
#     result = account_type_from_dict(json.loads(json_string))
#     result = account_subtype_prefix_from_dict(json.loads(json_string))
#     result = account_subtype_from_dict(json.loads(json_string))
#     result = commodity_type_from_dict(json.loads(json_string))
#     result = holding_from_dict(json.loads(json_string))
#     result = account_from_dict(json.loads(json_string))
#     result = transaction_from_dict(json.loads(json_string))
#     result = flags_from_dict(json.loads(json_string))
#     result = posting_from_dict(json.loads(json_string))
#     result = price_from_dict(json.loads(json_string))
#     result = commodity_from_dict(json.loads(json_string))
#     result = amount_from_dict(json.loads(json_string))
#     result = record_string_posting_from_dict(json.loads(json_string))
#     result = record_string_boolean_from_dict(json.loads(json_string))
#     result = record_string_any_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, Optional, List, Dict, TypeVar, Type, cast, Callable
from enum import Enum


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_float(x: Any) -> float:
    assert isinstance(x, float)
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


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


@dataclass
class Amount:
    """1.32 CAD
    
    Balance assignment
    """
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
class Holding:
    """Holding is really nothing but a posting and we may not actually need it at all
    See
    https://docs.google.com/document/d/1qPdNXaz5zuDQ8M9uoZFyyFis7hA0G55BEfhWhrVBsfc/edit#heading=h.n5ispaok8sog
    However many data vendors end up giving this and until we have a better way
    of representing it we'll keep it in the standard core. Though we should
    make this field not directly editable by the user, and only used at runtime
    by the providers
    """
    quantity: float
    unit: str
    """Per unit, not total. Informational, not used in accounting equation"""
    cost_basis: Optional[Amount] = None
    """Per unit, not total. Informational, not used in accounting equation"""
    last_quote: Optional[Amount] = None
    last_quote_date: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Holding':
        assert isinstance(obj, dict)
        quantity = from_float(obj.get("quantity"))
        unit = from_str(obj.get("unit"))
        cost_basis = from_union([Amount.from_dict, from_none], obj.get("costBasis"))
        last_quote = from_union([Amount.from_dict, from_none], obj.get("lastQuote"))
        last_quote_date = from_union([from_none, from_str], obj.get("lastQuoteDate"))
        return Holding(quantity, unit, cost_basis, last_quote, last_quote_date)

    def to_dict(self) -> dict:
        result: dict = {}
        result["quantity"] = to_float(self.quantity)
        result["unit"] = from_str(self.unit)
        result["costBasis"] = from_union([lambda x: to_class(Amount, x), from_none], self.cost_basis)
        result["lastQuote"] = from_union([lambda x: to_class(Amount, x), from_none], self.last_quote)
        result["lastQuoteDate"] = from_union([from_none, from_str], self.last_quote_date)
        return result


class AccountSubtype(Enum):
    ACCOUNTS_RECEIVABLE = "accounts_receivable"
    CASH = "cash"
    CHECKING = "checking"
    CREDIT_CARD = "credit_card"
    EXPENSE_FEES = "expense/fees"
    MISC_BALANCE_ASSIGNMENT = "misc/balance_assignment"
    MISC_INITIAL_BALANCE = "misc/initial_balance"
    MISC_RECONCILATION_ERROR = "misc/reconcilation_error"
    MISC_TRADING = "misc/trading"
    MISC_TRANSFER = "misc/transfer"
    MISC_UNCATEGORIZED = "misc/uncategorized"
    MORTGAGE = "mortgage"
    SAVINGS = "savings"


class AccountType(Enum):
    BALANCE_SHEET = "balance_sheet"
    BALANCE_SHEET_ASSET = "balance_sheet/asset"
    BALANCE_SHEET_EQUITY = "balance_sheet/equity"
    BALANCE_SHEET_LIABILITY = "balance_sheet/liability"
    INCOME_STATEMENT = "income_statement"
    INCOME_STATEMENT_EXPENSE = "income_statement/expense"
    INCOME_STATEMENT_INCOME = "income_statement/income"
    OTHER = "other"


@dataclass
class Account:
    """e.g. `Chase Checking`"""
    name: str
    balance: Optional[Amount] = None
    close_date: Optional[str] = None
    """ISO country code ideally, but really could be anything..."""
    country_code: Optional[str] = None
    default_unit: Optional[str] = None
    """Should not be edited by the user
    When present, the `balance` field above should be completely informational
    and not factor into the accounting equation
    """
    holdings: Optional[List[Holding]] = None
    institution_name: Optional[str] = None
    last_four: Optional[str] = None
    """
    https://en.wikipedia.org/wiki/Cash_and_cash_equivalents#:~:text=Cash%20and%20cash%20equivalents%20(CCE,into%20a%20known%20cash%20amount%22.
    """
    liquidity: Optional[str] = None
    notes: Optional[str] = None
    open_date: Optional[str] = None
    removed: Optional[bool] = None
    subtype: Optional[AccountSubtype] = None
    type: Optional[AccountType] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Account':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        balance = from_union([Amount.from_dict, from_none], obj.get("balance"))
        close_date = from_union([from_none, from_str], obj.get("closeDate"))
        country_code = from_union([from_none, from_str], obj.get("countryCode"))
        default_unit = from_union([from_none, from_str], obj.get("defaultUnit"))
        holdings = from_union([lambda x: from_list(Holding.from_dict, x), from_none], obj.get("holdings"))
        institution_name = from_union([from_none, from_str], obj.get("institutionName"))
        last_four = from_union([from_none, from_str], obj.get("lastFour"))
        liquidity = from_union([from_none, from_str], obj.get("liquidity"))
        notes = from_union([from_none, from_str], obj.get("notes"))
        open_date = from_union([from_none, from_str], obj.get("openDate"))
        removed = from_union([from_bool, from_none], obj.get("removed"))
        subtype = from_union([AccountSubtype, from_none], obj.get("subtype"))
        type = from_union([AccountType, from_none], obj.get("type"))
        return Account(name, balance, close_date, country_code, default_unit, holdings, institution_name, last_four, liquidity, notes, open_date, removed, subtype, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["balance"] = from_union([lambda x: to_class(Amount, x), from_none], self.balance)
        result["closeDate"] = from_union([from_none, from_str], self.close_date)
        result["countryCode"] = from_union([from_none, from_str], self.country_code)
        result["defaultUnit"] = from_union([from_none, from_str], self.default_unit)
        result["holdings"] = from_union([lambda x: from_list(lambda x: to_class(Holding, x), x), from_none], self.holdings)
        result["institutionName"] = from_union([from_none, from_str], self.institution_name)
        result["lastFour"] = from_union([from_none, from_str], self.last_four)
        result["liquidity"] = from_union([from_none, from_str], self.liquidity)
        result["notes"] = from_union([from_none, from_str], self.notes)
        result["openDate"] = from_union([from_none, from_str], self.open_date)
        result["removed"] = from_union([from_bool, from_none], self.removed)
        result["subtype"] = from_union([lambda x: to_enum(AccountSubtype, x), from_none], self.subtype)
        result["type"] = from_union([lambda x: to_enum(AccountType, x), from_none], self.type)
        return result


class CommodityType(Enum):
    CRYPTO = "crypto"
    CURRENCY = "currency"
    STOCK = "stock"


@dataclass
class Commodity:
    """symbol. `USD`"""
    unit: str
    description: Optional[str] = None
    exponent: Optional[float] = None
    """`US Dollar`"""
    name: Optional[str] = None
    type: Optional[CommodityType] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Commodity':
        assert isinstance(obj, dict)
        unit = from_str(obj.get("unit"))
        description = from_union([from_str, from_none], obj.get("description"))
        exponent = from_union([from_none, from_float], obj.get("exponent"))
        name = from_union([from_str, from_none], obj.get("name"))
        type = from_union([from_none, CommodityType], obj.get("type"))
        return Commodity(unit, description, exponent, name, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["unit"] = from_str(self.unit)
        result["description"] = from_union([from_str, from_none], self.description)
        result["exponent"] = from_union([from_none, to_float], self.exponent)
        result["name"] = from_union([from_str, from_none], self.name)
        result["type"] = from_union([from_none, lambda x: to_enum(CommodityType, x)], self.type)
        return result


@dataclass
class Price:
    """USD:CAD = 1.32
    [base]:[target] = [rate]
    """
    """`USD`"""
    base_unit: str
    """Assuming closing price of the day"""
    date: str
    """1.32 CAD"""
    quote: Amount

    @staticmethod
    def from_dict(obj: Any) -> 'Price':
        assert isinstance(obj, dict)
        base_unit = from_str(obj.get("baseUnit"))
        date = from_str(obj.get("date"))
        quote = Amount.from_dict(obj.get("quote"))
        return Price(base_unit, date, quote)

    def to_dict(self) -> dict:
        result: dict = {}
        result["baseUnit"] = from_str(self.base_unit)
        result["date"] = from_str(self.date)
        result["quote"] = to_class(Amount, self.quote)
        return result


@dataclass
class Flags:
    """Do not use for now"""
    cancelled: Optional[bool] = None
    confirmed: Optional[bool] = None
    follow_up: Optional[bool] = None
    pending: Optional[bool] = None
    transfer: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Flags':
        assert isinstance(obj, dict)
        cancelled = from_union([from_bool, from_none], obj.get("cancelled"))
        confirmed = from_union([from_bool, from_none], obj.get("confirmed"))
        follow_up = from_union([from_bool, from_none], obj.get("followUp"))
        pending = from_union([from_bool, from_none], obj.get("pending"))
        transfer = from_union([from_bool, from_none], obj.get("transfer"))
        return Flags(cancelled, confirmed, follow_up, pending, transfer)

    def to_dict(self) -> dict:
        result: dict = {}
        result["cancelled"] = from_union([from_bool, from_none], self.cancelled)
        result["confirmed"] = from_union([from_bool, from_none], self.confirmed)
        result["followUp"] = from_union([from_bool, from_none], self.follow_up)
        result["pending"] = from_union([from_bool, from_none], self.pending)
        result["transfer"] = from_union([from_bool, from_none], self.transfer)
        return result


@dataclass
class Transaction:
    date: str
    """Should be exactly as it appears on user's bank statement.
    payee | merchant | name https://hledger.org/journal.html#payee-and-note
    """
    description: str
    flags: Optional[Flags] = None
    """Label Name -> enabled"""
    labels_map: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
    """Aka Merchant | Customer | Vendor
    Often time same as the simpleDescription field. In particular this is a field
    we can depend on to render custom icons for each transaction (e.g. Walmart icon)
    """
    payee: Optional[str] = None
    """https://support.plaid.com/hc/en-us/articles/360008271814-Pending-transaction-overview"""
    pending_transaction_external_id: Optional[str] = None
    postings_map: Optional[Dict[str, Any]] = None
    removed: Optional[bool] = None
    """Provider's best guess attempt at an easy-to-understand, plain-language
    transaction description derived from original, abbreviated and, sometimes
    cryptic, transaction description
    https://developer.yodlee.com/docs/api/1.1/Transaction_Data_Enrichment
    """
    simple_description: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Transaction':
        assert isinstance(obj, dict)
        date = from_str(obj.get("date"))
        description = from_str(obj.get("description"))
        flags = from_union([Flags.from_dict, from_none], obj.get("flags"))
        labels_map = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("labelsMap"))
        notes = from_union([from_none, from_str], obj.get("notes"))
        payee = from_union([from_str, from_none], obj.get("payee"))
        pending_transaction_external_id = from_union([from_none, from_str], obj.get("pendingTransactionExternalId"))
        postings_map = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("postingsMap"))
        removed = from_union([from_bool, from_none], obj.get("removed"))
        simple_description = from_union([from_str, from_none], obj.get("simpleDescription"))
        return Transaction(date, description, flags, labels_map, notes, payee, pending_transaction_external_id, postings_map, removed, simple_description)

    def to_dict(self) -> dict:
        result: dict = {}
        result["date"] = from_str(self.date)
        result["description"] = from_str(self.description)
        result["flags"] = from_union([lambda x: to_class(Flags, x), from_none], self.flags)
        result["labelsMap"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.labels_map)
        result["notes"] = from_union([from_none, from_str], self.notes)
        result["payee"] = from_union([from_str, from_none], self.payee)
        result["pendingTransactionExternalId"] = from_union([from_none, from_str], self.pending_transaction_external_id)
        result["postingsMap"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.postings_map)
        result["removed"] = from_union([from_bool, from_none], self.removed)
        result["simpleDescription"] = from_union([from_str, from_none], self.simple_description)
        return result


class Version(Enum):
    STANDARD_1 = "standard-1"


@dataclass
class Ledger:
    accounts: List[Account]
    commodities: List[Commodity]
    prices: List[Price]
    transactions: List[Transaction]
    version: Version

    @staticmethod
    def from_dict(obj: Any) -> 'Ledger':
        assert isinstance(obj, dict)
        accounts = from_list(Account.from_dict, obj.get("accounts"))
        commodities = from_list(Commodity.from_dict, obj.get("commodities"))
        prices = from_list(Price.from_dict, obj.get("prices"))
        transactions = from_list(Transaction.from_dict, obj.get("transactions"))
        version = Version(obj.get("version"))
        return Ledger(accounts, commodities, prices, transactions, version)

    def to_dict(self) -> dict:
        result: dict = {}
        result["accounts"] = from_list(lambda x: to_class(Account, x), self.accounts)
        result["commodities"] = from_list(lambda x: to_class(Commodity, x), self.commodities)
        result["prices"] = from_list(lambda x: to_class(Price, x), self.prices)
        result["transactions"] = from_list(lambda x: to_class(Transaction, x), self.transactions)
        result["version"] = to_enum(Version, self.version)
        return result


@dataclass
class Institution:
    logo_url: str
    name: str
    url: str

    @staticmethod
    def from_dict(obj: Any) -> 'Institution':
        assert isinstance(obj, dict)
        logo_url = from_str(obj.get("logoUrl"))
        name = from_str(obj.get("name"))
        url = from_str(obj.get("url"))
        return Institution(logo_url, name, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["logoUrl"] = from_str(self.logo_url)
        result["name"] = from_str(self.name)
        result["url"] = from_str(self.url)
        return result


class ConnectionStatus(Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"


@dataclass
class Connection:
    status: ConnectionStatus
    """Whether we should hide the connection from user interface because
    it's really an implementation detail. Only applies to Yodlee.User for now
    """
    hidden: Optional[bool] = None
    institution: Optional[Institution] = None
    last_successful_refresh: Optional[str] = None
    name: Optional[str] = None
    removed: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Connection':
        assert isinstance(obj, dict)
        status = ConnectionStatus(obj.get("status"))
        hidden = from_union([from_bool, from_none], obj.get("hidden"))
        institution = from_union([Institution.from_dict, from_none], obj.get("institution"))
        last_successful_refresh = from_union([from_none, from_str], obj.get("lastSuccessfulRefresh"))
        name = from_union([from_none, from_str], obj.get("name"))
        removed = from_union([from_bool, from_none], obj.get("removed"))
        return Connection(status, hidden, institution, last_successful_refresh, name, removed)

    def to_dict(self) -> dict:
        result: dict = {}
        result["status"] = to_enum(ConnectionStatus, self.status)
        result["hidden"] = from_union([from_bool, from_none], self.hidden)
        result["institution"] = from_union([lambda x: to_class(Institution, x), from_none], self.institution)
        result["lastSuccessfulRefresh"] = from_union([from_none, from_str], self.last_successful_refresh)
        result["name"] = from_union([from_none, from_str], self.name)
        result["removed"] = from_union([from_bool, from_none], self.removed)
        return result


class AccountTypePrefix(Enum):
    BALANCE_SHEET = "balance_sheet"
    INCOME_STATEMENT = "income_statement"
    OTHER = "other"


class AccountSubtypePrefix(Enum):
    MISC = "misc"


class TypeEnum(Enum):
    TOTAL = "total"
    UNIT = "unit"


@dataclass
class Cost:
    amount: Amount
    type: TypeEnum
    date: Optional[str] = None
    label: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Cost':
        assert isinstance(obj, dict)
        amount = Amount.from_dict(obj.get("amount"))
        type = TypeEnum(obj.get("type"))
        date = from_union([from_str, from_none], obj.get("date"))
        label = from_union([from_str, from_none], obj.get("label"))
        return Cost(amount, type, date, label)

    def to_dict(self) -> dict:
        result: dict = {}
        result["amount"] = to_class(Amount, self.amount)
        result["type"] = to_enum(TypeEnum, self.type)
        result["date"] = from_union([from_str, from_none], self.date)
        result["label"] = from_union([from_str, from_none], self.label)
        return result


@dataclass
class Posting:
    amount: Amount
    """Maps to accountId?: Id.acct"""
    account_external_id: Optional[str] = None
    """Chase Checking"""
    account_name: Optional[str] = None
    account_subtype: Optional[AccountSubtype] = None
    account_type: Optional[AccountType] = None
    """Balance assignment"""
    balance: Optional[Amount] = None
    """Comment out as price ought to be inferred. However, which specific
    posting would have inferred price? Now that's the question
    See https://share.getcloudapp.com/ApukLmdx
    Mainly useful for lot-tracking and holding information.
    Would be inferred unless otherwise explicitly stated.
    """
    cost: Optional[Cost] = None
    """Posting level custom fields"""
    custom: Optional[Dict[str, Any]] = None
    date: Optional[str] = None
    """Do not use for now"""
    flags: Optional[Flags] = None
    memo: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Posting':
        assert isinstance(obj, dict)
        amount = Amount.from_dict(obj.get("amount"))
        account_external_id = from_union([from_str, from_none], obj.get("accountExternalId"))
        account_name = from_union([from_none, from_str], obj.get("accountName"))
        account_subtype = from_union([AccountSubtype, from_none], obj.get("accountSubtype"))
        account_type = from_union([AccountType, from_none], obj.get("accountType"))
        balance = from_union([Amount.from_dict, from_none], obj.get("balance"))
        cost = from_union([Cost.from_dict, from_none], obj.get("cost"))
        custom = from_union([lambda x: from_dict(lambda x: x, x), from_none], obj.get("custom"))
        date = from_union([from_str, from_none], obj.get("date"))
        flags = from_union([Flags.from_dict, from_none], obj.get("flags"))
        memo = from_union([from_none, from_str], obj.get("memo"))
        return Posting(amount, account_external_id, account_name, account_subtype, account_type, balance, cost, custom, date, flags, memo)

    def to_dict(self) -> dict:
        result: dict = {}
        result["amount"] = to_class(Amount, self.amount)
        result["accountExternalId"] = from_union([from_str, from_none], self.account_external_id)
        result["accountName"] = from_union([from_none, from_str], self.account_name)
        result["accountSubtype"] = from_union([lambda x: to_enum(AccountSubtype, x), from_none], self.account_subtype)
        result["accountType"] = from_union([lambda x: to_enum(AccountType, x), from_none], self.account_type)
        result["balance"] = from_union([lambda x: to_class(Amount, x), from_none], self.balance)
        result["cost"] = from_union([lambda x: to_class(Cost, x), from_none], self.cost)
        result["custom"] = from_union([lambda x: from_dict(lambda x: x, x), from_none], self.custom)
        result["date"] = from_union([from_str, from_none], self.date)
        result["flags"] = from_union([lambda x: to_class(Flags, x), from_none], self.flags)
        result["memo"] = from_union([from_none, from_str], self.memo)
        return result


def ledger_from_dict(s: Any) -> Ledger:
    return Ledger.from_dict(s)


def ledger_to_dict(x: Ledger) -> Any:
    return to_class(Ledger, x)


def unit_from_dict(s: Any) -> str:
    return from_str(s)


def unit_to_dict(x: str) -> Any:
    return from_str(x)


def iso_date_from_dict(s: Any) -> str:
    return from_str(s)


def iso_date_to_dict(x: str) -> Any:
    return from_str(x)


def iso_date_time_from_dict(s: Any) -> str:
    return from_str(s)


def iso_date_time_to_dict(x: str) -> Any:
    return from_str(x)


def connection_status_from_dict(s: Any) -> ConnectionStatus:
    return ConnectionStatus(s)


def connection_status_to_dict(x: ConnectionStatus) -> Any:
    return to_enum(ConnectionStatus, x)


def connection_from_dict(s: Any) -> Connection:
    return Connection.from_dict(s)


def connection_to_dict(x: Connection) -> Any:
    return to_class(Connection, x)


def statement_type_from_dict(s: Any) -> AccountTypePrefix:
    return AccountTypePrefix(s)


def statement_type_to_dict(x: AccountTypePrefix) -> Any:
    return to_enum(AccountTypePrefix, x)


def account_type_prefix_from_dict(s: Any) -> AccountTypePrefix:
    return AccountTypePrefix(s)


def account_type_prefix_to_dict(x: AccountTypePrefix) -> Any:
    return to_enum(AccountTypePrefix, x)


def account_type_from_dict(s: Any) -> AccountType:
    return AccountType(s)


def account_type_to_dict(x: AccountType) -> Any:
    return to_enum(AccountType, x)


def account_subtype_prefix_from_dict(s: Any) -> AccountSubtypePrefix:
    return AccountSubtypePrefix(s)


def account_subtype_prefix_to_dict(x: AccountSubtypePrefix) -> Any:
    return to_enum(AccountSubtypePrefix, x)


def account_subtype_from_dict(s: Any) -> AccountSubtype:
    return AccountSubtype(s)


def account_subtype_to_dict(x: AccountSubtype) -> Any:
    return to_enum(AccountSubtype, x)


def commodity_type_from_dict(s: Any) -> CommodityType:
    return CommodityType(s)


def commodity_type_to_dict(x: CommodityType) -> Any:
    return to_enum(CommodityType, x)


def holding_from_dict(s: Any) -> Holding:
    return Holding.from_dict(s)


def holding_to_dict(x: Holding) -> Any:
    return to_class(Holding, x)


def account_from_dict(s: Any) -> Account:
    return Account.from_dict(s)


def account_to_dict(x: Account) -> Any:
    return to_class(Account, x)


def transaction_from_dict(s: Any) -> Transaction:
    return Transaction.from_dict(s)


def transaction_to_dict(x: Transaction) -> Any:
    return to_class(Transaction, x)


def flags_from_dict(s: Any) -> Flags:
    return Flags.from_dict(s)


def flags_to_dict(x: Flags) -> Any:
    return to_class(Flags, x)


def posting_from_dict(s: Any) -> Posting:
    return Posting.from_dict(s)


def posting_to_dict(x: Posting) -> Any:
    return to_class(Posting, x)


def price_from_dict(s: Any) -> Price:
    return Price.from_dict(s)


def price_to_dict(x: Price) -> Any:
    return to_class(Price, x)


def commodity_from_dict(s: Any) -> Commodity:
    return Commodity.from_dict(s)


def commodity_to_dict(x: Commodity) -> Any:
    return to_class(Commodity, x)


def amount_from_dict(s: Any) -> Amount:
    return Amount.from_dict(s)


def amount_to_dict(x: Amount) -> Any:
    return to_class(Amount, x)


def record_string_posting_from_dict(s: Any) -> Dict[str, Any]:
    return from_dict(lambda x: x, s)


def record_string_posting_to_dict(x: Dict[str, Any]) -> Any:
    return from_dict(lambda x: x, x)


def record_string_boolean_from_dict(s: Any) -> Dict[str, Any]:
    return from_dict(lambda x: x, s)


def record_string_boolean_to_dict(x: Dict[str, Any]) -> Any:
    return from_dict(lambda x: x, x)


def record_string_any_from_dict(s: Any) -> Dict[str, Any]:
    return from_dict(lambda x: x, s)


def record_string_any_to_dict(x: Dict[str, Any]) -> Any:
    return from_dict(lambda x: x, x)
