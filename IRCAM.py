import socket

class IRCAM:

  def __init__(self,IP,port):
    self.UDP_IP = IP
    self.UDP_PORT = port
    self.type = 'IRCAM'

    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    self.sock.bind((self.UDP_IP, self.UDP_PORT))

  def __str__():
    return "IRCAM"

  def getMessage(self):

    data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
    self.sock.sendto(data, ('localhost',7004))
    # if data[:12] == 'spat source ':
    #   value = data[17:]
    #   if value != None:
    #     return abs(int(float(value)))
    if data[:5] == 'pitch':
      value = data[5:]
      if value != None:
        return int(value)
      #if data[:4] == 'cue ':
      #  value = int(float(data[4:]))
      #  return {'cue':{'cue':value}}


  def allMessage(self):
    data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
    #self.sock.sendto(data, ('localhost',7007))
    return data





if __name__ == '__main__':

  IRCAM = IRCAM('localhost',7007)
  while True:
    print IRCAM.getMessage()
