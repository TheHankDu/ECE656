import socket
import sys
import time
			
isClean = False
isAnalyzed = False

def start_tcp_client(ip, port): 
	###create socket
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Set Timeout to 60 sec
	#server.settimeout(60)

	failed_count = 0
	while True:
		try:
			print("start connect to server ")
			server.connect((ip, port))
			break
		except socket.error:
			failed_count += 1
			time.sleep(5)
			print("fail to connect to server %d times" % failed_count)
			if failed_count == 10: return

	quit = False
	# send and receive
	while (not quit):
		create_menu()
		opt = input()
		if opt == '1':
			if(clean(server) == '4'):
				quit = True
		elif opt == '2':
			if(analyze(server) =='4'):
				quit = True
		elif opt == '3':
			validate(server)
		elif (opt == 'R' or opt == 'r'):
			revert(server)
		elif (opt == '4' or opt == '4'):
			server.send('4'.encode())
			quit = True
		else:
			print("Invalid Option, Please enter your option again")
			#print("You should not be here, Report the detail how you reach this line to my lovely cat")
		if(quit):
			break
	server.close()

#Clean Data
#Parameter includes database name, table name,all the parameter required...
def clean(s):
	global isClean
	s.send('1'.encode())
	print("Please Enter the Option:")
	print("Do you want to commit the change? (Y/N)")
	commit = input()
	if(commit == 'y' or commit == 'Y'):
		s.send('Y'.encode())
	else:
		s.send('N'.encode())
	print("What years of data do you want to analyze? Enter 4 digit number")
	print("The number shall be less than 2017 and greater than 1871")
	print("i.e: If I want to use data before 2010, just enter 2010")
	period = input()
	s.send(period.encode())
	isClean = False
	while(not isClean):
		tmp = s.recv(1024).decode()
		if(tmp == "Clean Finished"):
			isClean = True
			print('Data is Cleaned\n')
		elif(tmp == '4'):
			return tmp
		elif(tmp != ''):
			print(tmp)
			if(tmp[0] == 'O'):
				tmp = input()
				s.send(tmp.encode())
	return

#Analyze data
def analyze(s):
	global isClean
	global isAnalyzed
	if(not isClean):
		print("Data is not cleaned, default clean has started...")
		clean(s)

	s.send('2'.encode())
	while (not isAnalyzed):
		tmp = s.recv(1024).decode() 
		if(tmp == "Analyze Finished"):
			print("Data is Analyzed\n")
			isAnalyzed = True
		elif(tmp == '4'):
			return tmp

	return

#Validate analysis
def validate(s):
	global isAnalyzed
	isValidated = False
	#Check if data is analyzed
	if(not isAnalyzed):
		print("Data is not analyzed, default analyze has started...")
		analyze(s)
	s.send('3'.encode())

	while (not isValidated):
		tmp = s.recv(1024).decode() 
		if("Validation Finished" in tmp):
			print("Data is Validated\n")
			isValidated = True
		elif(tmp == '4'):
			return tmp
		elif(tmp != ''):
			print(tmp,'\n')
	

def revert(s):
	isRevert = False
	s.send('R'.encode())
	while (not isRevert):
		tmp = s.recv(1024).decode() 
		if(tmp == "Revert Finished"):
			print("Data is Reverted\n")
			isRevert = True
		elif(tmp == '4'):
			return tmp


def create_menu():
	print("1: Data Clean")
	print("2: Data Analyze")
	print("3: Data Validate")
	print("R: Revert Database")
	print("4: Quit")

if __name__=='__main__':
	start_tcp_client('127.0.0.1',6000)
