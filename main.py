from pytube import YouTube, Channel, Playlist
from pathlib import Path
from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    print(percentage_of_completion)


def get_video_info(yt, url, optional_info):
    info = {
            'status': 200,
            'url': url,
            'channel_url': yt.channel_url,
            'channel_title': Channel(yt.channel_url).channel_name,
            'title': yt.title,
            'views': yt.views,
            'image': yt.thumbnail_url,
            'length': round(yt.length / 60, 2),
            'author': yt.author,
            }
    if optional_info:
        info['description'] = yt.description
    return info


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/youtubeinfo', methods=['POST'])
def youtubeinfo():
    url = request.form.get('urlInput')
    if 'watch?v' in url:
        try:
            yt = YouTube(url)
            optional_info = request.form.get('optional')
            info = get_video_info(yt, url, optional_info)
        except:
            info = None
        return render_template('info.html', context=info)
    elif 'playlist?' in url:
        try:
            video_list = []
            playlist = Playlist(url)
            optional_info = request.form.get('optional')
            info = {
                    'status': 200,
                    'url': url,
                    'channel_url': playlist.owner_url,
                    'channel_title': playlist.owner,
                    'title': playlist.title,
                    }
            for video in playlist.video_urls:
                video_list.append(get_video_info(YouTube(video), video, optional_info))
            info['videos'] = video_list
        except:
            info = {'channel_title': 'Нет доступа, возможно Вы пытаетесь получить доступ к закрытому плейлисту',
                    'channel_url': '/'}
        return render_template('info-playlist.html', context=info)
    else:
        info = {
            'status': 404,
            'channel_title': 'Нет доступа, необходимо указывать ссылку на видео или плейлист',
            'channel_url': '/'}
        return render_template('info.html', context=info)


@app.route('/download', methods=['POST', 'GET'])
def download():
    url = request.form.get('url')
    yt = YouTube(url)
    yt.register_on_progress_callback(on_progress)
    yd = yt.streams.get_highest_resolution()
    file_path = yd.download(os.path.join(BASE_DIR, 'downloads'))
    return {'file_path': file_path}


if __name__ == '__main__':
    app.run(debug=True)
