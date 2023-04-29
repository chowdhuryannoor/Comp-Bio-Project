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
        runtime = output.decode().split()[0]
        match = re.search(PATTERN, output.decode())
        if match:
            outname_time = NAMES[IMPORTS.index(i)] + "_runtime.csv"
            outname_ram = NAMES[IMPORTS.index(i)] + "_ram_usage.csv"

            outpath_ram = outpath.joinpath(outname_ram)
            outpath_time = outpath.joinpath(outname_time)

            # File format: (size in mB, ram usage in kB)
            with open(outpath_ram, 'a') as outfile:
                outfile.write(sys.argv[3] + "," + match.group(1) + "\n")

            # File format: (size in mB, time in seconds)
            with open(outpath_time, 'a') as outfile:
                outfile.write(sys.argv[3] + "," + runtime + "\n")
        break

if __name__ == "__main__":
    main()