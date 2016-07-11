import subprocess

g_output_log = []

def get_port(conf, ip):
    return conf.get("port", ip)

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
        get_cmd = "/usr/bin/ssh %s -p %s ls -al %s | grep -v \'^d\' | awk \'NR>1{print $NF}\'" % (ip, port, dir_name)
        print get_cmd
        popen = subprocess.Popen(['bash','-c',get_cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        line_list = popen.stdout.readlines()
        for line in line_list:
            line = line.strip()
            file_list.append(line)

    return file_list

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
