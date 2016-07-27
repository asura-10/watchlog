import subprocess, time, ConfigParser
from random import random
from paramiko import SSHClient, AutoAddPolicy

conf = ConfigParser.ConfigParser()
conf.read("ws.conf")

def list_sort(liststring):
    listtemp = [(x.lower(),x) for x in liststring]
    listtemp.sort()

    return [x[1] for x in listtemp]

def uniq_num():
    pre = str(int(time.time() * 1000000))
    last = str(int(random() * 10000000000000000))
    return pre + last

def get_port(conf, ip):
    return conf.get("port", ip)

def get_user(conf, ip):
    return conf.get("user", ip)

def get_ip_list(conf):
    options = conf.options("file")
    return options

def get_dir_list(conf, ip):
    options = conf.options("file")
    if ip in options:
        return conf.get("file", ip).split('|')
    else:
        return False

def get_file_list(conf, ip, dir_name, port):
    options = conf.options("file")
    file_list = []
    if ip in options:
        dir_list = conf.get("file", ip).split('|')

    if dir_name in dir_list:
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(ip, username = get_user(conf, ip), port = int(port))
        return list_sort(ssh.open_sftp().listdir(dir_name))

def tail_file(tail_cmd):
    global g_output_log
    popen = subprocess.Popen(['bash','-c',tail_cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pid = popen.pid
    print('Popen.pid:'+str(pid))
    while True:
        line=popen.stdout.readline().strip()
        print "output:%s" %(line)
        g_output_log.append(line)
        if subprocess.Popen.poll(popen) is not None:
            break
    print('DONE')

