#! /usr/bin/env python
from fiveminutes import *
from fiveminutes.models import User, Announcement, WorkItem, WorkItemComment, DailySong

if __name__ == '__main__':
    db.metadata.bind = db.engine
    db.metadata.reflect()
    db.metadata.drop_all()
    db.metadata.create_all()
