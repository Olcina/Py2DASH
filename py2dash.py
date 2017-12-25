# TODO:
# 1 - define the ffprobe and ffmpeg paths for the class
# 2 - define paths to input_videos

import os
import sys
import glob
import pprint
import subprocess as sp

# Global properties
INPUT_VIDEOS_PATH = 'input_videos'
OUTPUT_VIDEOS_PATH = 'output_videos'

class VideoStatus():
    def __init__(self,global_path):
        self.converted = False
        self.global_path = global_path
        self.file_name = os.path.basename(global_path)
        self.name = os.path.splitext(self.file_name)[0]

    def __str__(self):
        return self.name

class Py2Dash(object):
    name = 'py2dash'
    def __init__(self, **kwargs):
        self.input_videos = self.set_input_videos()

        if not kwargs.get('ffmpeg_path'):
            self.ffmpeg_path = self.get_ffmpeg_path()
        else:
            self.ffmpeg_path = kwargs.get('ffmpeg_path')
        if not kwargs.get('ffprobe_path'):
            self.ffprobe_path = self.get_ffprobe_path()
        else:
            self.ffprobe_path = kwargs.get('ffprobe_path')
        if not kwargs.get('shaka_path'):
            self.shaka_path = self.get_shaka_path()
        else:
            self.shaka_path = kwargs.get('shaka_path')

        self.render_queue = []
        self.videos_to_render()


    def __str__(self):
        return self.name

    def set_input_videos(self):
        # add the input videos to the vid_input videos
        input_videos = []
        paths = glob.glob(os.path.join(os.getcwd(),INPUT_VIDEOS_PATH ,'*.mp4'))
        for path in paths:
            input_videos.append(VideoStatus(path))
        return input_videos

    def get_ffmpeg_path(self):
        print('WARNING: please define the path to ffmpeg')
        return 'ok'
    def set_ffmpeg_path(self, ffmpeg_path):
        self.ffmpeg_path = ffmpeg_path
        
    def get_ffprobe_path(self):
        print('WARNING : please define the path to ffmpeg')
        return 'ok'
    def set_ffprobe_path(self, ffprobe_path):
        self.ffprobe_path = ffprobe_path

    def get_shaka_path(self):
        print('WARNING : please define the path to ffmpeg')
        return 'ok'

    def set_shaka_path(self, shaka_path):
        self.shaka_path = shaka_path

    def check_ffmpeg(self):
        status = sp.check_call(self.ffmpeg_path + ' -h')
        if status == 1:
            return print('something went wrong with ffmpeg, check the path')
        else:
            return print('ffmpeg working')

    def check_ffprobe(self):
        status = sp.check_call(self.ffprobe_path + ' -h')
        if status == 1:
            return print('something went wrong with ffprobe, check the path')
        else:
            return print('ffprobe working')

    def video_to_queue(self, video):
        out_path = os.path.join(os.getcwd(), OUTPUT_VIDEOS_PATH)

        self.render_queue.append(self.ffmpeg_path + \
            ' -y -i ' + video.global_path + ' -c:a copy ' + \
            ' -vf "scale=-2:360" ' + \
            ' -c:v libx264 -profile:v baseline -level:v 3.0 ' + \
            ' -x264opts scenecut=0:open_gop=0:min-keyint=72:keyint=72 ' + \
            ' -minrate 600k -maxrate 600k -bufsize 600k -b:v 600k ' + \
            ' -y ' + os.path.join(out_path,
                                 video.name) + '_360p_600.mp4')

        self.render_queue.append(self.ffmpeg_path +
            ' -i ' + video.global_path + ' -c:a copy ' + \
            ' -vf "scale=-2:480" ' + \
            ' -c:v libx264 -profile:v baseline -level:v 3.0 ' + \
            ' -x264opts scenecut=0:open_gop=0:min-keyint=72:keyint=72 ' + \
            ' -minrate 1000k -maxrate 1000k -bufsize 1000k -b:v 1000k ' + \
            ' -y ' + os.path.join(out_path,
                                  video.name) + '_480p_1000.mp4')

        self.render_queue.append(self.ffmpeg_path +
            ' -i ' + video.global_path + ' -c:a copy ' + \
            ' -vf "scale=-2:720" ' + \
            ' -c:v libx264 -profile:v baseline -level:v 3.0 ' + \
            ' -x264opts scenecut=0:open_gop=0:min-keyint=72:keyint=72 ' + \
            ' -minrate 1500k -maxrate 1500k -bufsize 1500k -b:v 1500k ' + \
            ' -y ' + os.path.join(out_path,
                                  video.name) + '_720p_1500.mp4')


    def packager_command(self, video):
        output_complete = os.path.join(
            os.getcwd(), OUTPUT_VIDEOS_PATH, 'package', video.name)
        input_complete = os.path.join(os.getcwd(),OUTPUT_VIDEOS_PATH, video.name)

        string = self.shaka_path + \
                ' in={video_name}_360p_600.mp4,stream=audio,output={output_complete}_audio_dash.mp4' + \
                ' in={video_name}_360p_600.mp4,stream=video,output={output_complete}_360p_dash.mp4' + \
                ' in={video_name}_480p_1000.mp4,stream=video,output={output_complete}_480p_dash.mp4' + \
                ' in={video_name}_720p_1500.mp4,stream=video,output={output_complete}_720p_dash.mp4' + \
                ' --mpd_output {output_complete}_manifest.mpd'

        formated_string = string.format(
            video_name=input_complete, output_complete=output_complete)
        self.render_queue.append(formated_string)

    def videos_to_render(self):
        for vid in self.input_videos:
            self.video_to_queue(vid)
            self.packager_command(vid)

    def render_all(self):
        for command in self.render_queue:
            command_output = sp.check_output(command).decode()
            print(command_output)
        
        print('all rendered and packaged')

