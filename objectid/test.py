import os
import time
import unittest
import random
from multiprocessing import Process, Lock
from threading import Thread, current_thread
import objectid


def gen_objectid(l):
    print('gen_objectid thread start', current_thread().ident)
    ids = []
    for i in range(1000):
        ids.append(objectid.create_objectid())

    l.acquire()
    try:
        f = open('objectid_test.tmp', 'a')
        for id in ids:
            f.write('%s\n'%(id,))
        f.close()
    finally:
        l.release()
    print('gen_objectid thread exit', current_thread().ident)


def gen_objectid_proc(l):
    print('gen_objectid_proc', os.getpid())
    ths = []
    count = 10
    for i in range(count):
        t = Thread(target=gen_objectid, args=(l,))
        t.start()
        ths.append(t)

    alives = count
    while True:        
        for i in range(count):            
            if ths[i] and not ths[i].is_alive():
                print('thread state', ths[i].ident, ths[i].is_alive())
                ths[i] = None
                alives -= 1
        if alives <= 0:
            break
        print('thead alives', alives)
        time.sleep(0.5)


def start_mutil_process():
    lock = Lock()
    procs = []
    count = 10
    for i in range(count):
        p = Process(target=gen_objectid_proc, args=(lock,))
        p.start()
        procs.append(p)

    alives = count
    while True:        
        for i in range(count):
            if procs[i]:
                print('process state', procs[i].pid, procs[i].is_alive())            
            if procs[i] and not procs[i].is_alive():
                procs[i] = None
                alives -= 1
        if alives <= 0:
            break
        print('process alives', alives)
        time.sleep(0.5)        



class TestCreateObjectID(unittest.TestCase):
    """测试ObjectID
    """
    def test_single_process_create_objectid(self):
        ids = []
        for i in range(10000):
            ids.append(objectid.create_objectid())
        idss = set(ids)
        self.assertEqual(10000, len(idss))

    def test_mutil_process_create_objectid(self):
        start_mutil_process()
        ids = []
        f = open('objectid_test.tmp', 'r')
        for line in f: 
            ids.append(line)
        f.close()
        idss = set(ids)
        os.remove('objectid_test.tmp')
        print('id count', len(ids))
        self.assertEqual(100000, len(ids))
        
        

        

    
    
if __name__ == '__main__':
    unittest.main()