import json

from models import ledger_from_dict
from converter import entries_from_ledger
from beancount.parser import printer

ledger = ledger_from_dict(json.load(open("./pta.local.json", "r")))
entries = entries_from_ledger(ledger)

for entry in entries:
    printer.print_entry(entry)

