from socket import *
import sys
import os

serverPort = 3000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print ('Server is running...')

def get_mimetype(file_path):
	filename, file_ext = os.path.splitext(file_path)
	mimetype = ''

	if (file_ext == '.txt'):
		mimetype = 'Content-Type: text/plain\r\n'
	elif (file_ext == '.jpg' or file_ext == '.jpeg'):
		mimetype = 'Content-Type: image/jpeg\r\n'
	elif (file_ext == '.png'):
		mimetype = 'Content-Type: image/png\r\n'
	elif (file_ext == '.html'):
		mimetype = 'Content-Type: text/html\r\n'
	elif (file_ext == '.mp3'):
		mimetype = 'Content-Type: audio/mpeg\r\n'
	elif (file_ext == '.ogg'):
		mimetype = 'Content-Type: audio/ogg\r\n'
	elif (file_ext == '.mp4'):
		mimetype = 'Content-Type: video/mp4\r\n'

	return mimetype

while 1:
	con, addr = serverSocket.accept()
	req = con.recv(1024).decode('utf-8')
	line = req.split()
	method = line[0]
	httpVersion = line[2]
	path = line[1]
	try:
		file_o = open('.' + path, 'rb')
		response = file_o.read()
		header = 'HTTP/1.1 200 OK\r\n'
		mimetype = get_mimetype(path)
		header += mimetype
		final = header.encode('utf-8')
		final += response
		final += "\r\n".encode('utf-8')
		con.send(final)
	except:
		error = 'Arquivo ' + path + ' nao encontrado.'
		con.send(error.encode('utf-8'))
	con.close()
