#! /usr/bin/env python
from datetime import datetime
from fiveminutes import db
from mixin import OurMixin, uuid

class User(OurMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.CHAR(length=36), default=uuid, primary_key=True)
    instances = db.relationship("Instance", backref="user")
    name = db.Column(db.String(60))
    email = db.Column(db.String(200))
    openid = db.Column(db.String(200))

    def __init__(self, name, email, openid):
        self.name = name
        self.email = email
        self.openid = openid

    def __repr__(self):
        return "User: {0} - {1}".format(self.id, self.email)

class Follower(OurMixin, db.Model):
    __tablename__ = 'followers'
    id = db.Column(db.CHAR(length=36), default=uuid, primary_key=True)
    who_id = db.Column(db.Integer())
    whom_id = db.Column(db.Integer())

    def __repr__(self):
        return "User: {0} - {1}".format(self.id, self.email)

class Message(OurMixin, db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.CHAR(length=36), default=uuid, primary_key=True)
    user_id = db.Column(db.CHAR(length=36), db.ForeignKey('users.id' ), nullable=False)
    text = db.Column(db.String())
    created_on = db.Column(db.DATETIME(), nullable=False, default=datetime.now)
    sticky = db.Column(db.Boolean(), default=False, server_default='0')

    def __repr__(self):
        return "User: {0} - {1}".format(self.id, self.email)

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
        return "User: {0} - {1}".format(self.id, self.email)
