from . import models
from beancount.core import data as bean
from itertools import chain
from datetime import date, datetime, time
from dacite import from_dict


def ledger_from_entries(entries: bean.Entries) -> models.Ledger:
    accounts = []
    transactions = []
    commodities = []
    tags = []  # need explicit declaration

    for entry in entries:
        if isinstance(entry, bean.Open):
            accounts.append(account_from_entry(entry))
        elif isinstance(entry, bean.Commodity):
            commodities.append(commodity_from_entry(entry))
        elif isinstance(entry, bean.Transaction):
            transactions.append(transaction_from_entry(entry))

    return models.Ledger(
        accounts,
        commodities,
        date.fromisoformat("2000-01-01"),
        "#id",
        tags,
        "",
        transactions,
    )


def account_from_entry(entry: bean.Open) -> models.Account:
    return models.Account(None, "#id", entry.date, entry.account)


def commodity_from_entry(entry: bean.Commodity) -> models.Commodity:
    return models.Commodity(entry.currency, entry.meta["name"], entry.currency)


def transaction_from_entry(entry: bean.Transaction) -> models.Transaction:
    return models.Transaction(
        entry.date,
        from_single_char_flag(entry.flag),
        "#id",
        list(entry.links),
        entry.narration,
        entry.payee,
        list(map(posting_from_entry, entry.postings)),
        list(entry.tags),
    )


def posting_from_entry(entry: bean.Posting) -> models.Posting:
    return models.Posting(
        entry.account,
        models.Amount(entry.units.number, entry.units.currency),
        None,
        "#id",
    )


def from_single_char_flag(flag: str) -> models.Flag:
    return {
        "!": models.Flag.ACTIONABLE,
        "*": models.Flag.CONFIRMED,
        "?": models.Flag.NEW,
    }[flag]
