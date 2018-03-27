# i3av(ailable)

This script list keys that isn't being used by i3 as keybindings so you 
easier can find available keys.
You can limit the listing to selected modifier keys, see [help](#help).

#### Example

````bash
$ ./i3av.py -m                                                                                                                                                                                                   
Reading from /home/rasmus/.i3/config

Available $mod:
g, i, m, o, p, x, colon, semicolon, less, equal, greater, asterisk, plus, comma, period, slash, apostrophe, f1, f4, f6, f7, f8, f9, f10, f11, f12
````

#### Help
````bash
usage: i3av.py [-h] [-m] [-s] [-c] [-t]

Lists available bindings for i3

optional arguments:
  -h, --help     show this help message and exit
  -m, --mod      available $mod bindings
  -s, --shift    available $mod+Shift bindings
  -c, --ctrl     available $mod+Ctrl bindings
  -t, --triplet  available $mod+Ctrl+Shift bindings
````