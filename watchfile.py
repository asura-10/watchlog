# -*- coding: utf-8 -*-
import time, threading
from paramiko import SSHClient, AutoAddPolicy

class watchfile(threading.Thread):
    def __init__(self, ip, user, port, file_path, line_list):
        threading.Thread.__init__(self)
        print file_path
        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh.connect(ip, username = user, port = int(port))
        sftp = self.ssh.open_sftp()

        self.remote_file = sftp.open(file_path)
        self.remote_file.seek(0, 2)
        fsize = self.remote_file.tell()
        self.remote_file.seek (max (fsize-2048, 0), 0)

        self.stop_signal = 0

        self.line_list = line_list

    def __watch__(self):
        while True:
            new = self.remote_file.readline()
            # Once all lines are read this just returns ''
            # until the file changes and a new line appears

            if self.stop_signal != 0:
                break

            if new:
                yield new
            else:
                time.sleep(0.5)

    def run(self):
        for line in self.__watch__():
            if self.stop_signal != 0:
                break
            line = line.strip()
            self.line_list.append(line)
            print line

    def stop(self):
        self.stop_signal = 1
        time.sleep(0.5)
        self.ssh.close()
        
        
def test():
    line_list
    new = watchfile('127.0.0.1', 'root', 10022, '/root/test_file', line_list)
    new.start()
    print "<<<start..."
    time.sleep(3)
    new.stop()
    print line_list
    print "<<<stop."


if __name__ == "__main__":
    test()
