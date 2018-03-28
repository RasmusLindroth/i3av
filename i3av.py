#!/usr/bin/env python3

import sys
import errno
import argparse
import string
import lib.config as config
import lib.keys

# The keys that will be listed as available
keys = lib.keys.getKeys(
    ["0-9", "a-z", "nordic", "arrow", "common", "function"])


def getCombo(active):
    """Set active modifiers. Used in lib.config.Config.availableBindings

    :param active: list of modifiers to activate, e.g. ["$mod"]
    :type active: list
    :return: dictionary of active modifiers
    :rtype: dict
    """

    modifiers = {
        "$mod": False,
        "Ctrl": False,
        "Shift": False,
        "Mod1": False,
        "Mod2": False,
        "Mod3": False,
        "Mod4": False,
        "Mod5": False
    }
    for k in active:
        if k in modifiers:
            modifiers[k] = True
    return modifiers


def printAvailable(modifier, available):
    """Prints available keys and their modifiers

    :param modifier: list of modifiers, see getCombo()
    :type modifier: dict
    :param available: list of available keys, see lib.config.Config.availableBindings()
    :type available: list
    """

    mods = "+".join([m for m in modifier if modifier[m]])
    print("\nAvailable " + mods + ":")
    print(", ".join(available))


combinations = {
    "mod": getCombo(["$mod"]),
    "shift": getCombo(["$mod", "Shift"]),
    "ctrl": getCombo(["$mod", "Ctrl"]),
    "triplet": getCombo(["$mod", "Ctrl", "Shift"]),
}

# Init argparse
parser = argparse.ArgumentParser(
    description="Lists available bindings for i3.")
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
args = parser.parse_args()

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
if not any([getattr(args, x) for x in combinations]):
    for attr in combinations:
        setattr(args, attr, True)

# Iterate through arguments and print if selected
for attr in combinations:
    if getattr(args, attr):
        available = c.availableBindings(keys, combinations[attr])
        printAvailable(combinations[attr], available)
