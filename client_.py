import socket
import argparse


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-p','--port', type=str,help='Port')
	args = parser.parse_args()

	HOST = 'localhost'    # Cấu hình address server
	try:
		PORT = int(args.port)
	except:
		PORT = 8003            # Cấu hình Port sử dụng
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cấu hình socket
	 # tiến hành kết nối đến server
	s.connect((HOST, PORT))
	while True:
		try:
			dt = input("Send : ")
			if dt == "":
				break
			print(dt,bytes(dt, 'utf-8'))
			s.sendall(bytes(dt, 'utf-8')) # Gửi dữ liệu lên server 
			data = s.recv(1024) # Đọc dữ liệu server trả về
			print('Server Respone: ', repr(data))
		except:
			print("Maybe disconnect to Server")


if __name__ == "__main__":
    main()
