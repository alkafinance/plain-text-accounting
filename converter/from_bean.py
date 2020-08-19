from . import models
from beancount.core import data as bean
from itertools import chain
from datetime import date, datetime, time
from dacite import from_dict


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

    ldgr = models.Ledger(
        accounts=accounts,
        commodities=commodities,
        prices=prices,
        transactions=transactions,
        version=models.Version.STANDARD_1,
    )
    return ldgr


def account_from_entry(entry: bean.Open) -> models.Account:
    acct = models.Account(name=entry.account)
    return acct


def commodity_from_entry(entry: bean.Commodity) -> models.Commodity:
    comm = models.Commodity(unit=entry.currency)
    return comm


def price_from_entry(entry: bean.Price) -> models.Price:
    prce = models.Price(
        date=entry.date.isoformat(), quote=models.Amount(entry.amount.number, entry.amount.currency)
    )
    return prce


def transaction_from_entry(entry: bean.Transaction) -> models.Transaction:
    txn = models.Transaction(
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
    )

    return txn


def posting_from_entry(entry: bean.Posting) -> models.Posting:
    return models.Posting(
        entry.account,
        models.Amount(entry.units.number, entry.units.currency),
        None,
        "#id",
    )


# def from_single_char_flag(flag: str) -> models.Flags:
#     return {
#         "!": models.Flags.ACTIONABLE,
#         "*": models.Flags.CONFIRMED,
#         "?": models.Flags.NEW,
#     }[flag]
