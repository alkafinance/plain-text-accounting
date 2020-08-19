from beancount import loader

from converter.models import ledger_to_dict
from converter.utils import json_dumps_decimal, get_entry_type
from converter.from_bean import ledger_from_entries

entries, errors, options = loader.load_file("./examples/currency-conversion.bean")

# ledger = ledger_from_entries(entries)

# new_entries = list(map(lambda e: (get_entry_type(e), e), entries))

# print(new_entries)

print(json_dumps_decimal({
  "variant": "beancount@2.2.1",
  "entries": list(map(lambda e: {"type": get_entry_type(e), "entry": e}, entries)),
  "errors": errors,
  "options": options
}))
