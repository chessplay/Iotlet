
import datetime
from app import app
from flask_apscheduler import APScheduler
import cv2
import logging
import time
import numpy as np

if __name__=='__main__':
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='0.0.0.0',port='5000',debug=True,threaded=True)