import os
import datetime
basedir=os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY='hard to guess string'
    SSL_DISABLE =False
    MQTT_BROKER_URL="localhost"
    MQTT_BROKER_PORT="1883"
    MQTT_USERNAME=''
    MQTT_PASSWORD=''
    MQTT_REFRESH_TIME=1.0
    MQTT_KEEPALIVE=5
    MQTT_TLS_ENABLED=False
    MQTT_LAST_WILL_TOPIC='home/lastwill'
    MQTT_LAST_WILL_MESSAGE='bye'
    MQTT_LAST_WILL_QOS=2
    TEMPLATES_AUTO_RELOAD=True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/iotbackend'
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    MAIL_SERVER=''
    MAIL_USE_SSL=True
    MAIL_USERNAME=''
    MAIN_PASSWORD=''

    SCHEDULER_API_ENABLED=True


