import os

print [F for F in os.listdir('/dev/') if F[:4] == 'tty.']