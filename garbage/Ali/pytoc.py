import socket

UDP_PORT = 50000 # port for python c communication
UDP_IP =  "127.0.0.1"

message = b"village "

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(message, (UDP_IP, UDP_PORT))
print("message sent")
sock.close()
