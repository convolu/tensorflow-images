import os
import hashlib
import sys
import tarfile

from functools import partial

import requests

DATAFILE = "101_ObjectCategories.tar.gz"
DATAFILE_MD5 = "b224c7392d521a49829488ab0f1120d9"

EXTRACTEDDATADIR = "101_ObjectCategories"

DATASETURL = "http://www.vision.caltech.edu/Image_Datasets/Caltech101/101_ObjectCategories.tar.gz"


def download_input_data():
    r = requests.get(DATASETURL)
    with open(DATAFILE, "wb") as f:
        f.write(r.content)


def md5sum(filename: str):
    with open(filename, mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return d.hexdigest()


def extract_tarfile():
    with tarfile.open(DATAFILE) as tar:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar)

if __name__ == "__main__":
    if not os.path.isfile(DATAFILE):
        print("File {} not found, will download".format(DATAFILE))
        download_input_data()

    if md5sum(DATAFILE) != DATAFILE_MD5:
        print("MD5 Hash doesn't match for dataset file", file=sys.stderr)
        sys.exit(1)

    if not os.path.isdir(EXTRACTEDDATADIR):
        print("Will extract {}".format(DATAFILE))
        extract_tarfile()
