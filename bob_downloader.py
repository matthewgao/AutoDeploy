#!/usr/bin/env python3
# coding=utf-8
# Created Time: 2015-10-12

__author__ = 'Matthew Gao'

import urllib.request
import sys
import time
import os

class BobDownloader(object):
    """docstring for BobDownloader"""
    _base_path = 'http://10.4.16.60/nas-bob/daily/appliance/daily/ex-{0}-appliance/{1}-{2}/{1}-{2}.iso'

    _branch_map = { 
                    '11.1.1': ['kili-tip','kili'],
                    '11.3.1' : ['k2-tip','k2'],
                    '11.2.0' : ['11.2.0','k2'],
                    '11.3.0' : ['11.3.0','k2'],
                    '11.1.0' : ['11.1.0','kili'],
                    '11.4.0' : ['kanga-tip','kanga'],
                    '10.7.3' : ['jaytip','jay'],
                    '10.7.2' : ['10.7.2','jay'],
                    '10.7.2' : ['10.7.1','jay'],
                    '10.7.0' : ['10.7.0','jay'],
                    '10.6.6' : ['indextip', 'index'],
                    '10.6.5' : ['10.6.5','index'],
                    '10.6.4' : ['10.6.4','index'],
                    '10.6.3' : ['10.6.3','index'],
                    '10.6.2' : ['10.6.2','index']
                 }

    def __init__(self, branch, build):
        super(BobDownloader, self).__init__()
        self.branch = branch
        self.build = build
        self.file_name = '{0}.{1}.iso'.format(self.branch, self.build)
        self.md5_file_name = '{0}.{1}.iso.md5'.format(self.branch, self.build)
        
        if '10' in self.branch:
            self.file_name = 'unstripped-' + self.file_name
            self.md5_file_name = 'unstripped-' + self.md5_file_name
        
        self.final_path = self._base_path.format(self._branch_map[self.branch][0], 
                                            self.branch, self.build)
        print(self.final_path)

    def start(self):
        if self._check_exist() or !self._check_valid():
            return

        try:
            print("Start downloading: {0}".format(self.file_name))
            local_filename, headers = urllib.request.urlretrieve(self.final_path, 
                            filename=self.file_name, reporthook=self._progress_hook)
            print("\nFinish: {0}".format(self.file_name))
            print("Start downloading: {0}".format(self.md5_file_name))
            local_filename, headers = urllib.request.urlretrieve(self.final_path, 
                            filename=self.md5_file_name, reporthook=self._progress_hook)
            print("\nFinish: {0}".format(self.md5_file_name))
        except urllib.error.HTTPError as e:
            print(e.code)
            print(e.read())

    def _check_exist(self):
        if os.path.exists(self.file_name) and os.path.exists(self.md5_file_name) and self._md5_check():
            print("{0} existed, skip downloading".format(self.file_name))
            return True
        return False

    def _check_valid(self):
        if self.branch in self._branch_map.keys():
            return True
        print("{0} is invalid branch".format(self.branch))
        return False

    def _md5_check(self): return True

    def _progress_hook(self, block, block_size, total_size):
        percent = (block * block_size)*100 / total_size
        sys.stdout.write('\b\b\b\b\b\b')
        sys.stdout.write('%.2f%%' % percent)
        sys.stdout.flush()


def run():
    b = BobDownloader('10.7.3','217')
    b.start()

def usage():
    pass

if __name__ == '__main__':
    run()
