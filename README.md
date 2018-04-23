# i3av(ailable)

This Python3 script list keys that isn't being used by i3 as keybindings so you 
easier can find available keys.
You can limit the listing to selected modifier keys and 
specify the path to the configuration file, see [help](#help).

* [Getting started](#getting-started)
  * [Change keys to list as available](#change-keys-to-list-as-available)
  * [Change primary modifier key](#change-primary-modifier-key)
  * [Custom bindings](#custom-bindings)
* [Example](#example)
* [Help](#help)

### Getting started
````bash
# Clone this repo and go to the directory
git clone https://github.com/RasmusLindroth/i3av.git
cd i3av/

# Run the program
./i3av.py
````

#### Change keys to list as available

If you would like to change which keys that get listed you can 
edit [i3av.py](./i3av.py) and [lib/keys.py](./lib/keys.py).

In [i3av.py](./i3av.py) you have a line like this:

````Python
keys = lib.keys.getKeys(
    ["0-9", "a-z", "nordic", "arrow", "common", "function"])
````

Current possible keys are `0-9, a-z, nordic, arrow, common, uncommon, function, 
numpad, numpad_other`

If you want to add more keys, just add your keys in the dict `keys = {...}`
located in [lib/keys.py](./lib/keys.py).

#### Change primary modifier key

This script defaults to `$mod` as the modifier key. You can change this with 
adding the argument `--modvar '$m'` or change `modVariable` in [i3av.py](./i3av.py).

#### Custom bindings

If the modifiers provided isn't enough you can add your own with `--bindings`, 
e.g. `./i3av.py --bindings '$mod+Mod2' '$mod+Mod4'`. You can also change the 
code, take a look at the dict `combinations` in [i3av.py](./i3av.py).

### Example

````bash
$ ./i3av.py -m
Reading from /home/rasmus/.i3/config

Available $mod:
g, i, o, p, x, oslash, ae, BackSpace, Tab, Pause, Scroll_Lock, Escape, Delete,
Prior, Next, End, Insert, Menu, Break, comma, period, slash, semicolon,
backslash, bracketleft, bracketright, plus, equal, less, greater, apostrophe,
asterisk, grave, section, F1, F4, F6, F7, F8, F9, F10, F11, F12
````

### Help
````bash
./i3av.py --help
usage: i3av.py [-h] [--modvar MODVAR] [--config CONFIG] [-m] [-s] [-c] [-t]
               [-b BINDINGS [BINDINGS ...]]

Lists available bindings for i3.

optional arguments:
  -h, --help            show this help message and exit
  --modvar MODVAR       variable name of modkey, e.g. '$m', defaults to $mod
  --config CONFIG       path to configuration file. Otherwise it searches in
                        default locations.
  -m, --mod             available $mod bindings
  -s, --shift           available $mod+Shift bindings
  -c, --ctrl            available $mod+Ctrl bindings
  -t, --triplet         available $mod+Ctrl+Shift bindings
  -b BINDINGS [BINDINGS ...], --bindings BINDINGS [BINDINGS ...]
                        custom binding(s), e.g. '$mod+Mod2'
````
