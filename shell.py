#!/usr/bin/env python
from fiveminutes import *
from fiveminutes.models import *
from fiveminutes.mixin import *
from flask import *

try:
    from IPython import embed
    embed()
except ImportError:
    import os
    import readline
    from pprint import pprint
    os.environ['PYTHONINSPECT'] = 'True'
