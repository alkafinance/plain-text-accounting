from typing import Any, Set
from beancount.core.data import Decimal, D, Entries
from beancount.core import data as bean
from beancount.core.display_context import DisplayContext
from beancount.parser import printer
from beancount import loader
from operator import itemgetter

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


def parseDate(d: str):
    if d is None:
        return d
    return dateutil.parser.parse(d).date()


def parseAmount(d: dict) -> bean.Amount:
    if d is None:
        return d
    return bean.Amount(number=d["number"], currency=d["currency"])


def parseCost(c: dict) -> bean.Cost:
    if c is None:
        return c
    return bean.Cost(
        number=c["number"],
        currency=c["currency"],
        date=parseDate(c["date"]),
        label=c["label"],
    )


def parsePosting(p: dict) -> bean.Posting:
    return bean.Posting(
        account=p["account"],
        units=parseAmount(p["units"]),
        cost=parseCost(p["cost"]),
        price=parseAmount(p["price"]),
        flag=p["flag"],
        meta=p["meta"],
    )


def wrap_entry(entry: bean.Directive):
    return {"type": get_entry_type(entry), "entry": entry}


def unwrap_entry(data: dict) -> bean.Directive:
    type, e = itemgetter("type", "entry")(data)
    meta = e["meta"]
    date = parseDate(e["date"])
    if type == "Open":
        return bean.Open(
            meta,
            date,
            account=e["account"],
            currencies=e["currencies"],
            booking=e["booking"],
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
            amount=parseAmount(e["amount"]),
            tolerance=e["tolerance"],
            diff_amount=e["diff_amount"],
        )
    if type == "Transaction":
        return bean.Transaction(
            meta,
            date,
            flag=e["flag"],
            payee=e["payee"],
            narration=e["narration"],
            tags=set(e["tags"] or []),
            links=set(e["links"] or []),
            postings=[parsePosting(p) for p in e["postings"] or []],
        )
    if type == "Note":
        return bean.Note(meta, date, account=e["account"], comment=e["comment"])
    if type == "Event":
        return bean.Event(meta, date, type=e["type"], description=e["description"])
    if type == "Query":
        return bean.Query(meta, date, name=e["name"], query_string=e["query_string"])
    if type == "Price":
        return bean.Price(
            meta, date, currency=e["currency"], amount=parseAmount(e["amount"])
        )
    if type == "Document":
        return bean.Document(
            meta,
            date,
            account=e["account"],
            filename=e["filename"],
            tags=set(e["tags"] or []),
            links=set(e["links"] or []),
        )
    if type == "Custom":
        return bean.Custom(meta, date, type=e["type"], values=e["values"])


def bean_to_json(content: str):
    entries, errors, options = loader.load_string(content)
    return {
        "variant": "beancount",
        "version": "2.2.1",
        "entries": list(
            map(lambda e: {"type": get_entry_type(e), "entry": e}, entries)
        ),
        "errors": errors,
        "options": options,
    }


def json_to_bean(json: dict):
    entries = [unwrap_entry(data) for data in json["entries"]]
    print(entries)
    return entries

