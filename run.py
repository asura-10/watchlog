import time, ConfigParser
from threading import Thread
from os import system, getpid
from random import random

from flask import Flask, render_template, request, session, make_response
from flask.ext.socketio import SocketIO, emit

from utils import get_ip_list, get_dir_list, get_file_list, get_port
from cookie_ws import cookie_ws

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess secret!'
socketio = SocketIO(app)

conf = ConfigParser.ConfigParser()
conf.read("ws.conf")

cookie_ws_dic = cookie_ws()

def write_pid(f):
    pid=str(getpid())
    f=open(f, 'w')
    f.write(pid)
    f.close()

@app.route('/')
def index():
    global cookie_ws_dic

    response = make_response(render_template('index.html', async_mode=socketio.async_mode))

    cookie_ws_dic.set_cookie(request, response)

    return response

@app.route('/get_ip_list', methods=['POST'])
def get_ip_list_route():
    app.logger.debug(request.form)
    ip_list = get_ip_list(conf)
    return " ".join(ip_list)

@app.route('/get_dir_list', methods=['POST'])
def get_dir_list_route():
    app.logger.debug(request.form)
    ip = dict(request.form)['ip'][0]
    dir_list = get_dir_list(conf, ip)
    return " ".join(dir_list)

@app.route('/get_file_list', methods=['POST'])
def get_file_list_route():
    app.logger.debug(request.form)
    ip = dict(request.form)['ip'][0]
    dir_name = dict(request.form)['dir'][0]
    port = get_port(conf, ip)
    file_list = get_file_list(conf, ip, dir_name, port)
    return " ".join(file_list)

@socketio.on('my event', namespace='/test')
def test_message(message):
    global cookie_ws_dic

    sid = cookie_ws_dic.get_client_sid(request)
    cookie_ws_dic.output(request, message)

    while True:
        if cookie_ws_dic.cookie_ws_dic[sid]['stop_signal'] != 0:
            break
        if len(cookie_ws_dic.cookie_ws_dic[sid]['output']) >0:
            log = cookie_ws_dic.cookie_ws_dic[sid]['output'].pop(0)
            emit('my response', {'data': log})  
        else:
            time.sleep(.1)

@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast = True)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    global cookie_ws_dic
    sid = cookie_ws_dic.get_client_sid(request)
    cookie_ws_dic.cookie_ws_dic[sid]['stop_signal'] = 1
    time.sleep(0.5)
    cookie_ws_dic.client_pop(request)
    app.logger.debug('Client disconnected')
    app.logger.debug(cookie_ws_dic.cookie_ws_dic)

if __name__ == '__main__':
    write_pid('./run.pid')
    socketio.run(app, host="0.0.0.0", debug=True)
