import telnetlib
import errno
import sys
import socket
import select
import time
class Telnet_print(telnetlib.Telnet):
    def _read_extra(self,command):
        time.sleep(30)
        buf = self.sock.recv(5000000)
        return buf
    def wirte_info(self,command):
        txt = self._read_extra(command)
        print txt
        ftxt = open('info_hard.txt_3','a+')
        ftxt.write(str(txt))
        ftxt.close()
    