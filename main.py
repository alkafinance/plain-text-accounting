from models import ledger_from_dict
from converter import entries_from_ledger
from utils import json_load_decimal, print_entries

ledger = ledger_from_dict(json_load_decimal(open("./pta.local.json", "r")))
entries = entries_from_ledger(ledger)

print_entries(list(entries))

