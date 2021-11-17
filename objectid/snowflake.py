'''雪花算法生成ID
'''
import os
import socket
import psutil

class SnowFlakeID():
    '''SnowFlake ID
    '''
    def __init__(self, id=None):
        if id:
            self.parser(id)
        else:
            self.new()

    def parser(self, id):
        '''解析ID
        '''

    def new(self):
        '''生成新ID
        '''

    @classmethod
    def get_host_name(cls):
        '''获取主机名
        '''
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
        return host

    @classmethod
    def get_all_ip(cls, num=False):
        all_ip = []
        all_if = psutil.net_if_addrs()
        for k, v in all_if.items():
            for snic in v:
                if not snic.family.name == 'AF_INET':
                    continue
                if num:
                    ip_list = snic.address.split('.')
                    result=0
                    for i in range(4):
                        result = result + int(ip_list[i])*256**(3-i)
                    all_ip.append(result)
                else:
                    all_ip.append(snic.address)
        return all_ip

    def get_workid(self):
        '''
        '''

    
