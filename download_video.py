from pytube import YouTube


def download_video(url, genre):
    Download_Folder = "./Movie/" + genre

    pl = YouTube("https://www.youtube.com/" + url)

    stream = pl.streams.get_highest_resolution()
    stream.download(Download_Folder)


# 플레이 리스트 저장
#for video in pl.videos:
#    video.streams.first().download(Download_Folder)