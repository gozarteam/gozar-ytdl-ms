from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from fastapi.background import BackgroundTasks
import tempfile
import os
import yt_dlp

from .models import DownloadPayload
from .deps import get_api_key
from .utils import clean_filename


app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Welcome to Gozar Youtube Downloader API! use /download endpoint"
    }


def remove_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)


@app.post("/download")
async def download_video(
    payload: DownloadPayload,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(get_api_key),
):
    file_name = payload.url
    file_name = file_name[file_name.find("v=") :]
    file_name = clean_filename(file_name)
    temp_file_path = os.path.join(
        f"{file_name}.{'mp3' if payload.extractaudio else 'mp4'}"
    )
    ydl_opts = {
        "format": payload.format,
        "outtmpl": temp_file_path,
        "noplaylist": payload.noplaylist,
        "geo_bypass": payload.geo_bypass,
        "extractaudio": payload.extractaudio,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([payload.url])
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to download video: {str(e)}"
        )
    background_tasks.add_task(remove_file, temp_file_path)
    return FileResponse(
        temp_file_path, media_type="video/mp4", filename=f"{file_name}.mp4"
    )
