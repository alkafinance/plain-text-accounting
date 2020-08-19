from typing import Any
from beancount.core.data import Decimal, D, Entries
from beancount.core import data as bean
from beancount.core.display_context import DisplayContext
from beancount.parser import printer
from beancount import loader
from datetime import datetime, date

import json
import simplejson as simplejson

DISPLAY_CONTEXT = DisplayContext()
DISPLAY_CONTEXT.commas = True

def json_load_decimal(fp: Any) -> Any:
    return json.load(fp, parse_float=D, parse_constant=D, parse_int=D)


def json_dumps_decimal(obj: Any):
    return simplejson.dumps(obj, use_decimal=True, default=date_to_json)


def date_to_json(o: Any):
    if isinstance(o, (date, datetime)):
        return o.isoformat()

def print_entries(entries: Entries):
    printer.print_entries(entries, dcontext=DISPLAY_CONTEXT)

def get_entry_type(entry: bean.Directive):
    if isinstance(entry, bean.Open): return "Open"
    if isinstance(entry, bean.Close): return "Close"
    if isinstance(entry, bean.Commodity): return "Commodity"
    if isinstance(entry, bean.Pad): return "Pad"
    if isinstance(entry, bean.Balance): return "Balance"
    if isinstance(entry, bean.Transaction): return "Transaction"
    if isinstance(entry, bean.Note): return "Note"
    if isinstance(entry, bean.Event): return "Event"
    if isinstance(entry, bean.Query): return "Query"
    if isinstance(entry, bean.Price): return "Price"
    if isinstance(entry, bean.Document): return "Document"
    if isinstance(entry, bean.Custom): return "Custom"


def bean_to_json(content: str):
  entries, errors, options = loader.load_string(content)
  return {
      "variant": "beancount",
      "version": "2.2.1",
      "entries": list(map(lambda e: {"type": get_entry_type(e), "entry": e}, entries)),
      "errors": errors,
      "options": options
  }