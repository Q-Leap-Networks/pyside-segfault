import re

class Autoconfig(dict):
    KEYS = ["# CPU cores", "# CPU sockets", "Size of RAM (GB)", "IB Adapter", "IPMI Adapter"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __hash__(self):
        s = ""
        for key in Autoconfig.KEYS:
            s = "{0}, {1}: {2}".format(s, key, self[key])
        return s.__hash__()

def natural_sortkey(key):
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    return [ convert(c) for c in re.split('([0-9]+)', key) ] 
