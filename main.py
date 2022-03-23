import flask
import yt_dlp as youtube_dl
import threading
import time
import os

from pydub import AudioSegment

app = flask.Flask("")

@app.route("/download")
def Test():
    request = flask.request
    id = request.args.get('ID')
    name = "Files/" + str(id) + ".ogg"
    options = {
        'format':'bestaudio/best',
        'outtmpl': "Files/" + str(id) + ".ogg",
        'keepvideo': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'vorbis',
            'preferredquality': '192k'
        }],
        'postprocessor_args': [
            '-ar', '160000',
            '-ac', '1'
        ],
    }
    
    ydl = youtube_dl.YoutubeDL(options)
    ydl.download(["https://www.youtube.com/watch?v=" + id])
    print("Converting file...")
    """sound = AudioSegment.from_file(name)
    sound = sound.set_channels(1)
    sound.export("Files/" + str(id) + ".ogg", format="ogg")"""
    print("Finished converting")
    @flask.after_this_request
    def remove_file(response):
        try:
            os.remove(name)
        except Exception as error:
            app.logger.error("Error removing or closing downloaded file handle", error)
        return response
    return flask.send_file("Files/" + str(id) + ".ogg")

@app.route("/dlopus")
def Opus():
    request = flask.request
    id = request.args.get('ID')
    name = "Files/" + str(id) + ".opus"
    options = {
        'format':'bestaudio/best',
        'outtmpl': "Files/" + str(id) + ".opus",
        'keepvideo': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'opus',
            'preferredquality': '192k'
        }],
        'postprocessor_args': [
            '-ac', '1'
        ],
    }
    
    ydl = youtube_dl.YoutubeDL(options)
    ydl.download(["https://www.youtube.com/watch?v=" + id])
    print("Converting file...")
    sound = AudioSegment.from_file(name)
    sound = sound.set_channels(1)
    sound.export("Files/" + str(id) + ".ogg", format="ogg")
    print("Finished converting")
    @flask.after_this_request
    def remove_file(response):
        try:
            os.remove(name)
        except Exception as error:
            app.logger.error("Error removing or closing downloaded file handle", error)
        return response
    return flask.send_file("Files/" + str(id) + ".ogg")

if __name__ == "__main__":
    app.run('0.0.0.0', 8080)
