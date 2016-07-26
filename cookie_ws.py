from utils import uniq_num, get_port
#from cmd_bind import cmd_bind
from watchfile import watchfile
import time, ConfigParser

conf = ConfigParser.ConfigParser()
conf.read("ws.conf")

class cookie_ws():
    def __init__(self):
        self.cookie_ws_dic = {}

    def set_cookie(self, request, response):
        sid = uniq_num()
        response.set_cookie('sid', sid)
        self.cookie_ws_dic[sid] = {}
        self.cookie_ws_dic[sid]['start_time'] = time.time()
        self.cookie_ws_dic[sid]['stop_signal'] = 0

        print self.cookie_ws_dic

        if len(self.cookie_ws_dic) > 10:
            for i in self.cookie_ws_dic:
                if int(time.time() - i['start_time']) > 36000:
                    self.cookie_ws_dic.pop[i]

        return response

    def client_exists(self, request):
        if request.cookies.get("sid") is not None:
            return True
        else:
            return False

    def client_pop(self, request):
        sid = self.get_client_sid(request)
        if self.get_client_cmd(request):
            self.cookie_ws_dic[sid]["cmd"].stop()

        self.cookie_ws_dic.pop(sid)
        
    def output(self, request, message):
        sid = self.get_client_sid(request)
        port = get_port(conf, message['ip'])
        file_path = message['dir'] + "/" +  message['file']
        tail_cmd="/usr/bin/ssh %s -p %s tail -f %s/%s" % (message['ip'], port, message['dir'], message['file'])

        if not self.cookie_ws_dic[sid].has_key('output'):
            self.cookie_ws_dic[sid]['output'] = []
        if not self.cookie_ws_dic[sid].has_key('cmd'):
            self.cookie_ws_dic[sid]['cmd'] = watchfile(message['ip'], 'root', port, file_path, self.cookie_ws_dic[sid]['output'])
            self.cookie_ws_dic[sid]['cmd'].start()

    def get_client_sid(self, request):
        sid = request.cookies.get("sid")
        if self.cookie_ws_dic.has_key(sid):
            return sid
        else:
            return False

    def get_client_cmd(self, request):
        sid = request.cookies.get("sid")
        if self.cookie_ws_dic[sid].has_key("cmd"):
            return True
        else:
            return False


def test():
    a = cookie_ws()
    print a.cookie_ws_dic
        
if __name__ == '__main__':
    test()    
