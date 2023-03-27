import msvcrt
from threading import Thread, Lock
import random
import time
import os
from filelock import FileLock, Timeout

while True:

    file_path = "temperature.txt"
    lock_path = "temperature.txt.lock"

    lock = FileLock(lock_path, timeout=1)
    with lock:
        with open(file_path, "a") as f:
            #f.truncate(0)
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

        
