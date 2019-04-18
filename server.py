import socket
import sys
import struct
import pandas as pd
import pymysql
 
 
SEND_BUF_SIZE = 256
 
RECV_BUF_SIZE = 256
 
Communication_Count: int = 0
 
receive_count : int = 0

class MysqlHelper:
    def __init__(self, host = 'localhost', user = 'root', password = 'root', database = 'proj656', charset = 'utf8'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.db = None
        self.curs = None

    # connect
    def open(self):
        self.db = ps.connect(host=self.host, user=self.user, password=self.password,database=self.database, charset=self.charset)
        self.curs = self.db.cursor()

    # connect close
    def close(self):
        self.curs.close()
        self.db.close()

    # modify
    def cud(self, sql, params):
        self.open()
        try:
            self.curs.execute(sql, params)
            self.db.commit()
            print("ok")
        except:
            print('modify error')
            self.db.rollback()
        self.close()

    # search
    def find(self, sql, params):
        self.open()
        try:
            result = self.curs.execute(sql, params)
            self.close()
            results = self.curs.fetchall()
            return results
        except:
            print('find error')
 
 
def start_tcp_server(ip, port):
    # create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, port)
 
    # bind port
    print("starting listen on ip %s, port %s" % server_address)
    sock.bind(server_address)
 
    # get the old receive and send buffer size
    s_send_buffer_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    s_recv_buffer_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    print("socket send buffer size[old] is %d" % s_send_buffer_size)
    print("socket receive buffer size[old] is %d" % s_recv_buffer_size)
 
    # set a new buffer size
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SEND_BUF_SIZE)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, RECV_BUF_SIZE)
 
    # get the new buffer size
    s_send_buffer_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    s_recv_buffer_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    print("socket send buffer size[new] is %d" % s_send_buffer_size)
    print("socket receive buffer size[new] is %d" % s_recv_buffer_size)
 
    # start listening, allow only one connection
    try:
        sock.listen(1)
    except socket.error as e:
        print("fail to listen on port %s" % e)
        sys.exit(1)
    while True:
        print("waiting for connection")
        client, addr = sock.accept()
        print("having a connection")
        break
    msg = 'welcome to tcp server' + "\r\n"
    receive_count = 0
    receive_count += 1
    while True:
        print("\r\n")
        msg = client.recv(16384)
        msg_de = msg.decode('utf-8')
        print("recv len is : [%d]" % len(msg_de))
        print("###############################")
        print(msg_de)
        print("###############################")
        
        if msg_de == 'disconnect':break
 
        msg = ("hello, client, i got your msg %d times, now i will send back to you " % receive_count)
        client.send(msg.encode('utf-8'))
        receive_count += 1
        print("send len is : [%d]" % len(msg))
 
    print("finish test, close connect")
    client.close()
    sock.close() 
    print(" close client connect ")

def revert():
    #Revert from backup table

def clean():
    # 1. Create New Table called temp to store all the change 
    # 2. Peroform Data Clean
    # 3. Commit change and update table if success
    # 4. Delete temp if failed 

    mh = MysqlHelper('localhost', 'root', 'root', 'proj656', 'utf8')
    sql = "DELETE {0} FROM {0} INNER JOIN (SELECT {0}.business_id FROM {0} LEFT JOIN business ON {0}.business_id = business.id WHERE business.id IS NULL) as tmp on {0}.business_id = tmp.business_id".format('review')
    results = mh.cud(sql)



    #identify forms of consistency and sanity checking
    #determine if there are problems with portions of data using query
    #implement solution such as ignore and create new table for analysis, or adjusting analysis in order to compensate for data skew(long tail of data distribution)
    #parameter should include threshold and identified by client
    if False: # not as expected 
        mh.db.rollback()
        revert()



#Analyze Data include detailed and careful study of particular things 
def analyze():
    #decision tree classifier
    # a priori algo
    #using sql
    #Minimized return to Client, only the result
    print("TODO")

def validate():
    #divide data into two at random.
    #first half would be used to analysis and predict for the oter half
    #The other half would be used to validate or refute hypothesis
    #return should be validated or not, probably with some reason

 
 
 
if __name__=='__main__':
    start_tcp_server('127.0.0.1',6000)