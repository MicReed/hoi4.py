
#TODO Anki
"""
1. what moddul to use to define a command-line argument for a script
2. how to see the help message for a script
3. how to add a argument option
#A
1. argparse
2. python tempt.py -h
3. parser.add_argument("filename", help="The name of the file to process")
e.g.
``` python
import argparse

parser = argparse.ArgumentParser(description="Process a file with optional verbosity.")
parser.add_argument("filename", help="The name of the file to process")
# -v, or --verbosity
parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2], help="Increase output verbosity")

args = parser.parse_args()

print(f"Filename: {args.filename}")
print(f"Verbosity: {args.verbosity}")
```
"""



import argparse

parser = argparse.ArgumentParser(description="Process a file with optional verbosity.")
parser.add_argument("filename", help="The name of the file to process")
parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2], help="Increase output verbosity")

args = parser.parse_args()

print(f"Filename: {args.filename}")
print(f"Verbosity: {args.verbosity}")
