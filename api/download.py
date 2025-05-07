import os
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
import yt_dlp
import uuid

app = FastAPI()

@app.get("/api/download")
async def download_twitter_video(url: str):
    if not url:
        return JSONResponse(status_code=400, content={"error": "URL is required"})

    video_id = str(uuid.uuid4())
    output_path = f"/tmp/{video_id}.mp4"

    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
        'merge_output_format': 'mp4',
        'outtmpl': output_path,
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    if not os.path.exists(output_path):
        return JSONResponse(status_code=500, content={"error": "Download failed."})

    return FileResponse(output_path, media_type='video/mp4', filename='twitter_video.mp4')
