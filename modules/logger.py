from pathlib import Path
from datetime import datetime
import os

home_dir = str(Path.home())
log_dir = home_dir + "\zorra_hlrer"
log_file_name = "zorra_hlr_{}.log".format(datetime.now().strftime("%Y-%m-%d_%H%M%S"))


def logger(message):
    global log_dir
    global log_file_name
    
    full_log_path = os.path.join(log_dir, log_file_name)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    with open(full_log_path, 'a+') as log_f:
        log_message = "[{}] {}\n".format(timestamp, message)
        log_f.write(log_message)
