import json
import os
import shelve
from pathlib import Path


shelf_dir = Path(os.path.expanduser('~/.nginx-lm'))

if not shelf_dir.is_dir():
    shelf_dir.mkdir()

shelf = shelve.open(os.path.expanduser('~/.nginx-lm/config'))


def main(args):
    for key, val in args.__dict__.items():
        shelf[key] = val
    shelf.sync()
