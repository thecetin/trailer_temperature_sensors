from threading import Thread, Lock
import random
import time
import os
import fcntl
from filelock import FileLock, Timeout
'''

file_path = "temperature.txt"

with open(file_path, "a") as f:
        f.truncate(0)
        for i in range(1,23):
            rand_temp = str(round(random.uniform(5.0,25.0),1))
            wrt = (f'000{i} {rand_temp} C')
            f.write(wrt)
            f.write('\n')
f.close()


while True:
    file_path = "temperature.txt"
    lock_path = "temperature.txt.lock"

    lock = FileLock(lock_path, timeout=1)
    with lock:
        with open(file_path, "a") as f:
            f.truncate(0)
            for i in range(1,23):
                rand_temp = str(round(random.uniform(5.0,25.0),1))
                wrt = (f'000{i} {rand_temp} C')
                f.write(wrt)
                f.write('\n')

    lock.acquire()
    try:
        with open(file_path, "a") as f:
            f.truncate(0)
            for i in range(1,23):
                rand_temp = str(round(random.uniform(5.0,25.0),1))
                wrt = (f'000{i} {rand_temp} C')
                f.write(wrt)
                f.write('\n')
    finally:
        lock.release()

    time.sleep(5)


'''
#another code 
while True:
    file_path = "temperature.txt"
    file_lock = open(file_path, 'w')

    try:
        fcntl.flock(file_lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        #print("File is lock")

        file_lock.truncate(0)
        for i in range(1,23):
                rand_temp = str(round(random.uniform(5.0,25.0),1))
                wrt = (f'000{i} {rand_temp} C')
                file_lock.write(wrt)
                file_lock.write('\n')

    except IOError:
        continue
        #print("File is already locked by another process")

    finally:
        fcntl.flock(file_lock.fileno(), fcntl.LOCK_UN)
        #print("File is unclocked")
        file_lock.close()
    
    time.sleep(5)
