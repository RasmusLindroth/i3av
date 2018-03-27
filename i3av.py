#!/usr/bin/env python3

import string, re, argparse, sys, errno, os

# Return the configuration for i3 or False
def confPath():
    paths = [os.path.expanduser("~/.i3/config")]

    if "XDG_CONFIG_HOME" in os.environ:
        paths.append(os.path.expanduser(os.environ["XDG_CONFIG_HOME"] + "/i3/config"))
    else:
        paths.append(os.path.expanduser("~/.config/i3/config"))

    paths.append("/etc/i3/config")

    if "XDG_CONFIG_DIRS" in os.environ:
        paths.append(os.path.expanduser(os.environ["XDG_CONFIG_DIRS"] + "/i3/config"))
    else:
        paths.append("/etc/xdg/i3/config")

    for p in paths:
        if os.path.isfile(p) and os.access(p, os.R_OK):
            return p
    return False

# Set binary bit
def setBit(i, offset):
    return (i | 1 << offset)

# Splits keys, e.g. $mod+Shift+x and sets active keys
def splitKey(s):
    keys = [x.lower() for x in s.split("+")]

    i = 0
    if "$mod" in keys:
        i = setBit(i, 2)
    if "ctrl" in keys:
        i = setBit(i, 1)
    if "shift" in keys:
        i = setBit(i, 0)
    
    return [i] + keys

# Init argparse
parser = argparse.ArgumentParser(description="Lists available bindings for i3.")
parser.add_argument("-m", "--mod", help="available $mod bindings", action="store_true")
parser.add_argument("-s", "--shift", help="available $mod+Shift bindings", action="store_true")
parser.add_argument("-c", "--ctrl", help="available $mod+Ctrl bindings", action="store_true")
parser.add_argument("-t", "--triplet", help="available $mod+Ctrl+Shift bindings", action="store_true")
args = parser.parse_args()

# Checks if atleast one keygroup is selected, else print all
if args.mod == False and args.shift == False and args.ctrl == False and args.triplet == False:
    args.mod = True
    args.shift = True
    args.ctrl = True
    args.triplet = True

# All used combinations
# index (see splitKey(s) bit), name, offset, key (without modifiers), the whole command
combinations = {
    0: ("Other", 0, []),
    1: ("Shift", 1, []),
    2: ("Ctrl", 1, []),
    3: ("Ctrl+Shift", 2, []),
    4: ("$mod", 1, []),
    5: ("$mod+Shift", 2, []),
    6: ("$mod+Ctrl", 2, []),
    7: ("$mod+Ctrl+Shift", 3, [])
}

# Find all lines with bindsym in it and a key combination
bindKeys = re.compile("\s*?bindsym\s(.+?)\s")
keyCombinations = []
conf = confPath()

if conf == False:
    print("Error: Couldn't find or read the i3 configuration file", file=sys.stderr)
    sys.exit(errno.EINVAL)
else:
    print("Reading from " + conf)


with open(conf, "r") as f:
    for line in f:
        l = line.strip()
        # Ignore commented and empty lines
        if len(l) == 0 or l[0] == "#":
            continue
        matches = bindKeys.match(line)
        if matches:
            k = splitKey(matches.group(1))
            key = k[0]
            offset = combinations[key][1]+1
            combinations[key][2].append(k[offset])

# Keysymbols that will be listed as available if they are available
keys = []
keys += [str(x) for x in range(10)]
keys += [x for x in string.ascii_lowercase]
keys += ["aring", "adiaeresis", "odiaeresis"]
keys += ["space", "colon", "semicolon", "less", "equal", "greater", "asterisk", "plus", "comma", "minus", "period", "slash", "apostrophe"]
keys += ["left", "down", "up", "right"]
keys += ["f" + str(i) for i in range(1,13)]


# Print all available keys in a combination
def printFree(keys, comb):
    free = []
    for key in keys:
        if key not in comb[2]:
            free.append(key)
    print("\nAvailable " + comb[0] + ":")
    print(", ".join(free))

# Iterate through arguments and print if selected
for i, attr in enumerate(("mod", "shift", "ctrl", "triplet")):
    if getattr(args, attr):
        printFree(keys, combinations[i + 4])