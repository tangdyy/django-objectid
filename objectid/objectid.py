"""用于分布式环境中生成24个字符组成的不重复ID
"""

import os
import re
import hashlib
import time
import threading
import socket


l = threading.RLock()

class ObjectID():
    """
    Generate object id. 
    """
    def __init__(self, id=None):
        l.acquire()
        try:
            g = globals()
            if not '__objectid_global' in g:
                obj = {}
                obj["timestamp"] = 0
                obj["host"] = self.getIP(hex=True) or self.getHostID()
                obj["host"] = obj["host"][:6]
                obj["counter"] = 0
                ptid = os.getpid()
                obj["pid"] = "{:0>4x}".format(ptid)[:4]
                g['__objectid_global'] = obj
            self._gobj = g['__objectid_global']
            if id:
                self.parser(id)
            else:
                self.new()
        finally:
            l.release()
        
    def parser(self, id):
        """
        Parser id to objectid.
        """
        if not isinstance(id, str) or not re.match('^[0-9a-fA-F]{24}$', id):
            raise ValueError('objectid is 12 bytes hex str.')
        # timestamp sec 8 bytes
        sec = int(id[:8],16)
        # timestamp msec 3 bytes
        msec = int(id[8:11],16)
        self.timestamp = sec*1000 + msec
        # host 6 bytes
        self.host = id[11:17]
        # pid 4 bytes
        self.pid = id[17:21]
        # counter 3 bytes
        self.count = int(id[21:24],16)
        
    def new(self):
        """
        Generate new id.
        """
        old_time = self._gobj["timestamp"]        
        self.timestamp = int(time.time()*1000)
        if self.timestamp < old_time:
            self.timestamp = old_time
            
        if old_time == self.timestamp and self._gobj["counter"] < 0xfff:
            self._gobj["counter"] += 1
        elif old_time == self.timestamp and self._gobj["counter"] >= 0xfff:
            self.timestamp += 1
            self._gobj["counter"] = 0
        else:
            self._gobj["counter"] = 0
            
        if self._gobj["counter"] > 0xfff:
            raise ValueError('Counter greater than 0xfff.')      
              
        self._gobj["timestamp"] = self.timestamp    
        self.count = self._gobj["counter"]
        self.host = self._gobj["host"]
        self.pid = self._gobj["pid"]
        return self.__str__()
           
    def getHostID(self):
        systype = os.name
        host = 'Unkwon hostname'
        if systype == 'nt':
            host = os.getenv('computername')
        elif systype == 'posix':
            h = os.popen('echo $HOSTNAME')
            try:
                host = h.read()
            finally:
                h.close()
        m = hashlib.sha256()
        m.update('{}'.format(host).encode('utf-8'))
        d = m.hexdigest()
        return d[:6]
     
    def __str__(self):
        sec = int(self.timestamp/1000)
        msec = int(self.timestamp - sec*1000)
        return "{0:08x}{1:03x}{2}{3}{4:03x}".format(sec, msec, self.host[:6], self.pid[:4], self.count)

    def getIP(self, hex=False):
        """获取本机IP
        为保证ID唯一, 不允许使用127.0.0.1, 按以下优先级获取IP
        公网IP > 10.0.0.0 > 172.0.0.0 > 192.168.0.0 
        """
        prefixs = ['10.', '172.16.', '172.17.', '172.18.', '172.19.', '172.20.', '172.21.', '172.22.', '172.23.',
                   '172.24.', '172.25.', '172.26.', '172.27.', '172.28.', '172.29.', '172.30.', '172.31.', '192.168.']
        ip0 = None
        priority = 10000
        hostname = socket.gethostname()
        try:
            ip_list = socket.gethostbyname_ex(hostname)[2]

            for ip in ip_list: 
                if ip.startswith("127."):
                    continue

                if ip.startswith("10."):
                    if priority > 0:
                        ip0 = ip
                        priority = 0
                elif ip.startswith("172.") and ip[:7] in prefixs:
                    if priority > 1:
                        ip0 = ip
                        priority = 1
                elif ip.startswith("192.168."):
                    if priority > 2:
                        ip0 = ip 
                        priority = 2 
                else:
                    ip0 = ip
                    priority = -1            
        except:
            pass
        if ip0 is None: 
            return None
        
        if hex: 
            iparr = ip0.split('.')
            return '{:02x}{:02x}{:02x}{:02x}'.format(int(iparr[0]), int(iparr[1]), int(iparr[2]), int(iparr[3]))
        return ip0


def create_objectid():
    return str(ObjectID())        
    