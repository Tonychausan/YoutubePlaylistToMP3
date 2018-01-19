from youtubePlaylistToMP3_downloader import YoutubePlaylistToMp3Downlaoder


# Global Parameters
music_folder = 'music'
playlist_url = 'https://www.youtube.com/playlist?list=PLcdukubGAjK4Uaivt_slr9C_csdx5lvKQ'
playlist_info_json_filename = '{}/playlist_info.json'.format(music_folder)
download_check_json_filename = '{}/download_check.json'.format(music_folder)


# Download MP3 from youtube playlist
youtube_playlist_to_mp3_downloader = YoutubePlaylistToMp3Downlaoder(music_folder, playlist_url, playlist_info_json_filename, download_check_json_filename)
youtube_playlist_to_mp3_downloader.start_download()
