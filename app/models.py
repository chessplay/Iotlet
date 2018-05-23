# -*- coding:utf-8 -*-
from  app import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import  UserMixin
from app import login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),index=True,unique=True)
    email=db.Column(db.String(120),index=True,unique=True)
    password_hash=db.Column(db.String(128))
    app=db.relationship('App',backref='user',lazy='dynamic')
    tmp = db.relationship('Tmp', backref='user', lazy='dynamic')
    tmpdata = db.relationship('TmpData', backref='user', lazy='dynamic')
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    def __repr__(self):
        return '<User {}>'.format(self.username)
class App(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    appname=db.Column(db.String(20))
    description=db.Column(db.String(40))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    Appaddr=db.Column(db.String(20))
    flow=db.Column(db.Integer,default=0)
    status=db.Column(db.Integer,default=0)
    controller=db.Column(db.String(40),default="STM32")
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    devices=db.relationship('Device',backref='app',lazy='dynamic')
    datas=db.relationship('Data',backref='app',lazy='dynamic')
    def __repr__(self):
        return '<App {}>'.format(self.name)
class Device(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    devicename=db.Column(db.String(20))
    pinnames=db.Column(db.String(40))
    app_id=db.Column(db.Integer,db.ForeignKey('app.id'))
    pins=db.relationship('Pin',backref='device',lazy='dynamic')
    def __repr__(self):
        return '<Device {}>'.format(self.name)
class Data(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(40),primary_key=True)
    video_url=db.Column(db.String(40))
    img_url=db.Column(db.String(40))
    other1=db.Column(db.String(40))
    other2=db.Column(db.String(40))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    app_id=db.Column(db.Integer,db.ForeignKey('app.id'))
    def __repr__(self):
        return '<Data {}>'.format(self.name)
class Pin(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    pinname=db.Column(db.String(10))
    connections=db.Column(db.Integer)
    device_id=db.Column(db.Integer,db.ForeignKey('device.id'))
    def __repr__(self):
        return '<Pin {}>'.format(self.pinname)
class Tmp(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    appname=db.Column(db.String(40))
    serveraddr=db.Column(db.String(40))
    rtmpaddr=db.Column(db.String(40))
    controller=db.Column(db.String(40))
    module=db.Column(db.String(40))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Tmp {}>'.format(self.appname)
class TmpData(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    video_url = db.Column(db.String(80))
    img_url = db.Column(db.String(80))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '<TmpData {}>'.format(self.id)