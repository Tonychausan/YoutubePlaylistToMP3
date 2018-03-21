from youtubePlaylistToMP3_downloader import YoutubePlaylistToMp3Downlaoder
from mp3FileTransfer import mp3FileTransfer

# Global Parameters
music_folder = 'music'
playlist_url = 'https://www.youtube.com/playlist?list=PLcdukubGAjK4Uaivt_slr9C_csdx5lvKQ'

# Download MP3 from youtube playlist
youtube_playlist_to_mp3_downloader = YoutubePlaylistToMp3Downlaoder(music_folder, playlist_url)
youtube_playlist_to_mp3_downloader.start_download()
mp3 = mp3FileTransfer('music')
mp3.startFileTransfer()
