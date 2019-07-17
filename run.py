
from slave import commentLoop
from config import SLAVES
import threading
import time
import os

# create export directory if needed
export_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'exports')
if not os.path.exists(export_dir):
    os.makedirs(export_dir)

# create one thread for each slave instance
threads = []
for slave in SLAVES:
    export_path = os.path.join(export_dir, slave['name'])

    t = threading.Thread(target=commentLoop, args=(
        slave['hashtags'], export_path,))
    threads.append(t)

# start all threads
for t in threads:
    t.start()