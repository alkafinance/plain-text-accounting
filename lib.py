from typing import Any, Set
from beancount.core.data import Decimal, D, Entries
from beancount.core import data as bean
from beancount.core import compare
from beancount.core.display_context import DisplayContext
from beancount.parser import printer
from beancount import loader
from operator import itemgetter

import io
import datetime
import dateutil.parser
import json
import simplejson as simplejson

DISPLAY_CONTEXT = DisplayContext()
DISPLAY_CONTEXT.commas = True


def json_load_decimal(str: str) -> Any:
    return json.loads(str, parse_float=D, parse_constant=D, parse_int=D)


def json_dumps_decimal(obj: Any):
    return simplejson.dumps(
        obj, use_decimal=True, default=json_default, iterable_as_array=True
    )


def json_default(o: Any):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def print_entries(entries: Entries):
    printer.print_entries(entries, dcontext=DISPLAY_CONTEXT)


def get_entry_type(entry: bean.Directive):
    if isinstance(entry, bean.Open):
        return "Open"
    if isinstance(entry, bean.Close):
        return "Close"
    if isinstance(entry, bean.Commodity):
        return "Commodity"
    if isinstance(entry, bean.Pad):
        return "Pad"
    if isinstance(entry, bean.Balance):
        return "Balance"
    if isinstance(entry, bean.Transaction):
        return "Transaction"
    if isinstance(entry, bean.Note):
        return "Note"
    if isinstance(entry, bean.Event):
        return "Event"
    if isinstance(entry, bean.Query):
        return "Query"
    if isinstance(entry, bean.Price):
        return "Price"
    if isinstance(entry, bean.Document):
        return "Document"
    if isinstance(entry, bean.Custom):
        return "Custom"


def parse_date(d: str):
    if d is None:
        return d
    return dateutil.parser.parse(d).date()


def parse_amount(d: dict) -> bean.Amount:
    if d is None:
        return d
    return bean.Amount(number=d["number"], currency=d["currency"])


def parse_cost(c: dict) -> bean.Cost:
    if c is None:
        return c
    return bean.Cost(
        number=c["number"],
        currency=c["currency"],
        date=parse_date(c.get("date")),
        label=c.get("label"),
    )


def parse_posting(p: dict) -> bean.Posting:
    return bean.Posting(
        account=p["account"],
        units=parse_amount(p["units"]),
        cost=parse_cost(p["cost"] if "cost" in p else None),
        price=parse_amount(p["price"] if "price" in p else None),
        flag=p.get("flag"),
        meta=p.get("meta"),
    )


def wrap_entry(entry: bean.Directive):
    return {
        "type": get_entry_type(entry),
        "entry": entry,
        "hash": compare.hash_entry(entry),
    }


def unwrap_entry(data: dict) -> bean.Directive:
    type, e = itemgetter("type", "entry")(data)
    meta = e.get("meta")
    date = parse_date(e["date"])
    if type == "Open":
        return bean.Open(
            meta,
            date,
            account=e["account"],
            currencies=e.get("currencies", []),
            booking=e.get("booking"),
        )
    if type == "Close":
        return bean.Close(meta, date, account=e["account"])
    if type == "Commodity":
        return bean.Commodity(meta, date, currency=e["currency"])
    if type == "Pad":
        return bean.Pad(
            meta, date, account=e["account"], source_account=e["source_account"]
        )
    if type == "Balance":
        return bean.Balance(
            meta,
            date,
            account=e["account"],
            amount=parse_amount(e["amount"]),
            tolerance=e.get("tolerance"),
            diff_amount=e.get("diff_amount"),
        )
    if type == "Transaction":
        return bean.Transaction(
            meta,
            date,
            flag=e["flag"],
            payee=e.get("payee"),
            narration=e["narration"],
            tags=set(e["tags"] if "tags" in e else []),
            links=set(e["links"] if "links" in e else []),
            postings=[parse_posting(p) for p in e.get("postings", [])],
        )
    if type == "Note":
        return bean.Note(meta, date, account=e["account"], comment=e.get("comment", ""))
    if type == "Event":
        return bean.Event(meta, date, type=e["type"], description=e["description"])
    if type == "Query":
        return bean.Query(meta, date, name=e["name"], query_string=e["query_string"])
    if type == "Price":
        return bean.Price(
            meta, date, currency=e["currency"], amount=parse_amount(e["amount"])
        )
    if type == "Document":
        return bean.Document(
            meta,
            date,
            account=e["account"],
            filename=e["filename"],
            tags=set(e["tags"] if "tags" in e else []),
            links=set(e["links"] if "links" in e else []),
        )
    if type == "Custom":
        return bean.Custom(meta, date, type=e["type"], values=e["values"])


def bean_to_json(bean_str: str):
    if 'beancount.plugins.auto_accounts' not in bean_str:
        bean_str = 'plugin "beancount.plugins.auto_accounts"\n' + bean_str
    entries, errors, options = loader.load_string(bean_str)
    data = {
        "variant": "beancount",
        "version": "2.2.1",
        "entries": list(map(wrap_entry, entries)),
        "errors": errors,
        "options": options,
    }
    return json_dumps_decimal(data), data


def json_to_bean(json_str: dict):
    data = json_load_decimal(json_str)
    entries = [unwrap_entry(data) for data in data["entries"]]
    currs = data.get("options", {}).get("operating_currency", [])
    options = '\n'.join([f'option "operating_currency" "{c}"' for c in currs])
    if len(options) > 0:
        options = options + '\n\n'

    buff = io.StringIO()
    printer.print_entries(entries, dcontext=DISPLAY_CONTEXT, file=buff)
    buff.seek(0)

    return options + buff.read(), entries, data["errors"], data["options"]

