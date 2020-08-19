from lib import (
    bean_to_json,
    json_dumps_decimal,
    json_load_decimal,
    json_to_bean,
    print_entries,
)

# content = open("./examples/currency-conversion.bean", mode="r", encoding="utf-8").read()
content = open("./examples/example.beancount", mode="r", encoding="utf-8").read()

json_string, *_ = bean_to_json(content)
bean_str, *_ = json_to_bean(json_string)

print(bean_str)
