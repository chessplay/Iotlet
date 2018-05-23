from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_login import  LoginManager
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from flask_apscheduler import APScheduler
from flask_mqtt import Mqtt


import json

from flask_login import current_user
#eventlet.monkey_patch()
app=Flask(__name__)
app.config.from_object(Config)
db=SQLAlchemy(app)
login=LoginManager(app)
login.login_view='login'
migrate=Migrate(app,db)
bootstrap=Bootstrap(app)

mqtt=Mqtt(app)
#socketio=SocketIO(app)
nav = Nav()
@nav.navigation()
def mynavebar():
    return Navbar(
        View('Home', 'index'),
        View('Setting', 'setting'),
        View('Logout','logout')
    )
nav.init_app(app)



#@socketio.on('publish')
#def handle_publish(json_str):
#    data=json.loads(json_str)
#    mqtt.subscribe(data['topic'])
#@mqtt.on_message()
#def handle_myqq_message(client,userdata,message):
#   data=dict(
#        topic=message.topic,
#        payload=message.payload.decode()
#    )
#    socketio.emit('mqtt_message',data=data)
#@mqtt.on_log()
#def handle_logging(client,userdata,level,buf):
 #   print(level,buf)

from app import routes,models
