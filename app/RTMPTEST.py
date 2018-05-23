import librtmp
import cv2
import subprocess as sp
camera = cv2.VideoCapture("/home/zlw/91369.mp4")
command=[
    'ffmpeg',
    '-re',
    '-y',
    '-f','rawvideo',
    '-vcodec','rawvideo',
    '-pix_fmt','bgr24',
    '-s','1280*720',
    '-i','-',
    '-an',
    '-r','500',
    '-c:v','libx264',
    '-pix_fmt','yuv420p',
    '-preset','ultrafast',
    '-f','flv',
    'rtmp://localhost:1935/live/film'
    ]
if not camera.isOpened():
    raise RuntimeError('Could not start camera.')
else:
    proc = sp.Popen(command, stdin=sp.PIPE, shell=False)
    count=0

    while True:
            # read current frame
        count=count+1
        _, img = camera.read()
        print img.shape

            # encode as a jpeg image and return it
           # yield cv2.imencode('.jpg', img)[1].tobytes()
        if count%5==0:
            proc.stdin.write(img.tostring())
#conn=librtmp.RTMP("rtmp://localhost:1935/live/film",live=True)
#conn.connect()
#stream=conn.create_stream()
#conn_r=librtmp.RTMP("rtmp://live.hkstv.hk.lxdns.com/live/hks",live=True)
#conn_r.connect()
#stream_r=conn_r.create_stream()




