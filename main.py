from typing import List
import fastapi as _fastapi
from fastapi.responses import HTMLResponse, FileResponse
import shutil
import os

from scraper import run_scraper
from utils import clean_file, csv_writer

app = _fastapi.FastAPI()


@app.get("/")
def index():
    content = """
<body>
<form method="post" action="/api/v1/scraped_csv" enctype="multipart/form-data">
<input name="csv_file" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


@app.post("/api/v1/scraped_csv")
async def extract_ads(csv_file: _fastapi.UploadFile = _fastapi.File(...)):
    temp_file = _save_file_to_disk(csv_file, path="temp", save_as="temp")
    await run_scraper(temp_file)
    csv_path = os.path.abspath(clean_file)
    return FileResponse(path=csv_path, media_type="text/csv", filename=clean_file)


def _save_file_to_disk(uploaded_file, path=".", save_as="default"):
    extension = os.path.splitext(uploaded_file.filename)[-1]
    temp_file = os.path.join(path, save_as + extension)
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return temp_file
