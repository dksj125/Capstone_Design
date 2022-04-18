from pytube import YouTube


def download_video(url):
    Download_Folder = "../Movie"

    pl = YouTube("https://www.youtube.com/" + url)

    stream = pl.streams.get_highest_resolution()
    stream.download(Download_Folder)


# 플레이 리스트 저장
#for video in pl.videos:
#    video.streams.first().download(Download_Folder)