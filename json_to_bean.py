from converter.models import ledger_from_dict
from converter.utils import json_load_decimal, print_entries
from converter.to_bean import entries_from_ledger

ledger = ledger_from_dict(json_load_decimal(open("./pta.local.json", "r")))
entries = entries_from_ledger(ledger)

print_entries(list(entries))

