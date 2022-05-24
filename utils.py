import asyncio
import os
from datetime import datetime
import pytz
import pandas as pd
import aiofiles
from aiocsv import AsyncDictReader, AsyncDictWriter
import csv

dt_obj = datetime.now(pytz.timezone("Australia/Sydney"))
time_stamp = datetime.strftime(dt_obj, "%Y-%m-%d %H:%M:%S")

temp_data = f"temp_data.csv"
clean_file = f"google_ads_urls_{time_stamp}.csv"


def csv_reader():
    keywords = []
    with open(
        "keywords_for_scraper.csv", mode="r", encoding="utf-8", newline=""
    ) as file:
        data = csv.DictReader(file)
        for col in data:
            keywords.append(col["keywords"])
    return keywords[:5]


def csv_writer(data_obj):
    try:
        with open(temp_data, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=data_obj[0].keys())
            writer.writeheader()

            for row in data_obj:
                writer.writerow(row)
    except:
        pass

    try:
        df = pd.read_csv(temp_data)
        df.drop_duplicates(inplace=True)
        df.to_csv(clean_file, index=False)
    except:
        pass

    os.remove(temp_data)


async def csv_reader(file_path):
    keywords = []
    async with aiofiles.open(file_path, mode="r", encoding="utf-8", newline="") as file:
        data = AsyncDictReader(file)
        async for col in data:
            keywords.append(col["keywords"])
    return keywords


async def csv_writer(data_obj):
    try:
        async with aiofiles.open(
            temp_data, mode="w", encoding="utf-8", newline=""
        ) as file:
            writer = AsyncDictWriter(file, fieldnames=data_obj[0].keys())
            await writer.writeheader()

            for row in data_obj:
                await writer.writerow(row)
    except:
        pass

    try:
        df = pd.read_csv(temp_data)
        df.drop_duplicates(inplace=True)
        df.to_csv(clean_file, index=False)
    except:
        pass

    os.remove(temp_data)


if __name__ == "__main__":
    # file_path = os.path.abspath("keywords_for_scraper.csv")
    # kw = csv_reader(file_path)
    data = [{"Ad_url": "www.google.com"}]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(csv_writer(data))
