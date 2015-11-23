import socket, sys
from device import device

class IRCAM(device):

  def __init__(self):
    pass

  def __str__(self):
    return "IRCAM"

  def connect(self, IP, port):
    self.disconnect()
    self.UDP_IP = IP
    self.UDP_PORT = port
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    self.sock.bind((self.UDP_IP, self.UDP_PORT))

    self.lastspat = None
    self.lastpitch = None
    self.lastcue = None

  def disconnect(self):
    try:
        self.sock.shutdown()
        self.sock.close()
        del self.sock
    except:
        sys.stdout.write("Socket not connected\n")

  def getMessage(self):

    while True:

        data = self.sock.recv(1024)         # buffer size is 1024 bytes
        self.sock.sendto(data, ('localhost',7004))  # Send data to local port where Processing sketch is listening

        if data[:12] == 'spat source ':

          value = data[17:]
          value = abs(int(float(value))) #numbers are negative so abs() is needed
          print value, self.lastspat
          if value != self.lastspat:
            self.lastspat = value
            return {'spat':value}

        elif data[:5] == 'pitch':

          value = data[5:]
          value = int(value)

          if value != self.lastpitch:
            self.lastpitch = value
            return {'pitch':value}

        elif data[:4] == 'cue ':

            value = int(float(data[4:]))

            if value != self.lastcue:
                self.lastcue = value
                return {'cue':value}

  def allMessage(self):
    data, addr = self.sock.recvfrom(1024)       # buffer size is 1024 bytes
    #self.sock.sendto(data, ('localhost',7007))
    return data





if __name__ == '__main__':

  IRCAM = IRCAM()
  IRCAM.connect('localhost',7000)
  while True:
    print IRCAM.getMessage()
    print IRCAM.allMessage()
