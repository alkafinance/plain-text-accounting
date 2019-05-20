#!/usr/bin/env python3

from beancount import loader
from converter.entries_to_dir import entries_to_dir

entries, errors, options = loader.load_file("./main.bean")

entries_to_dir(entries)