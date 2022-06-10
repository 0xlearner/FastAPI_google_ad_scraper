from typing import List
import fastapi as _fastapi
from fastapi.responses import HTMLResponse, FileResponse, Response, RedirectResponse, StreamingResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import shutil
import os
import time

from rq import Queue, Retry
from rq.job import Job

from redis import Redis

from scraper import get_google_ad_urls
from utils import clean_file, csv_writer

app = _fastapi.FastAPI()

r = Redis()
q = Queue(connection=r, default_timeout=-1)

templates = Jinja2Templates("templates")

app.mount("/static", StaticFiles(directory="static"), name="static")




@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/v1/scraped_csv")
async def extract_ads(csv_file: _fastapi.UploadFile = _fastapi.File(...)):
    temp_file = _save_file_to_disk(csv_file, path="temp", save_as="temp")
    task = q.enqueue(get_google_ad_urls, temp_file, result_ttl=10800)

    return RedirectResponse(f'/progress/{task.id}', status_code=303)
    
    # csv_path = os.path.abspath(clean_file)
    # return FileResponse(path=csv_path, media_type="text/csv", filename=clean_file)


@app.get("/progress/{job_id}")
def progress(request: Request, job_id):
    job = Job.fetch(job_id, connection=r)
    status = job.get_status()
    if job.is_finished:
        csv_path = os.path.abspath(clean_file)
        return FileResponse(path=csv_path, media_type="text/csv", filename=clean_file)
    return templates.TemplateResponse("log_stream.html", {"request": request})


@app.get("/log_stream/")
def stream():
    def iterfile():
        with open("scraper.log") as log_info:
            while True:
                where = log_info.tell()
                line = log_info.readline()
                if not line:
                    time.sleep(0.5)
                    log_info.seek(where)
                else:
                    yield line

   
    return StreamingResponse(iterfile(), media_type="text/plain")


def _save_file_to_disk(uploaded_file, path=".", save_as="default"):
    extension = os.path.splitext(uploaded_file.filename)[-1]
    temp_file = os.path.join(path, save_as + extension)
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return temp_file

if __name__ == "__main__":
    uvicorn.run(app, port=8000, hostname="0.0.0.0")
