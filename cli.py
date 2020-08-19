from lib import (
    bean_to_json,
    json_dumps_decimal,
    json_load_decimal,
    json_to_bean,
    print_entries,
)

# content = open("./examples/currency-conversion.bean", mode="r", encoding="utf-8").read()
content = open("./examples/example.beancount", mode="r", encoding="utf-8").read()
json = bean_to_json(content)

json_string = json_dumps_decimal(json)
print(json_string)

json2 = json_load_decimal(json_string)
# print(json2)
entries = json_to_bean(json2)

print_entries(entries)
