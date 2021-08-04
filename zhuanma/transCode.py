import thread
import time
import subprocess
import os

process_num = 1
result = [0] * process_num

file = ""
def run_ffmpeg(count):
    cmd = 'ffmpeg -f concat -safe 0 -i list.txt -vf "scale=1280:720" ' + str(count) + '.mp4'
    print(cmd)
    p = subprocess.Popen(cmd, shell=True)
    p.wait()
    result[count-1] = 1

start_time = time.time()

# for i in range(1, process_num+1):
thread.start_new_thread(run_ffmpeg, (1,))

done = False
while not done:
    done = True
    for i in range(0, process_num):
        if result[i] != 1:
            done = False
            break
    if not done:
        time.sleep(1)

cost_time = time.time() - start_time
print('done', cost_time)
