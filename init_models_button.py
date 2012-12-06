#! /usr/bin/env python
from fiveminutes import *
from fiveminutes.models import User, Follower, Message, DailySong

if __name__ == '__main__':
    User.__table__.drop(db.engine, checkfirst=True)
    User.__table__.create(db.engine, checkfirst=True)
    Follower.__table__.drop(db.engine, checkfirst=True)
    Follower.__table__.create(db.engine, checkfirst=True)
    Message.__table__.drop(db.engine, checkfirst=True)
    Message.__table__.create(db.engine, checkfirst=True)
    DailySong.__table__.drop(db.engine, checkfirst=True)
    DailySong.__table__.create(db.engine, checkfirst=True)
