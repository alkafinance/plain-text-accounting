#!/usr/bin/env python3
from beancount import loader
import pprint
import json
import datetime
import typedload
from beancount.parser import printer
from beancount.core.data import Open

from beancount.core import data as models


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


filename = "./test.beancount"
entries, errors, options = loader.load_file(filename)
pp = pprint.PrettyPrinter(indent=4)

# print(json.dumps(entries, default = myconverter))
# print(entries)
# pp.pprint(errors)
# pp.pprint(options)


# print(json.dumps(typedload.dump(entries[1])))
meta = models.new_metadata("https://alka.one/example.json", 0)

# data = {
#     "meta": {
#         "filename": "/Users/tony/dev/src/github.com/alkafinance/backend/test.beancount",
#         "lineno": 5,
#     },
#     "date": [2014, 5, 1],
#     "account": "Liabilities:CreditCard:CapitalOne",
#     "currencies": ["USD"],
#     "booking": None,
# }
entries = [
    # typedload.load(data, Open)
    models.Open(meta, datetime.date(2014, 1, 18), "Assets:MyAccount", ["USD"], None)
]


for entry in entries:
    printer.print_entry(entry)


# dddd\

