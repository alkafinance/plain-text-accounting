from beancount import loader
from beancount.core import data as bean

from utils import print_entries
from journal_to_json_converter import ledger_from_entries
from utils import json_dumps_decimal
import models as models


entries, errors, options = loader.load_file("./main.bean")

ledger = ledger_from_entries(entries)

print(json_dumps_decimal(models.ledger_to_dict(ledger)))

# print_entries(list(filter(lambda e: isinstance(e, bean.Open), entries)))


# accounts = map(account_from_entry, filter(lambda e: isinstance(e, bean.Open), entries))

# commodities = map(commodity_from_entry, filter(lambda e: isinstance(e, bean.Commodity), entries))

# print(list(accounts))


# print(len(entries)

