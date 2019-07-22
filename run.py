from slave import Slave
from config import CONFIG_SLAVES
import os
import logging
logging.basicConfig(level=logging.DEBUG)

# # create export directory if needed
export_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'exports')
# if not os.path.exists(export_dir):
#     os.makedirs(export_dir)

for config in CONFIG_SLAVES:
    export_path = os.path.join(export_dir, config['ig_login'])
    slave = Slave(ig_login=config['ig_login'], ig_password=config['ig_password'],
                  comments=config['comments'], hashtags=config['hashtags'], export_path=export_path)