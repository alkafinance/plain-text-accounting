#!/usr/bin/env python3

# from beancount import loader
# from converter.entries_to_dir import entries_to_dir

# entries, errors, options = loader.load_file("./main.bean")

# entries_to_dir(entries)

from converter.from_bean import account_id_name_type_from_name

print(account_id_name_type_from_name("Assets:US:Cash"))