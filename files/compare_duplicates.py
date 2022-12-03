import argparse
from filecmp import cmp
import glob
import os
import itertools

from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="files to compare from", type=str, required=True)
parser.add_argument("-o", "--output", help="files to compare to", type=str, required=True)
parser.add_argument("-r", "--remove", help="remove file from output", type=bool, default=False)
args = parser.parse_args()

# read files
inp = glob.glob(f'{args.input}/**/*', recursive=True)
output = glob.glob(f'{args.output}/**/*', recursive=True)

inp = [f for f in inp if not os.path.isdir(f)]
output = [f for f in output if not os.path.isdir(f)]

remove_list = []
# use tqdm on all possibilites of i o
possibilities = list(itertools.product(inp, output))
total_possibilities = len(possibilities)
for i, o in tqdm(possibilities, total=total_possibilities):
    # Compare extensions
    i_ext = i.split('.')[-1]
    o_ext = o.split('.')[-1]
    if i_ext != o_ext:
        continue
    if cmp(i, o, shallow=False) and i != o:
        print(f'Found duplicate: {i} {o}')
        remove_list.append(o)

if args.remove:
    for r in remove_list:
        try:
            os.remove(r)
        except:
            pass
