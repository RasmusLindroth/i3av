#!/usr/bin/env python3

import string

# Dict of keys you can choose from
keys = {
    "0-9": [str(x) for x in range(10)],
    "a-z": [x for x in string.ascii_lowercase],
    "nordic": ["aring", "adiaeresis", "odiaeresis", "oslash", "ae"],
    "arrow": ["Left", "Up", "Right", "Down"],
    "common": ["BackSpace", "Tab", "Return", "Pause", "Scroll_Lock", "Escape",
               "Delete", "Prior", "Next", "End", "Insert", "Menu", "Break",
               "space", "comma", "period", "slash", "semicolon", "backslash",
               "bracketleft", "bracketright", "plus", "minus", "equal", "less",
               "greater", "apostrophe", "asterisk", "grave", "section"],
    "uncommon": ["Clear", "Sys_Req", "Select", "Print", "Begin", "Find",
                 "Cancel", "Help", "Execute", "Undo", "Redo"],
    "function": ["F" + str(i) for i in range(1, 13)],
    "numpad": ["KP_" + str(x) for x in range(10)],
    "numpad_other": ["KP_Space", "KP_Tab", "KP_Enter", "KP_F1", "KP_F2",
                     "KP_F3", "KP_F4", "KP_Home", "KP_Left", "KP_Up",
                     "KP_Right", "KP_Down", "KP_Prior", "KP_Next", "KP_End",
                     "KP_Begin", "KP_Insert", "KP_Delete", "KP_Equal",
                     "KP_Multiply", "KP_Add", "KP_Separator", "KP_Subtract",
                     "KP_Decimal", "KP_Divide"]
}

def getKeys(names):
    """Returns keysyms for selected keys

    :param names: a list of categories, e.g. ["0-9", "a-z", "nordic"]
    :type names: list
    :return: a list of keysyms
    :rtype: list
    """
    r = []
    for n in names:
        if n in keys:
            r += keys[n]
    return r
