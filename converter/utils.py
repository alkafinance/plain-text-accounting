from typing import Optional, Any, List, TypeVar, Type, cast, Callable
from beancount.core.data import Decimal, D, Entries
from beancount.core.display_context import DisplayContext
from beancount.parser import printer
from datetime import datetime

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
    return simplejson.dumps(obj, use_decimal=True)


def print_entries(entries: Entries):
    dc = DisplayContext()
    dc.commas = True
    printer.print_entries(entries, dcontext=dc)
