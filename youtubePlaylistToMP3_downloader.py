import os
import json
import shutil
import youtube_dl


class YoutubePlaylistToMp3Downlaoder:
    def __init__(self, music_folder, playlist_url):
        self.music_folder = music_folder
        self.playlist_url = playlist_url
        self.playlist_info_json_filename = '{}/playlist_info.json'.format(music_folder)
        self.download_check_json_filename = '{}/download_check.json'.format(music_folder)

        self.download_url_list = []

    def create_playlist_info_json_file(self):
        print('Creating JSON-file...')

        create_json_command = 'youtube-dl --flat-playlist --dump-single-json {} > {}'.format(self.playlist_url, self.playlist_info_json_filename)
        os.system(create_json_command)

        print('Created JSON-file: {}\n'.format(self.playlist_info_json_filename))

    def get_url_list_from_json_file(self, filename):
        with open(filename) as json_data:
            parsed_json = json.load(json_data)

        video_url_list = []
        for video_info in parsed_json['entries']:
            video_url_list.append(video_info['url'])

        return video_url_list

    def filter_list(self, full_list, excludes):
        return [x for x in full_list if x not in excludes]

    def download_mp3_from_url_list(self):
        print('Videos to download: {}'.format(len(self.download_url_list)))
        print('Download Start...')

        ydl_opts = {
            'outtmpl': 'music/%(title)s.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        youtube_video_links = []
        for url in self.download_url_list:
            link = 'https://www.youtube.com/watch?v={}'.format(url)
            youtube_video_links.append(link)

        # for link in youtube_video_links:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(youtube_video_links)

        print('Download finished...')

    def start_download(self):
        # Create
        if not os.path.exists(self.music_folder):
            os.makedirs(self.music_folder)

        # Create JSON-file with playlist info
        self.create_playlist_info_json_file()

        video_url_list = self.get_url_list_from_json_file(self.playlist_info_json_filename)

        # Excludes videos downloaded on earlier run
        video_url_check_list = []
        if os.path.isfile(self.download_check_json_filename):
            video_url_check_list = self.get_url_list_from_json_file(self.download_check_json_filename)
        self.download_url_list = self.filter_list(video_url_list, video_url_check_list)

        # Download list
        self.download_mp3_from_url_list()

        # Update exclude list
        shutil.copy(self.playlist_info_json_filename, self.download_check_json_filename)
