#!/usr/bin/env python3

# # Monkeypatch to start
# import beancount.core.display_context as dc

# from beancount.core import data as bean


# def amount_to_string(self, dformat=dc.DEFAULT_DISPLAY_CONTEXT.build(commas=True)):
#     """Convert an Amount instance to a printable string.

#         Args:
#           dformat: An instance of DisplayFormatter.
#         Returns:
#           A formatted string of the quantized amount and symbol.
#         """
#     number_fmt = (
#         dformat.format(self.number, self.currency)
#         if isinstance(self.number, bean.Decimal)
#         else str(self.number)
#     )
#     return "{} {}".format(number_fmt, self.currency)


# bean.Amount.to_string = amount_to_string

# print(bean.Amount(bean.D("-25880.78"), "USD").to_string())



# from beancount import loader
# import pprint
# import json
# import datetime
# import typedload
# from beancount.parser import printer
# from beancount.core.data import Open

# from beancount.core import data as models


# def myconverter(o):
#     if isinstance(o, datetime.datetime):
#         return o.__str__()


# filename = "./test.beancount"
# entries, errors, options = loader.load_file(filename)
# pp = pprint.PrettyPrinter(indent=4)

# # print(json.dumps(entries, default = myconverter))
# # print(entries)
# # pp.pprint(errors)
# # pp.pprint(options)


# # print(json.dumps(typedload.dump(entries[1])))
# meta = models.new_metadata("https://alka.one/example.json", 0)

# # data = {
# #     "meta": {
# #         "filename": "/Users/tony/dev/src/github.com/alkafinance/backend/test.beancount",
# #         "lineno": 5,
# #     },
# #     "date": [2014, 5, 1],
# #     "account": "Liabilities:CreditCard:CapitalOne",
# #     "currencies": ["USD"],
# #     "booking": None,
# # }
# entries = [
#     # typedload.load(data, Open)
#     models.Open(meta, datetime.date(2014, 1, 18), "Assets:MyAccount", ["USD"], None)
# ]


# for entry in entries:
#     printer.print_entry(entry)


# # dddd\

