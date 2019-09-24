from socket import *
import sys
import os

serverPort = 3000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print ('Server is running on http://localhost:{}/'.format(serverPort))

def get_mimetype(file_ext):
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
	elif (file_ext == '.pdf'):
		mimetype = 'Content-Type: application/pdf\r\n'

	return mimetype

while 1:
	con, addr = serverSocket.accept()
	req = con.recv(1024).decode('utf-8')
	line = req.split(' ')

	print('user {} was connected.'.format(addr))

	method = line[0]
	path = line[1]
	http_version = line[2].split('\r\n')[0]
	header = ''
	try:
		print(path)
		if path == '/':
			path = '/index.html'
		file_o = open('.' + path, 'rb')
		response = file_o.read()
		file_o.close()
		header = '{} 200 OK\r\n'.format(http_version)

		file_name, file_ext = os.path.splitext(path)

		mimetype = get_mimetype(file_ext)
		header += mimetype

		final = header.encode('utf-8')
		final += '\r\n'.encode('utf-8')
		final += response
		final += "\r\n\r\n".encode('utf-8')

		print('{} {} - {} 200 OK'.format(method, path, file_name))

		con.send(final)
	except:
		page_404 = open('./404.html', 'rb')
		response = page_404.read()
		page_404.close()
		header = '{} 200 OK\r\n'.format(http_version)
		mimetype = 'Content-Type: text/html\r\n'

		final = header.encode('utf-8')
		final += '\r\n'.encode('utf-8')
		final += response
		final += "\r\n".encode('utf-8')
		print('{} {} 404 Returning to fallback page...'.format(method, path))
		con.send(final)

	con.close()
