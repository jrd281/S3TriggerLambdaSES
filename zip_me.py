import os
import shutil
import tempfile
from pathlib import Path
from shutil import copytree, ignore_patterns
from zipfile import ZipFile
from os import path
from shutil import make_archive


# https://stackoverflow.com/questions/32640053/compressing-directory-using-shutil-make-archive-while-preserving-directory-str
def make_archive(source, destination):
    base = os.path.basename(destination)
    name = base.split('.')[0]
    format = base.split('.')[1]
    shutil.make_archive(name, format, source)
    shutil.move('%s.%s' % (name, format), destination)


temp_dir = tempfile.TemporaryDirectory().name

current_file_path = os.path.realpath(__file__)
parent_path = Path(__file__).parent
parent_path = str(parent_path)

print(temp_dir)

copytree(parent_path, temp_dir, ignore=ignore_patterns('*.git', '*.iml', '.idea','*.zip'))
remove_us = list()
for root, dirs, files in os.walk(temp_dir, topdown=False):
    for filename in files:
        if filename.endswith(".iml"):
            remove_us.append(os.path.join(root, filename))

    for dirname in dirs:
        if dirname.endswith(".iml") or dirname.endswith(".git") or dirname.endswith(".idea"):
            remove_us.append(os.path.join(root, dirname))

for removable in remove_us:
    os.remove(removable)

output_path = parent_path + '/lambda_s3_ses_v1-1.zip'
make_archive(temp_dir, output_path)
# output_zip = parent_path + '/output.zip'
# make_archive(parent_path, output_zip)
