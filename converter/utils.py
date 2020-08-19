from typing import Optional, Any, List, TypeVar, Type, cast, Callable
from beancount.core.data import Decimal, D, Entries
from beancount.core import data as bean
from beancount.core.display_context import DisplayContext
from beancount.parser import printer
from datetime import datetime, date

import dateutil.parser
import json
import simplejson as simplejson


class DecimalEncoder(json.JSONEncoder):
    def _iterencode(self, o, markers=None):
        if isinstance(o, Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)


def from_datetime(x: Any) -> datetime:
    """Ignore date component"""
    return dateutil.parser.parse(x).date()


def from_decimal(x: Any) -> Decimal:
    assert isinstance(x, (Decimal)) and not isinstance(x, bool)
    return D(x)


def to_decimal(x: Any) -> Decimal:
    assert isinstance(x, Decimal)
    return x


def json_load_decimal(fp) -> Any:
    return json.load(fp, parse_float=D, parse_constant=D, parse_int=D)


def json_dumps_decimal(obj):
    return simplejson.dumps(obj, use_decimal=True, default=date_to_json)


def date_to_json(o: Any):
    if isinstance(o, (date, datetime)):
        return o.isoformat()


def clean_nones(value):
    """
    Recursively remove all None values from dictionaries and lists, and returns
    the result as a new dictionary or list.
    https://stackoverflow.com/questions/4255400/exclude-empty-null-values-from-json-serialization/4257279
    """
    if isinstance(value, list):
        return [clean_nones(x) for x in value if x is not None]
    elif isinstance(value, dict):
        return {key: clean_nones(val) for key, val in value.items() if val is not None}
    else:
        return value


DISPLAY_CONTEXT = DisplayContext()
DISPLAY_CONTEXT.commas = True


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