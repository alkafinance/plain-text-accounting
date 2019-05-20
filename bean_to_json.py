from beancount import loader

from converter.models import ledger_to_dict
from converter.utils import json_dumps_decimal
from converter.from_bean import ledger_from_entries

entries, errors, options = loader.load_file("./main.bean")

ledger = ledger_from_entries(entries)

print(json_dumps_decimal(ledger_to_dict(ledger)))
