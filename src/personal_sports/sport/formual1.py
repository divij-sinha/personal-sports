import json
import logging
import pathlib
import pickle

import httpx
from whenever import PlainDateTime

from personal_sports import utils

data_dir = pathlib.Path(__file__).parent.parent.parent / "data"

logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


def parse_f1_calendar_row(title: str, row: str, source_url: str):
    """Parses a row from the Formula 1 calendar page.
    Args:
        title (str): The title of the calendar event.
        row (str): The row containing the date and location information.
    Returns:
        dict: A dictionary containing the parsed information.
    """
    title = title.strip().title()
    row = row.strip()
    event_dm = row[0:5].strip()
    event_date = int(event_dm[:2].strip())
    event_month = utils.month_to_num[event_dm[2:5].strip()]
    if "-" in row:
        date_split = -13
    else:
        date_split = -5
    event_times = row[date_split:].strip().split("-")
    start_time = event_times[0].strip().split(":")
    start_hour = int(start_time[0].strip())
    start_minute = int(start_time[1].strip())

    start_datetime = PlainDateTime(2026, event_month, event_date, start_hour, start_minute)
    start_datetime = start_datetime.assume_tz("America/Chicago").to_tz("UTC")

    event_subtitle = row[5:date_split].strip()
    event_dict = {
        "title": title,
        "subtitle": event_subtitle,
        "start_datetime": start_datetime,
        "source_url": source_url,
    }

    if date_split == -13:
        end_time = event_times[1].strip().split(":")
        end_hour = int(end_time[0].strip())
        end_minute = int(end_time[1].strip())
        end_datetime = PlainDateTime(2026, event_month, event_date, end_hour, end_minute)
        end_datetime = end_datetime.assume_tz("America/Chicago").to_tz("UTC")
        event_dict["end_datetime"] = end_datetime

    return event_dict


def main():
    logger.info("Starting Formula 1 calendar fetch...")
    main_url = "https://www.formula1.com/en/racing/2026"
    xpath_filter = '//div[@class="grid justify-items-stretch items-center gap-px-12 @[738px]/cards:gap-px-16 lg:gap-px-24 grid-cols-1 @[640px]/cards:grid-cols-2 @[1320px]/cards:grid-cols-3"]//a'
    links = utils.extract_from_url(main_url, xpath_filter)[0]
    logger.info(f"Found {len(links)} links on the page.")
    page_xpath_filter = ["//h1", '//ul[contains(@class, "890px]/page:grid-cols")]/li']
    all_events = []
    for link in links:
        cur_link = link.get("href")
        logger.debug(f"Fetching page: {cur_link}")
        cur_url = httpx.URL(main_url).join(cur_link)
        page_info = utils.extract_from_url(cur_url, page_xpath_filter)
        logger.debug(f"Page info: {page_info}")
        title = page_info[0][0].text_content().strip()
        for info in page_info[1]:
            info = info.text_content().strip()
            event_dict = parse_f1_calendar_row(title, info, cur_url)
            all_events.append(event_dict)
    logger.info(f"Parsed {len(all_events)} events for {title}.")

    json.dump(all_events, open(data_dir / "f1_2026_calendar.json", "w"), indent=4, default=str)
    pickle.dump(all_events, open(data_dir / "f1_2026_calendar.pkl", "wb"))

    logger.info("Finished fetching and parsing Formula 1 calendar data.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger.info("Starting Formula 1 data fetch...")
    main()
