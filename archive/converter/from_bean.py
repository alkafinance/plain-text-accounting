from . import models
from beancount.core import data as bean
from itertools import chain
from datetime import date, datetime, time
from dacite import from_dict
import hashlib


def ledger_from_entries(entries: bean.Entries) -> models.Ledger:
    accounts = []
    transactions = []
    commodities = []
    prices = []
    tags = []  # need explicit declaration

    for entry in entries:
        if isinstance(entry, bean.Open):
            accounts.append(account_from_entry(entry))
        elif isinstance(entry, bean.Commodity):
            commodities.append(commodity_from_entry(entry))
        elif isinstance(entry, bean.Transaction):
            transactions.append(transaction_from_entry(entry))
        elif isinstance(entry, bean.Price):
            prices.append(price_from_entry(entry))

    return models.Ledger(
        accounts=accounts,
        commodities=commodities,
        prices=prices,
        transactions=transactions,
        version=models.Version.STANDARD_1,
    )


def account_from_entry(entry: bean.Open) -> models.Account:
    return models.Account(name=entry.account)


def commodity_from_entry(entry: bean.Commodity) -> models.Commodity:
    return models.Commodity(unit=entry.currency)


def price_from_entry(entry: bean.Price) -> models.Price:
    return models.Price(
        date=entry.date.isoformat(),
        quote=models.Amount(entry.amount.number, entry.amount.currency),
    )


def transaction_from_entry(entry: bean.Transaction) -> models.Transaction:
    return models.Transaction(
        # entry.date,
        # from_single_char_flag(entry.flag),
        # "#id",
        # list(entry.links),
        # entry.narration,
        # entry.payee,
        # list(map(posting_from_entry, entry.postings)),
        # list(entry.tags),
        date=entry.date.isoformat(),
        description=entry.narration,
        payee=entry.payee,
        flags=from_single_char_flag(entry.flag),
        labels_map={
            tag: True for tag in chain(entry.tags, map(lambda l: f"^{l}", entry.links))
        },
    )


def posting_from_entry(entry: bean.Posting) -> models.Posting:
    return models.Posting(
        # entry.account,
        # models.Amount(entry.units.number, entry.units.currency),
        # None,
        # "#id",
        account_name=entry.account_name
    )


def from_single_char_flag(flag: str) -> models.Flags:
    return {
        "!": models.Flags(follow_up=True),
        "*": models.Flags(confirmed=True),
        "?": models.Flags(pending=True),
    }[flag]


def account_id_name_type_from_name(name: str) -> (str, str, str):
    id = hashlib.md5(name.encode('utf-8')).hexdigest()
    splits = name.split(":")
    first = splits[0]
    remainder = "/".join(splits[1:])
    type = {
        "Asset": models.AccountType.BALANCE_SHEET_ASSET,
        "Assets": models.AccountType.BALANCE_SHEET_ASSET,
        "Liability": models.AccountType.BALANCE_SHEET_LIABILITY,
        "Liabilities": models.AccountType.BALANCE_SHEET_LIABILITY,
        "Equity": models.AccountType.BALANCE_SHEET_EQUITY,
        "Equities": models.AccountType.BALANCE_SHEET_EQUITY,
        "Income": models.AccountType.INCOME_STATEMENT_INCOME,
        "Revenue": models.AccountType.INCOME_STATEMENT_INCOME,
        "Expense": models.AccountType.INCOME_STATEMENT_EXPENSE,
        "Expenses": models.AccountType.INCOME_STATEMENT_EXPENSE,
    }[first]
    return (id, type, remainder)

