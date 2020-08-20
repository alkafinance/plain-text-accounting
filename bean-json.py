import argparse, sys
from lib import bean_to_json, json_to_bean

parser = argparse.ArgumentParser(description="Beancount JSON")
parser.add_argument("command", help="bean_to_json | json_to_bean")

command = parser.parse_args().command
content = sys.stdin.read()

if command == "bean_to_json":
    json_str, *_ = bean_to_json(content)
    print(json_str)
elif command == "json_to_bean":
    bean_str, *_ = json_to_bean(json_str)
    print(bean_str)
else:
  print("command must be bean_to_json or json_to_bean")
