from app import app,db
from flask import flash,url_for,redirect,render_template,session,request,abort,Response
from flask_login import current_user,login_user,login_required,logout_user
from forms import LoginForm,RegisterForm,SettingForm
from models import User,Device,Tmp,TmpData
from werkzeug.urls import url_parse
import cv2
from camera_opencv import Camera
import librtmp
from flask_apscheduler import APScheduler
import logging
import numpy as np
import datetime
import time
import os

from flask_mqtt import  Mqtt
from flask import current_app
from app import mqtt
basedir ="app/static/data"
logging.basicConfig()
def jobfromparm(jobargs):
    id = jobargs['id']
    func = jobargs['func']
    args = jobargs['args']
    print(args)
    trigger = jobargs['trigger']
    seconds = jobargs['seconds']

    print('add job: ',id)
    sche=current_app.apscheduler
    job = sche.add_job(func=__name__+":"+func,id=id, args=args,trigger=trigger,seconds=seconds,replace_existing=True)
    return 'sucess'
@login_required
@app.route('/pause')
def pausejob():
    sche = current_app.apscheduler
    sche.pause_job(str(current_user.id))
    return "Success!"
@login_required
@app.route('/resume')
def resumejob():
    sche = current_app.apscheduler
    sche.resume_job(str(current_user.id))
    return "Success!"
@login_required
@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
    arg=(current_user.id,)

    data = {
        "id":str(current_user.id),
        "func":"save_movie",
        "args":arg,
        "trigger":"interval",
        "seconds":60
    }
    job = jobfromparm(data)
    return "OK"


def save_movie(a):
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]

    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe('./MobileNetSSD_deploy.prototxt.txt', "./MobileNetSSD_deploy.caffemodel")
    print(a)
    #print(current_user.id)
    tmp = Tmp.query.filter_by(user_id=a).first()
    print(tmp.rtmpaddr)

    if tmp is  None:
        print(tmp.rtmpaddr)
    videoCapture=cv2.VideoCapture(tmp.rtmpaddr)


    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    if not os.path.exists(os.path.join(basedir,str(a))):
        #os.mkdir(basedir)
        os.mkdir(os.path.join(basedir,str(a)))
    if not os.path.exists(os.path.join(basedir,str(a),'video')):
        os.mkdir(os.path.join(basedir,str(a), 'video'))
    if not os.path.exists(os.path.join(basedir, str(a), 'img')):
        os.mkdir(os.path.join(basedir,str(a), 'img'))


    filename=str(datetime.datetime.utcnow())+".mp4"
    filename=filename.replace(' ','')
    print(filename)
    videoWriter = cv2.VideoWriter(os.path.join(basedir,str(a),'video',filename), cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size)
    time_start=time.time()
    success, img = videoCapture.read()

    imgname=str(datetime.datetime.utcnow())+".jpg"
    imgname=imgname.replace(' ','')

    cv2.imwrite(os.path.join(basedir,str(a),'img',imgname),img)
    print(os.path.join(basedir,str(a),'img',imgname))
    tmpData = TmpData(img_url=os.path.join("/static/data",str(a),'img',imgname),video_url=os.path.join("/static/data",str(a),'video',filename),user_id=a)
    db.session.add(tmpData)
    db.session.commit()
    flag=False
    while success:
        videoWriter.write(img)
        success, img = videoCapture.read()
        img = cv2.resize(img, (300, 300))
        (h, w) = img.shape[:2]
        blob = cv2.dnn.blobFromImage(img, 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()
        if flag==True:

            videoWriter.write(cv2.resize(img,(size[0],size[1])))
            isfind=False
            for i in np.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.2:
                    isfind=True
            time_end=time.time()
            if (time_end-time_start)>60:
                return
        else:
            for i in np.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.2:
                    idx = int(detections[0, 0, i, 1])
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                    print("[INFO] {}".format(label))
                    cv2.rectangle(img, (startX, startY), (endX, endY), COLORS[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(img, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                    flag=True
                videoWriter.write(cv2.resize(img, (size[0], size[1])))


    print("I am working:%s" %(datetime.datetime.utcnow()))
    return "ok"


@app.route('/')
@app.route('/index')
@login_required
def index():
    form = SettingForm()
    datas=TmpData.query.filter_by(user_id=current_user.id).all()
    print(datas)

    return render_template('index.html',form=form,data=datas)
@app.route('/details',methods=['GET','POST'])
def details():
    return render_template('details.html')
@app.route('/setting',methods=['GET','POST'])
def setting():
    form=SettingForm()
    print(request.args)
    if request.method=='POST':
        appname = request.form.get('appname')
        serveraddr = request.form.get('serveraddr')
        rtmpaddr = request.form.get('rtmpaddr')
        controller = request.form.get('controller')
        module = request.form.get('module')
        tmp = Tmp.query.filter_by(user_id=current_user.id).first()
        if tmp is None:
            device=Tmp(user_id=current_user.id,appname=appname,serveraddr=serveraddr,rtmpaddr=rtmpaddr,controller=controller,module=module)
            db.session.add(device)
            db.session.commit()
        else:
            tmp.appname=appname
            tmp.serveraddr=serveraddr
            tmp.rtmpaddr=rtmpaddr
            tmp.controller=controller
            tmp.module=module
            db.session.commit()
    data = [{
        'username', 'abc',
        'age', 18
    }, {
        'username', 'abc',
        'age', 18
    },
        {
            'username', 'abc',
            'age', 18
        }
    ]
    return render_template('index.html', form=form, data=data)
def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/video_feed',methods=['GET','POST'])
@login_required
def video_feed():
    print('i am called')
    #source="rtmp://localhost:1935/live/film"

    camera=Camera()
    tmp = Tmp.query.filter_by(user_id=current_user.id).first()
    camera.set_video_source(tmp.rtmpaddr)
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/command')
@login_required
def command():
   command=request.args.get('command')
   print(command)
   print(current_user.id)
   tmp=Tmp.query.filter_by(user_id=current_user.id).first()

   mqtt.publish(str(current_user.id)+"/"+tmp.controller, command, 1)
   return "OK"

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    print('----')
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',form=form)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return  redirect(url_for('index'))
    form=RegisterForm()
    if form.validate_on_submit():
        user=User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations,you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/data',methods=['GET'])
def data():
    name="visiter"
    username=request.args.get('username')
    password=request.args.get('password')
    user=User(username=username,password=password)
    db.session.add(user)
    db.session.commit()
    return render_template("404.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500
