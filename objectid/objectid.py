"""用于分布式环境中生成24个字符组成的不重复ID
"""

import os
import re
import hashlib
import time
import threading
import psutil

l = threading.RLock()

class ObjectID():
    """
    Generate object id. 
    """
    def __init__(self,id=None):
        l.acquire()
        try:
            g = globals()
            if not '__objectid_global' in g:
                obj = {}
                obj["timestamp"] = 0
                obj["host"] = self.getIP() or self.getHostID()
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
        
    def parser(self,id):
        """
        Parser id to objectid.
        """
        if not isinstance(id,str) or not re.match('^[0-9a-fA-F]{24}$',id):
            raise ValueError('objectid is 12 bytes hex  str.')
        self.timestamp = int(id[:11],16)
        self.host = id[8:14]
        self.pid = id[14:18]
        self.count = int(id[21:24],16)
        
    def new(self):
        """
        Generate new id.
        """
        old_time = self._gobj["timestamp"]        
        self.timestamp = int(time.time()*1000)
        if self.timestamp < old_time:
            raise SystemError('Time callback exists. Please check the host clock.')
            
        if old_time == self.timestamp:
            self._gobj["counter"] += 1
        else:
            self._gobj["counter"] = 0
        if self._gobj["counter"] > 0xfff:
            raise ValueError('Counter greater than 0xfff.')            
        self._gobj["timestamp"] = self.timestamp    
        self.count = self._gobj["counter"]
        self.host = self._gobj["host"]
        self.pid = self._gobj["pid"]
        return self.__str__()

    def getIP(self):
        ip = None
        info = psutil.net_if_addrs()  
        for k,v in info.items():
            for item in v:
                if item[0] == 2 and not item[1]=='127.0.0.1':
                    if item[1][:2] == '10' or item[1][:7] == '192.168':
                        ip = item[1]
                        break
            if ip:
                break
        if ip is None:
            return None
        ipl = ip.split('.')
        return '%02x%02x%02x'%(int(ipl[1]), int(ipl[2]), int(ipl[3]))
            
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
        return "{0:011x}{1}{2}{3:03x}".format(self.timestamp,self.host,self.pid,self.count)


def create_objectid():
    return str(ObjectID())        
    