import socket
import sys
 
receive_count = 0
import pymysql as ps	
			
def start_tcp_client(ip, port): 
	###create socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Set Timeout to 60 sec
	s.settimeout(60)

	failed_count = 0
	while True:
		try:
			print("start connect to server ")
			s.connect((ip, port))
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
		print("client TCP receive buffer size is %d" % s_receive_buffer_size)

		while True:
			print("send len is : [%d]" % len(msg))
			
			msg = s.recv(1024)
			print(msg.decode('utf-8'))
			print("recv len is : [%d]" % len(msg))

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
def clean(db,table):
	print("TODO: Clean Data")

#Analyze data
#Parameter includes database name, table name,all the parameter required...TODO
def analyze(db, table):
	#Check if data is cleaned
	print("TODO: Analyze Data")

#Validate analysis
#Parameter includes database name, table name,analysis result...TODO
def validate(db, table, analysis):
	#Check if data is analyzed
	print("TODO: Validate Data")


def create_menu():
		print("1: Data Clean(param)")
		print("2: Data Analyze(param)")
		print("3: Data Validate(param)")
		print("4: Quit")
		tmp = input()
		if tmp == 1:
			clean()
		elif tmp == 2:
			analyze()
		elif tmp == 3:
			validate()
		else:
			print("Invalid Option, Please enter your option again")
			#print("You should not be here, Report the detail how you reach this line to my lovely cat")

if __name__=='__main__':
	create_menu()
	start_tcp_client('127.0.0.1',6000)
