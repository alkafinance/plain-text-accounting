from lib import bean_to_json, json_dumps_decimal

content = open("./examples/currency-conversion.bean", mode="r", encoding="utf-8").read()
json = bean_to_json(content)

print(json_dumps_decimal(json))