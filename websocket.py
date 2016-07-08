from flask import Flask, render_template, request, json
from flask.ext.socketio import SocketIO, emit
import time, ConfigParser, json, ast
from threading import Thread
from utils import g_output_log, get_ip_list, get_dir_list, get_file_list, tail_file, get_port

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# celery
# from celery_app import make_celery
# app.config.update(
#     CELERY_BROKER_URL='redis://127.0.0.1:6379',
#     CELERY_RESULT_BACKEND='redis://127.0.0.1:6379'
# )
# celery = make_celery(app)

thread = None
conf = ConfigParser.ConfigParser()
conf.read("ws.conf")


@app.route('/')
def index():
	global thread
	#if thread is None:
	#thread = socketio.start_background_task(target=tailfile, file_path="/root/websocket.file")
	return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/get_ip_list', methods=['POST'])
def get_ip_list_route():
	print request.form
	ip_list = get_ip_list(conf)
	return " ".join(ip_list)

@app.route('/get_dir_list', methods=['POST'])
def get_dir_list_route():
	print request.form
	#data = json.loads(dict(request.form).popitem()[0])
	ip = dict(request.form)['ip'][0]

	#print request.json()
	#ip = data.get("ip")
	dir_list = get_dir_list(conf, ip)
	return " ".join(dir_list)

@app.route('/get_file_list', methods=['POST'])
def get_file_list_route():
	print request.form
	ip = dict(request.form)['ip'][0]
	dir_name = dict(request.form)['dir'][0]
	print ip + dir_name
	port = get_port(conf, ip)
	file_list = get_file_list(conf, ip, dir_name, port)
	print file_list
	return " ".join(file_list)

@socketio.on('my event', namespace='/test')
def test_message(message):
    #emit('my response', {'data': message['data']})
	print "message" + str(message)
	global thread
	port = get_port(conf, ip)
	tail_cmd="/usr/bin/ssh %s -p %s tail -f %s/%s" % (message['ip'], port, message['dir'], message['file'])
	thread = socketio.start_background_task(target=tail_file, tail_cmd=tail_cmd)
	global g_output_log
	while True:
		if len(g_output_log) >0:
			log = g_output_log.pop(0)
			emit('my response', {'data': log})
		else:
			time.sleep(.01)

@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
	emit('my response', {'data': message['data']}, broadcast = True)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
	socketio.run(app, host="0.0.0.0", debug=True)
