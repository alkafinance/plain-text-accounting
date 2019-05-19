import models
from beancount.core import data as bean
from itertools import chain
from datetime import date

def entries_from_ledger(ledger: models.Ledger) -> bean.Entries:
    return chain(
        map(entry_from_account, ledger.accounts),
        map(entry_from_transaction, ledger.transactions),
    )


def entry_from_account(account: models.Account) -> bean.Open:
    return bean.Open(
        bean.new_metadata("", 0),
        # account.open_date,
        date.fromisoformat('2005-11-22'), # Temp hack until we fix open date
        account.path,
        [],
        None,
    )


def entry_from_transaction(txn: models.Transaction) -> bean.Transaction:
    return bean.Transaction(
        bean.new_metadata("", 0),
        txn.date,
        to_single_char_flag(txn.flag),
        txn.payee,
        txn.narration,
        set(txn.tag_names) if txn.tag_names else set(),
        set(txn.links) if txn.links else set(),
        list(map(entry_from_posting, txn.postings)),
    )


def entry_from_posting(posting: models.Posting) -> bean.Posting:
    return bean.Posting(
        posting.account_path,
        bean.Amount(posting.amount.quantity, posting.amount.unit),
        None,  # Cost / CostSpec
        None,  # Price
        None,  # Flag
        None,  # Meta
    )


def to_single_char_flag(flag: models.Flag) -> str:
    return {
        models.Flag.ACTIONABLE: "!",
        models.Flag.CONFIRMED: "*",
        models.Flag.NEW: "?",
    }[flag]
