#!/usr/bin/env python
'''
The entry of video classfier.
This program takes in a command line argument which is the given title of input video file.
FFmpeg is used to extract video frame every five second.
The extracted jpg files are examined by Yahoo's open-source CNN NSFW classfier.

Example:
Python3 video_classifier.py test.mp4
'''

import sys, os, subprocess
import argparse
import tensorflow as tf
import numpy as np

from model import OpenNsfwModel, InputType
from image_utils import create_tensorflow_image_loader
from image_utils import create_yahoo_image_loader

IMAGE_LOADER_TENSORFLOW = "tensorflow"
IMAGE_LOADER_YAHOO = "yahoo"



def main(fileTitle):

    videoTitle = fileTitle.split('.')[0]

    home = os.path.expanduser("~")
    # The directory in which video file is stored
    inFilePath = home + '/Documents/Videos/'
	
    # The directory the extracted video frames will be stored in
    outPath = home + '/Documents/Frames/' + str(videoTitle)
    os.mkdir(outPath)
    outFilePath = outPath + '/' + str(videoTitle) + '%03d.jpg'
	
    # The directory of ffmpeg executable
    ffmpeg = home + '/Downloads/ffmpeg-3.4.1/ffmpeg'

    # Generate and execute ffmpeg command       
    cmd = ffmpeg + ' -i ' + inFilePath + fileTitle + ' -vf fps=1 -qscale:v 16 ' + outFilePath
    subprocess.call(cmd, shell=True)

    # Evaluate the extracted frames
    NSFWscore = 0
    for root, dirs, files in os.walk(outPath):
        for jpgFile in files:
            line = 'python3 classify_nsfw.py -m open_nsfw-weights.npy ' + outPath + '/' + jpgFile
            obj = os.popen(line)    # block 
            score = obj.read()
            obj.close()
            NSFWscore = max(NSFWscore, float(score))
    print(NSFWscore)
    if (NSFWscore >= 0.8):
        print('This video contains image that is Not Suitable For Work.')
    elif (NSFWscore > 0.5 and NSFWscore < 0.8):
        print('This video is probably Not Suitable For Work.')
    else:
        print('Video OK.')



if __name__ == "__main__":
	main(sys.argv[1])
