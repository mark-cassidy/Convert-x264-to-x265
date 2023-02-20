# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 09:27:48 2023

@author: Mark Cassidy
"""

import os
from moviepy.editor import VideoFileClip
import subprocess
import json


basepath="Z:\The X-Files\Season 1"

ffmpeg="C:\\ffmpeg\\ffmpeg.exe"
ffprobe="C:\\ffmpeg\\ffprobe.exe"

for entry in os.listdir(basepath):
    if os.path.isfile(os.path.join(basepath, entry)):
        entry_fullpath=os.path.join(basepath, entry)
        
        command_ffp=[ffprobe,"-hide_banner -loglevel fatal -show_error -show_format -show_streams -show_programs -show_chapters -show_private_data -print_format json",'"'+entry_fullpath+'"' ]
        
        command_string_ffp=' '.join(command_ffp)
        
        
        output_ffp=subprocess.run(command_string_ffp,stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        
        
        output_ffp_dict=json.loads(output_ffp.stdout)
        
        codec=output_ffp_dict['streams'][0]['codec_name']
        
        
        
        if codec=="h264":
            print(entry+" - File x264 - running conversion")
            vid=VideoFileClip(entry_fullpath)
            #Get file size in GB
            vid_size=(os.stat(entry_fullpath).st_size/(1024*1024*1024))
            
            #Get length of video in minutes
            vid_len=(vid.duration)*0.0166667
            
            #Calculate current bit rate
            curr_bitrate=(vid_size)/(vid_len*0.0075)
        
            #Calculate target bit rate in megabits (x265 twice as good so bitrate halved)
            target_bitrate=curr_bitrate/2
        
            #Create upper and lower bounds for bitrate in megabits
        
            min_bitrate=target_bitrate*0.7
            max_bitrate=target_bitrate*1.3
            
            #Build FFMpeg command
            command_list=[ffmpeg,"-i",'"'+entry_fullpath+'"',"-c:v hevc_amf","-b:v",str(target_bitrate)+"M",
                          "-minrate",str(min_bitrate)+"M","-maxrate",str(max_bitrate)+"M",
                          "-c:a copy -c:s copy -bufsize 1M -max_muxing_queue_size 1024",
                          '"'+entry_fullpath[:-4]+" (x265).mkv"+'"']
        
        
            command_string=' '.join(command_list)

            #run FFMpeg
            if subprocess.run(command_string).returncode == 0:
                print (entry+" - FFmpeg Script Ran Successfully")
            else:
                print (entry+" - There was an error running your FFmpeg script")
        else:
            print(entry+" - File not x264")
quit
