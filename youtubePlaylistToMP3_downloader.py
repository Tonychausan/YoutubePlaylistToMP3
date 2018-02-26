import os
import json
import youtube_dl


class YoutubePlaylistToMp3Downlaoder:
    def __init__(self, music_folder, playlist_url):
        self.playlist_info_filename = 'playlist_info.json'

        self.music_folder = music_folder
        self.playlist_url = playlist_url
        self.playlist_info_json_filename = '{}/{}'.format(music_folder, self.playlist_info_filename)

        self.download_url_map = {}

    def create_playlist_info_json_file(self):
        print('Creating JSON-file...')

        create_json_command = 'youtube-dl --flat-playlist --dump-single-json {} > {}'.format(self.playlist_url, self.playlist_info_json_filename)
        os.system(create_json_command)

        print('Created JSON-file: {}\n'.format(self.playlist_info_json_filename))

    def get_url_list_from_json_file(self, filename):
        with open(filename) as json_data:
            parsed_json = json.load(json_data)

        video_url_list = {}
        for video_info in parsed_json['entries']:
            video_id = video_info['id']
            title = video_info['title']
            if video_id not in video_url_list:
                video_url_list[video_id] = title

        return video_url_list

    def filter_map(self, full_map, exclude_map):
        new_map = {}
        for key, value in full_map.items():
            if key not in exclude_map:
                new_map[key] = value

        return new_map

    def download_mp3_from_url_list(self):
        print('Videos to download: {}'.format(len(self.download_url_map)))
        print('Download Start...')

        ydl_opts = {
            'outtmpl': 'music/%(id)s#%(title)s.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        youtube_video_links = []
        for url in self.download_url_map:
            link = 'https://www.youtube.com/watch?v={}'.format(url)
            youtube_video_links.append(link)

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(youtube_video_links)

        print('Download finished...')

    def get_predownloaded_files_map(self):
        file_list = self.get_mp3_files_in_music_folder()

        predownloaded_files_map = {}
        for filename in file_list:
            (key, value) = filename.split('#', 1)

            if(key not in predownloaded_files_map):
                # Remove mp3 from value
                predownloaded_files_map[key] = value[:len(value) - len('.mp3')]

        return predownloaded_files_map

    def delete_files_not_in_playlist(self, file_map, playlist_map):
        copy_map = self.filter_map(file_map, playlist_map)
        print()
        for key, value in copy_map.items():
            filename = '{}#{}.mp3'.format(key, value)
            # Remove file
            os.remove('{}/{}'.format(self.music_folder, filename))
            # Remove from map
            del file_map[key]
            print('Removed file: {}'.format(filename))
        print()

    def start_download(self):
        # Create
        if not os.path.exists(self.music_folder):
            os.makedirs(self.music_folder)

        # Create JSON-file with playlist info
        self.create_playlist_info_json_file()
        video_url_list = self.get_url_list_from_json_file(self.playlist_info_json_filename)

        predownloaded_files_map = self.get_predownloaded_files_map()
        self.delete_files_not_in_playlist(predownloaded_files_map, video_url_list)

        # Excludes videos downloaded on earlier run
        self.download_url_map = self.filter_map(video_url_list, predownloaded_files_map)

        # Download list
        self.download_mp3_from_url_list()

    def get_mp3_files_in_music_folder(self):
        file_list = []
        for (dirpath, dirnames, filenames) in os.walk(self.music_folder):
            file_list.extend(filenames)
            break

        # Filter filename that ends with <.mp3>
        file_list = [file for file in file_list if file.endswith(".mp3")]

        return file_list
