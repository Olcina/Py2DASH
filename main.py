from py2dash import Py2Dash

import os

if __name__ == "__main__":
    ffmpeg_path = os.path.join(os.getcwd(), 'libs', 'ffmpeg.exe')
    ffprobe_path = os.path.join(os.getcwd(), 'libs', 'ffprobe.exe')
    shaka_packager_path = os.path.join(os.getcwd(), 'libs', 'packager-win.exe')
    Obj = Py2Dash(ffmpeg_path=ffmpeg_path, shaka_path=shaka_packager_path)
    print(Obj.name)
    print(Obj.ffmpeg_path)
    print(len(Obj.render_queue))
    for ren in Obj.render_queue:
        print(ren)
        print('')
    Obj.render_all()
