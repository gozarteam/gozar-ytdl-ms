import yt_dlp

yt_dlt_default_opts = {
    "outtmpl": "yt.py.mp4",
    "format": "mp4",
}


def download(url, opts=yt_dlt_default_opts): ...
