import socket


class IRCAM:

  def __init__(self,IP,port):
    self.UDP_IP = IP
    self.UDP_PORT = port
    self.type = 'IRCAM'

    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    self.sock.bind((self.UDP_IP, self.UDP_PORT))

  def getMessage(self):

    while True:
      data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
      if data[:17] == 'spat source 3 az ':
        return abs(int(data[17:]))




if __name__ == '__main__':

  IRCAM = IRCAM('localhost',7003)
  while True:
    print IRCAM.getMessage()


