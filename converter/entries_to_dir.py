from beancount.core import data as bean
from itertools import chain
from datetime import date, datetime, time
from dacite import from_dict
from slugify import slugify
from beancount.parser import printer
from typing import Dict, List

from .utils import DISPLAY_CONTEXT

import os


def entries_to_dir(entries: bean.Entries):
    entries_by_path: Dict[str, List[bean.Directive]] = {}
    index_path = "journal/index.bean"
    index_entries = []
    entries_by_path[index_path] = index_entries

    for entry in entries:
        if isinstance(entry, bean.Open):
            path = path_from_account(entry.account)
            entries_by_path[path] = [entry]
        elif isinstance(entry, bean.Transaction):
            path = path_from_transaction(entry)
            entries_by_path[path].append(entry)
        else:
            index_entries.append(entry)

    for path, es in entries_by_path.items():
        dirname = os.path.dirname(path)
        if os.path.exists(dirname) == False:
            os.makedirs(dirname, exist_ok=True)
        printer.print_entries(es, dcontext=DISPLAY_CONTEXT, file=open(path, "w"))

    index_file = open(index_path, "a")
    index_file.write("\n; includes\n")
    for path in entries_by_path:
        if path == index_path:
            continue
        index_file.write('include "' + path.replace("journal", ".") + '"\n')


def path_from_account(account: str) -> str:
    return "journal/" + "/".join(map(slugify, account.split(":"))) + ".bean"


def path_from_transaction(txn: bean.Transaction) -> str:
    for posting in txn.postings:
        if posting.account != "Equity:Equity":
            return path_from_account(posting.account)
    raise Exception("Cannot compute path for transaction")
