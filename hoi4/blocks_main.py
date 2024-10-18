import json
import orjson
import argparse
from hoi4.parse import load_as_text, load_as_dict
from hoi4.blocks_parse import load_as_dict_block

parser = argparse.ArgumentParser(description="Parse HoI4 save files.")
parser.add_argument("mode", choices=["binary2plain", "hoi42json", "hoi42json_blocks"])
parser.add_argument("-i", "--input", help="The input file")
parser.add_argument("-o", "--output", help="The output file")
args = parser.parse_args()

# args = argparse.Namespace(mode="hoi42json_blocks", input="demo_my_save_file.hoi4", output="demo_my_save_file_or.json")

if args.mode == "binary2plain":
    text = load_as_text(args.input)
    with open(args.output, "w") as f:
        f.write(text)

elif args.mode == "hoi42json":
    d = load_as_dict(args.input)
    with open(args.output, "w") as f:
        json.dump(d, f, indent=4)
    
elif args.mode == "hoi42json_blocks":
    d = load_as_dict_block(args.input)
    with open(args.output, 'wb') as f:
        f.write(orjson.dumps(d, option=orjson.OPT_INDENT_2))