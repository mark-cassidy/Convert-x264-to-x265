# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 20:10:17 2023

@author: Mark Cassidy
"""

import os
from moviepy.editor import VideoFileClip
import subprocess

basepath="Z:\Band Of Brothers\m4v"
targetpath="Z:\Frasier\Season 1"
ffmpeg="C:\\ffmpeg\\ffmpeg.exe"

for entry in os.listdir(basepath):
    if os.path.isfile(os.path.join(basepath, entry)):
        entry_fullpath=os.path.join(basepath, entry)
        vid=VideoFileClip(entry_fullpath)
        #Get file size in GB
        vid_size=(os.stat(entry_fullpath).st_size/(1024*1024*1024))
        #print(entry)
        #print(vid_size)
        #Get length of video in minutes
        vid_len=(vid.duration)*0.0166667
        #print(vid_len)
        #Calculate current bit rate
        curr_bitrate=(vid_size)/(vid_len*0.0075)
        #print(curr_bitrate)
        #print(curr_bitrate)
        #Calculate target bit rate in megabits (x265 twice as good so bitrate halved)
        target_bitrate=curr_bitrate/2
        
        #Create upper and lower bounds for bitrate in megabits
        
        min_bitrate=target_bitrate*0.7
        
        max_bitrate=target_bitrate*1.3
        
        command_list=[ffmpeg,"-i",'"'+entry_fullpath+'"',"-c:v hevc_amf","-b:v",str(target_bitrate)+"M",
                      "-minrate",str(min_bitrate)+"M","-maxrate",str(max_bitrate)+"M",
                      "-c:a copy -c:s copy -bufsize 1M -max_muxing_queue_size 1024",
                      '"'+entry_fullpath[:-4]+" (x265).mkv"+'"']
        
        
        command_string=' '.join(command_list)
        #print(curr_bitrate)
        #print(command_string)
        if subprocess.run(command_string).returncode == 0:
            print (entry+" - FFmpeg Script Ran Successfully")
        else:
            print (entry+" - There was an error running your FFmpeg script")
quit
        