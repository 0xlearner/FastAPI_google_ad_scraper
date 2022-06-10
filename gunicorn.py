import multiprocessing
import os
from dotenv import load_dotenv
load_dotenv()

name = "gunicorn config for FastAPI - TutLinks.com"
accesslog = "/root/fastapi_google_ads_scraper/google_ad_scraper/gunicorn-access.log"
errorlog = "/root/fastapi_google_ads_scraper/google_ad_scraper/gunicorn-error.log"

bind = "0.0.0.0:8000"

worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count () * 2 + 1
worker_connections = 1024
backlog = 2048
max_requests = 5120
timeout = 0
keepalive = 2

debug = os.environ.get("debug", "false") == "true"
reload = debug
preload_app = False
daemon = False
