#!/usr/bin/env python3
# coding=utf-8
# Created Time: 2015-10-12

__author__ = 'Matthew Gao'

import urllib.request
import sys
import time
import os

BRANCH_MAP = { 
               '11.1.1': ['kili-tip','kili'],
               '11.3.1' : ['k2-tip','k2'],
               '11.2.0' : ['11.2.0','k2'],
               '11.3.0' : ['11.3.0','k2'],
               '11.1.0' : ['11.1.0','kili'],
               '11.4.0' : ['kanga-tip','kanga'],
               '10.7.3' : ['jaytip','jay'],
               '10.7.2' : ['10.7.2','jay'],
               '10.7.2' : ['10.7.1','jay'],
               '10.7.0' : ['10.7.0','jay']
               # '10.6.6' : ['indextip', 'index'],
               # '10.6.5' : ['10.6.5','index'],
               # '10.6.4' : ['10.6.4','index'],
               # '10.6.3' : ['10.6.3','index'],
               # '10.6.2' : ['10.6.2','index']
            }


class BobDownloader(object):
    """docstring for BobDownloader"""
    _base_path = 'http://10.4.16.60/nas-bob/daily/appliance/daily/ex-{0}-appliance/{1}-{2}/{1}-{2}.iso'
    


    def __init__(self, branch, build, _image_dir=None):
        super(BobDownloader, self).__init__()
        self._image_dir = _image_dir
        self.branch = branch
        self.build = build
        self.file_name = '{0}.{1}.iso'.format(self.branch, self.build)
        self.md5_file_name = '{0}.{1}.iso.md5'.format(self.branch, self.build)
        
        if '10' in self.branch:
            self.file_name = 'unstripped-' + self.file_name
            self.md5_file_name = 'unstripped-' + self.md5_file_name
        
        self.final_path = self._base_path.format(BRANCH_MAP[self.branch][0], 
                                            self.branch, self.build)

        if (self._image_dir is not None and 
                isinstance(self._image_dir,str) and 
                self._image_dir[-1] != '/'):
            self._image_dir += '/'

        if self._image_dir is not None and isinstance(self._image_dir, str):
            self._full_path_file_name = self._image_dir + self.file_name
            self._full_path_md5_file_name = self._image_dir + self.md5_file_name

        print(self.final_path)

    def start(self):
        if self._check_exist() or (not self._check_valid()):
            return self._full_path_file_name

        try:
            print("Start downloading: {0}".format(self.file_name))
            local_filename, headers = urllib.request.urlretrieve(self.final_path, 
                            filename=self._full_path_file_name, reporthook=self._progress_hook)
            print("\nFinish: {0}".format(self.file_name))
            print("Start downloading: {0}".format(self.md5_file_name))
            local_filename, headers = urllib.request.urlretrieve(self.final_path, 
                            filename=self._full_path_md5_file_name, reporthook=self._progress_hook)
            print("\nFinish: {0}".format(self.md5_file_name))
        except urllib.error.HTTPError as e:
            print(e.code)
            print(e.read())

        return self._full_path_file_name

    def _check_exist(self):
        if os.path.exists(self._full_path_file_name) and os.path.exists(self._full_path_md5_file_name) and self._md5_check():
            print("{0} existed, skip downloading".format(self.file_name))
            return True
        return False

    def _check_valid(self):
        if self.branch in BRANCH_MAP.keys():
            return True
        print("{0} is invalid branch".format(self.branch))
        return False

    def _md5_check(self): return True

    def _progress_hook(self, block, block_size, total_size):
        percent = (block * block_size)*100 / total_size
        sys.stdout.write('\b\b\b\b\b\b\b')
        sys.stdout.write('%.2f%%' % percent)
        sys.stdout.flush()


def run():
    b = BobDownloader('10.7.3','217','/home/shgao/bob_build')
    b.start()

if __name__ == '__main__':
    run()
