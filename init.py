#! /usr/bin/env python
from fiveminutes import *

if __name__ == '__main__':
    db.metadata.bind = db.engine
    db.metadata.reflect()
    db.metadata.drop_all()
    db.metadata.create_all()
