#!/usr/bin/env python3

import os
import re
import subprocess
import sys


def getKeyCodes():
    """Get keycodes from xmodmap with the corresponding keysym

    :return: A dictionary with keycode as key and keysym as value
    :rtype: dict or False
    """

    keycodes = {}
    reKeycode = re.compile(
        r"^keycode\s*(\d+?)\s*=\s*(?:NoSymbol\s?)*(.+?)(?:\s+|$)")
    try:
        ls = subprocess.Popen(['xmodmap', '-pke'], stdout=subprocess.PIPE)
        for line in ls.stdout:
            l = line.decode().strip()
            matches = reKeycode.match(l)

            if matches:
                keycodes[matches.group(1)] = matches.group(2)
    except FileNotFoundError:
        print("Warning: Could't call xmodmap. Keycodes will not be mapped to keysyms.")
        return False
    return keycodes


class Path:
    """Holds a path to an i3 configuration file and checks if it exists
    """

    def __init__(self, path, env=""):
        """Init path

        :param path: path to i3 config
        :type path: str
        :param env: environment variable that prepends path e.g. "XDG_CONFIG_HOME", defaults to ""
        :param env: str, optional
        """

        if env == "":
            self.path = self.getPath(path)
            self.exists = self.checkPath()
        elif env != "" and env in os.environ:
            self.path = self.getPath(os.environ[env] + path)
            self.exists = self.checkPath()
        else:
            self.path = None
            self.exists = False

    def getPath(self, path):
        """Expands tilde to home path

        :param path: path to config
        :type path: str
        :return: expanded path
        :rtype: str
        """
        return os.path.expanduser(path)

    def checkPath(self):
        """Check if the file exists and if we can read it

        :return: bool
        :rtype: bool
        """

        if os.path.isfile(self.path) and os.access(self.path, os.R_OK):
            return True
        return False


class Config:
    """Holds a configuration file and the keybindings in it
    """

    def __init__(self, path):
        """Init config

        :param path: path to configuration file
        :type path: str
        """

        self.path = path
        self.bindings = self.getBindings()

    def getBindings(self):
        """Gets keybindings from configuration file

        :return: a list of keybindings
        :rtype: [Binding, ...]
        """

        bindings = []
        reBinding = re.compile(r"^bind(sym|code)\s(.+?)\s")

        with open(self.path, "r") as f:
            for line in f:
                l = line.strip()
                matches = reBinding.match(l)
                if matches:
                    bindings.append(
                        Binding(
                            matches.group(1), matches.group(2)
                        )
                    )
        return bindings

    def availableBindings(self, keys, combination):
        """Check which keybindings that aren't used for selected modifiers

        :param keys: list of keys e.g. ["a","1","Escape"]
        :type keys: list
        :param combination: dict of modifiers to compare with
        :type combination: dict
        :return: a list of available keybindings, bindings that isn't used
        :rtype: list
        """

        used = [x.sym.lower()
                for x in self.bindings if x.modifiers == combination and x.sym != None]
        return [x for x in keys if x.lower() not in used]


class Binding:
    """Holds a keybinding
    """

    def __init__(self, bindtype, keys):
        """Init Binding

        :param bindtype: either sym or code
        :type bindtype: str
        :param keys: string of keys, e.g. "$mod+Shift+a"
        :type keys: str
        """

        self.type = bindtype
        self.sym = None
        self.code = None

        self.modifiers = {
            "$mod": False,
            "Ctrl": False,
            "Shift": False,
            "Mod1": False,
            "Mod2": False,
            "Mod3": False,
            "Mod4": False,
            "Mod5": False
        }
        self.keys = self.splitKeys(keys)
        self.setModifiers()

        if self.type == "sym":
            self.sym = self.keys[-1]
        elif self.type == "code":
            self.code = self.keys[-1]
            self.sym = self.getKeySym(self.code)

    def splitKeys(self, keys):
        """Splits a string of keys to a list

        :param keys: string of keys, e.g. "$mod+Shift+a"
        :type keys: str
        :return: returns a list of keys, e.g. ["$mod", "Shift", "a"]
        :rtype: list
        """

        return [x for x in keys.split("+")]

    def setModifiers(self):
        """Sets all modifiers in use to True
        """

        modifiers = self.modifiers.keys()
        for k in self.keys:
            if k.lower().capitalize() in modifiers:
                self.modifiers[k] = True

    def getKeySym(self, code):
        """Keycode to keysym

        :param code: Keycode
        :type code: str
        :return: Keysym
        :rtype: str or None
        """

        if keycodes != False and code in keycodes:
            return keycodes[code]
        else:
            return None

    def __str__(self):
        """String representation of object

        :return: a string of the keybinding
        :rtype: str
        """

        v = []
        for m in self.modifiers:
            if self.modifiers[m]:
                v.append(m)
        v.append(self.sym or "(code " + self.code + ")")
        return "+".join(v)


keycodes = getKeyCodes()
