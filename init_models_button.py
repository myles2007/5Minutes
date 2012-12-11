#! /usr/bin/env python
from fiveminutes import *
from fiveminutes.models import User, Announcement, WorkItem, WorkItemComment, DailySong

if __name__ == '__main__':
    User.__table__.drop(db.engine, checkfirst=True)
    User.__table__.create(db.engine, checkfirst=True)
    Announcement.__table__.drop(db.engine, checkfirst=True)
    Announcement.__table__.create(db.engine, checkfirst=True)
    WorkItem.__table__.drop(db.engine, checkfirst=True)
    WorkItem.__table__.create(db.engine, checkfirst=True)
    WorkItemComment.__table__.drop(db.engine, checkfirst=True)
    WorkItemComment.__table__.create(db.engine, checkfirst=True)
    DailySong.__table__.drop(db.engine, checkfirst=True)
    DailySong.__table__.create(db.engine, checkfirst=True)
