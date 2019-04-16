import socket
import sys
 
receive_count = 0
import pymysql as ps

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
        except :
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
			
			
def start_tcp_client(ip,port): 
	###create socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	failed_count = 0
	while True:
		try:
			print("start connect to server ")
			s.connect((ip,port))
			break
		except socket.error:
			failed_count += 1
			print("fail to connect to server %d times" % failed_count)
			if failed_count == 100: return

	# send and receive
	while True:
		print("connect success")

		#get the socket send buffer size and receive buffer size
		s_send_buffer_size = s.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
		s_receive_buffer_size = s.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)

		print("client TCP send buffer size is %d" % s_send_buffer_size)
		print("client TCP receive buffer size is %d" %s_receive_buffer_size)

		receive_count = 0
		while True:
			msg = 'hello server, i am the client'
			s.send(msg.encode('utf-8'))
			print("send len is : [%d]" % len(msg))
			
			msg = s.recv(1024)
			print(msg.decode('utf-8'))
			print("recv len is : [%d]" % len(msg))

			receive_count+= 1

			if receive_count==14:
				msg = 'disconnect'
				print("total send times is : %d " % receive_count)
				s.send(msg.encode('utf-8'))
				break
		break
 
        s.close()

def add():
	mh = MysqlHelper('localhost', 'root', 'root', 'proj656', 'utf8')
	sql = "insert into courses(title) values(%s)"
	mh.cud(sql, ('test1'))
	
def find():
	mh = MysqlHelper('localhost', 'root', 'root', 'proj656', 'utf8')
	sql = "select * from courses where title=%s"
	print(mh.find(sql, 'test1'))

#Clean Data
#Parameter includes database name, table name,all the parameter required...TODO
def clean(db = 'proj656', table):
	print("TODO: Clean Data")

#Analyze data
#Parameter includes database name, table name,all the parameter required...TODO
def analyze(db = 'proj656', table):
	print("TODO: Analyze Data")

#Validate analysis
#Parameter includes database name, table name,analysis result...TODO
def validate(db = 'proj656', table, analysis):
	print("TODO: Validate Data")


def create_menu():
		print "1: modify"
		print "2: search"
		print "3: quit"
		input = raw_input()
		if input == "1":
			add()
		elif input == "2":
			find()
if __name__=='__main__':
	create_menu()
	start_tcp_client('127.0.0.1',6000)
