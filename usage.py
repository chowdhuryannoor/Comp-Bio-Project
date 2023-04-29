import sys
import subprocess
import re
import math
from pathlib import Path

NAMES = ["naive", "original_ukkonen", "sa_lcp", "sl_ukkonen"]
TRACKING = ["/usr/bin/time", "-v", "python", "-c"]
IMPORTS = ["import " + func + "; " + func + ".runtime('{}')" for func in NAMES]
PATTERN = r"Maximum resident set size \(kbytes\): (\d+)"

def main():
    inpath = sys.argv[1]
    outpath = Path(sys.argv[2])
    characters = math.floor(float(sys.argv[3]) * 1000000)
    with open(inpath, 'r') as infile:
        text = ''.join(infile.read().split()).strip()
        text = text[0:characters] + "$"
    for i in IMPORTS:
        command = TRACKING + [i.format(text)]
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=False)
        match = re.search(PATTERN, output.decode())
        if match:
            outname = NAMES[IMPORTS.index(i)] + "_ram_usage.csv"
            outpath = outpath.joinpath(outname)
            with open(outpath, 'a') as outfile:
                outfile.write(sys.argv[3] + "," + match.group(1) + "\n")

if __name__ == "__main__":
    main()