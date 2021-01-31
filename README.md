# gps_metadata
Extract GPS coordinates from image metadata 
This python script will help you extract GPS coordinates (latitude, longitude, altitude) along with timestamp of all the geo-tagged images in a directory.
The extracted information is stored in *.txt file. Information of each image file is stored in a new line.
This script invokes Phil Harvey's "ExifTool" to read the metadata file of geo-tagged images and then extracts the desired information from there.

Successfully Tested on:
# Python 3.8
# Exiftool 11.99
# Anaconda3
# Windows10

