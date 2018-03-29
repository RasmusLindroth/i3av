#!/usr/bin/env python3

import sys
import errno
import argparse
import string
import lib.config as config
import lib.keys

# Hardcoded default variable for the primary modifier key,
# can be changed with --modvar
modVariable = "$mod"

# The keys that will be listed as available
keys = lib.keys.getKeys(
    ["0-9", "a-z", "nordic", "arrow", "common", "function"])

def printAvailable(modifier, available):
    """Prints available keys and their modifiers

    :param modifier: list of modifiers
    :type modifier: dict
    :param available: list of available keys, see lib.config.Config.availableBindings()
    :type available: list
    """

    mods = "+".join([m for m in modifier])
    print("\nAvailable " + mods + ":")
    print(", ".join(available))

# Init argparse
parser = argparse.ArgumentParser(
    description="Lists available bindings for i3.")
parser.add_argument(
    "--modvar", help="variable name of modkey, e.g. '$m', defaults to $mod", type=str)
parser.add_argument(
    "--config", help="path to configuration file. Otherwise it searches in default locations.", type=str)
parser.add_argument(
    "-m", "--mod", help="available $mod bindings", action="store_true")
parser.add_argument(
    "-s", "--shift", help="available $mod+Shift bindings", action="store_true")
parser.add_argument(
    "-c", "--ctrl", help="available $mod+Ctrl bindings", action="store_true")
parser.add_argument(
    "-t", "--triplet", help="available $mod+Ctrl+Shift bindings", action="store_true")
parser.add_argument(
    "-b", "--bindings", help="custom binding(s), e.g. '$mod+Mod2'", type=str, nargs='+')
args = parser.parse_args()

# Turple with args that will be iterated
boolArgs = ("mod", "shift", "ctrl", "triplet")

# If --modvar is set change the default modifier
if args.modvar:
    modVariable = args.modvar

combinations = {
    "mod": [modVariable],
    "shift": [modVariable, "Shift"],
    "ctrl": [modVariable, "Ctrl"],
    "triplet": [modVariable, "Ctrl", "Shift"],
}

# Adds custom binding(s)
if args.bindings:
    for i, b in enumerate(args.bindings):
        combinations["binding_"+str(i)] = b.split("+")

# Use user selected config else search defaults
if args.config:
    conf = config.Path(args.config)
    if conf.exists == False:
        print("Error: Couldn't find or read the i3 configuration file", file=sys.stderr)
        sys.exit(errno.ENOENT)
else:
    configs = [
        config.Path("~/.i3/config"),
        config.Path("/i3/config", "XDG_CONFIG_HOME"),
        config.Path("~/.config/i3/config"),
        config.Path("/etc/i3/config"),
        config.Path("/i3/config", "XDG_CONFIG_DIRS"),
        config.Path("/etc/xdg/i3/config"),
    ]
    conf = None
    for c in configs:
        if c.exists:
            conf = c
            break
    if conf == None:
        print("Error: Couldn't find or read any i3 configuration file", file=sys.stderr)
        sys.exit(errno.ENOENT)

print("Reading from " + conf.path)
c = config.Config(conf.path)

# Checks if atleast one keygroup is selected, else all True
if not args.bindings and not any([getattr(args, x) for x in boolArgs]):
    for attr in combinations:
        setattr(args, attr, True)

# Iterate through arguments and print if selected
for attr in combinations:
    # Skip combinations that isn't selected by the user
    if attr in args and not getattr(args, attr):
        continue
    available = c.availableBindings(keys, combinations[attr])
    printAvailable(combinations[attr], available)
