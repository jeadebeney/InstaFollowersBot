import os
import csv
import datetime


class Tracker:

    __slots__ = '_export_path'

    def __init__(self, export_path):
        self._export_path = export_path
        self._init_export_dir()

    def _init_export_dir(self):
        ''' Init export dir and file if needed '''
        export_dir = '/'.join([x for x in self._export_path.split('/')[:-1]])

        # Create required directories
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        # create a csv file if does not exist yet
        if os.path.isfile(self._export_path) == False:
            headers = ['time', 'action']
            with open(self._export_path, mode='w') as f:
                csv_writer = csv.writer(f, delimiter=',')
                csv_writer.writerow(headers)

    def track(self, action, *args):
        ''' Append new row to export file '''
        now = datetime.datetime.now()
        with open(self._export_path, mode='a') as tracking_file:
            track_writer = csv.writer(tracking_file, delimiter=',')
            track_writer.writerow([now] + [action] + list(args))
