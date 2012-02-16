#!/usr/bin/python
import serial
import sys
import glob
import sys
import termios
import tty
import select

def DataAvailable(pipe):
   return select.select([pipe], [], [], 0) == ([pipe], [], [])

if(len(sys.argv) != 2):
   print "Usage: %s <OUTFILE>" % (sys.argv[0],)
   sys.exit(-1)

old_settings_in = termios.tcgetattr(sys.stdin)
old_settings_out = termios.tcgetattr(sys.stdout)

serialDevices = glob.glob("/dev/tty.usbserial-*")
serialDevice = serialDevices[0]
outfile = open(sys.argv[1], "w")

# open nonblocking
ser=serial.Serial(serialDevice, baudrate = 115200, timeout = 0)

try:
   tty.setcbreak(sys.stdin.fileno())
   tty.setcbreak(sys.stdout.fileno())

   while 1:
      if DataAvailable(sys.stdin):
         c = sys.stdin.read(1)
         if c == '\x1b':    # x1b is ESC
            break
         ser.write(c)
         sys.stdout.write(c)
         sys.stdout.flush()
      buf = ser.read(128)
      sys.stdout.write(buf)
      sys.stdout.flush()
      outfile.write(buf)

finally:
   termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings_in)
   termios.tcsetattr(sys.stdout, termios.TCSADRAIN, old_settings_out)
