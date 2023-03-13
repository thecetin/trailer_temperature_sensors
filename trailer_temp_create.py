import random
import time

while True:
    with open("temperature.txt", 'w') as temp_data:
        temp_data.truncate(0)
        for i in range(1,23):
            rand_temp = str(round(random.uniform(5.0,25.0),1))
            wrt = (f'000{i} {rand_temp} C')
            temp_data.write(wrt)
            temp_data.write('\n')
    
    temp_data.close()
    time.sleep(5)

        