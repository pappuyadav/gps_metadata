
@author: pyada
"""

import subprocess
import os
import json
import glob

class ExifTool(object):

    sentinel = "{ready}\r\n" 

    def __init__(self, executable=r"This is the path where exiftool executable and batch files are stored and installed\exiftool.bat"):
        self.executable = executable 

    def __enter__(self):
        self.process = subprocess.Popen(
            [self.executable, "-stay_open", "True",  "-@", "-"],
            universal_newlines=True,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        return self

    def  __exit__(self, exc_type, exc_value, traceback):
        self.process.stdin.write("-stay_open\nFalse\n")
        self.process.stdin.flush()

    def execute(self, *args):
        args = args + ("-execute\n",)
        self.process.stdin.write(str.join("\n", args))
        self.process.stdin.flush()
        output = ""
        fd = self.process.stdout.fileno()
        while not output.endswith(self.sentinel):
            output += os.read(fd, 4096).decode('utf-8')
        return output[:-len(self.sentinel)]

    def get_metadata(self, *filenames):
        return json.loads(self.execute("-G", "-j", "-n", *filenames))


with ExifTool() as et:
    dirpath=r"This is your image files directory path"
    filelist = [f for f in glob.glob(dirpath + "**/*.*", recursive=True)]
    img_num=1
    for fp in filelist:
        b=str(fp)
        name, ext = os.path.splitext(b)
        name=os.path.basename(b)
        name=os.path.splitext(name)[0]
        datafile=os.path.join(dirpath,b)
        metadata=et.get_metadata(datafile)
        gpsfile=open('gps_data.txt','a')
        for d in metadata:
            gpsfile.write("{:20.20} {:20.20} {:20.20} {:20.20}\n".format(d["EXIF:DateTimeOriginal"],d["EXIF:GPSLatitude"],d["EXIF:GPSLongitude"],d["EXIF:GPSAltitude"]))
        img_num += 1
    gpsfile.close()
