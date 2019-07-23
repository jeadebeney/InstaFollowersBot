from slave import Slave
from config import CONFIG_SLAVES
import os
import logging
logging.basicConfig(level=logging.INFO)

export_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'exports')

processes = []
for config in CONFIG_SLAVES:
    slave = Slave(ig_login=config['ig_login'], ig_password=config['ig_password'],
                  comments=config['comments'], hashtags=config['hashtags'], export_dir=export_dir)
    processes.append(slave)
    slave.start()

