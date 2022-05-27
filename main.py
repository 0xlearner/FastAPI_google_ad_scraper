from typing import List
import fastapi as _fastapi
from fastapi.responses import HTMLResponse, FileResponse, Response
from starlette.requests import Request
from starlette.templating import Jinja2Templates
import shutil
import os
import json

from rq import Queue
from rq.job import Job

from redis import Redis

from scraper import run_scraper
from utils import clean_file, csv_writer

app = _fastapi.FastAPI()

r = Redis(
    host="localhost",
    port=6379,
    db=0,
)
q = Queue(connection=r, default_timeout=-1)

templates = Jinja2Templates("templates")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/v1/scraped_csv")
async def extract_ads(csv_file: _fastapi.UploadFile = _fastapi.File(...)):
    temp_file = _save_file_to_disk(csv_file, path="temp", save_as="temp")
    job = q.enqueue(run_scraper, temp_file)

    return {"message": "Scraping has been started", "job_id": job.id}


@app.get("/progress/{job_id}")
def progress(job_id):
    job = Job.fetch(job_id, connection=r)
    if job.is_finished:
        csv_path = os.path.abspath(clean_file)
        return FileResponse(path=csv_path, media_type="text/csv", filename=clean_file)
    return {"message": "Scraper is running."}


def _save_file_to_disk(uploaded_file, path=".", save_as="default"):
    extension = os.path.splitext(uploaded_file.filename)[-1]
    temp_file = os.path.join(path, save_as + extension)
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return temp_file
