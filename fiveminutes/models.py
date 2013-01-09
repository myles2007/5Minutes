#! /usr/bin/env python
from datetime import datetime
from fiveminutes import db, WORK_ITEM_TYPES
from mixin import OurMixin, uuid

class User(OurMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.CHAR(length=36), default=uuid, primary_key=True)
    announcements = db.relationship("Announcement", backref="user")
    work_items = db.relationship("WorkItem", backref="user")
    name = db.Column(db.String(60))
    email = db.Column(db.String(200))
    openid = db.Column(db.String(200))
    group = db.Column(db.String(60))
    super_user = db.Column(db.Boolean(), default=False, server_default='0')

    def __repr__(self):
        return "User: {0} - {1}".format(self.id, self.email)


class Announcement(OurMixin, db.Model):
    __tablename__ = 'announcements'

    id = db.Column(db.CHAR(length=36), default=uuid, primary_key=True)
    user_id = db.Column(db.CHAR(length=36), db.ForeignKey('users.id' ), nullable=False)
    # Text is stored markdown text that is rendered before being displayed on the screen.
    text = db.Column(db.String())
    created_on = db.Column(db.DATETIME(), nullable=False, default=datetime.now)

    def __repr__(self):
        return "Announcement: {}".format(self.id)


class Iteration(OurMixin, db.Model):
    __tablename__ = 'iterations'

    id = db.Column(db.CHAR(length=36), default=uuid, primary_key=True)
    work_items = db.relationship("WorkItem", backref="iteration")
    title = db.Column(db.String())
    completed = db.Column(db.Boolean(), default=False, server_default='0')
    created_on = db.Column(db.DATETIME(), nullable=False, default=datetime.now)
    completed_on = db.Column(db.DATETIME())

    def __repr__(self):
        return "Iteration: {0} - {1}".format(self.id, self.title)


class WorkItem(OurMixin, db.Model):
    __tablename__ = 'work_items'

    id = db.Column(db.CHAR(length=36), default=uuid, primary_key=True)
    comments = db.relationship("WorkItemComment", backref="work_item")
    user_id = db.Column(db.CHAR(length=36), db.ForeignKey('users.id' ), nullable=False)
    iteration_id = db.Column(db.CHAR(length=36), db.ForeignKey('iterations.id' ), nullable=False)
    title = db.Column(db.String())
    # Summary is stored markdown text that is rendered before being displayed on the screen.
    summary = db.Column(db.String())
    type = db.Column(db.Enum(*WORK_ITEM_TYPES), nullable=False)
    iteration_sort_order = db.Column(db.Integer(), server_default='0', default=0)
    queue_sort_order = db.Column(db.Integer(), server_default='0', default=0)
    completed = db.Column(db.Boolean(), default=False, server_default='0')
    created_on = db.Column(db.DATETIME(), nullable=False, default=datetime.now)
    completed_on = db.Column(db.DATETIME())

    def __repr__(self):
        return "WorkItem: {0} - {1}".format(self.id, self.title)


class WorkItemComment(OurMixin, db.Model):
    __tablename__ = 'work_item_comments'

    id = db.Column(db.CHAR(length=36), default=uuid, primary_key=True)
    work_item_id = db.Column(db.CHAR(length=36), db.ForeignKey('work_items.id' ), nullable=False)
    # Text is stored markdown text that is rendered before being displayed on the screen.
    text = db.Column(db.String())
    created_on = db.Column(db.DATETIME(), nullable=False, default=datetime.now)

    def __repr__(self):
        return "Comment: {}".format(self.id)


class DailySong(OurMixin, db.Model):
    __tablename__ = 'daily_songs'

    id = db.Column(db.CHAR(length=36), default=uuid, primary_key=True)
    created_on = db.Column(db.DATETIME(), nullable=False, default=datetime.now)
    track_uri = db.Column(db.String())
    artist_uri = db.Column(db.String())
    album_uri = db.Column(db.String())
    track_name = db.Column(db.String())
    artist_name = db.Column(db.String())
    album_name = db.Column(db.String())

    def __repr__(self):
        return "DailySong: {0} - {1}".format(self.id, self.track_name)
