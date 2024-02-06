import requests
import selectorlib
import time
import sqlite3

URL = "https://programmer100.pythonanywhere.com/tours/"
connection = sqlite3.connect("data.db")

def scrape(url):
    """Scrape the page from the URL."""
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tour"]
    return value


def store(extracted):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events Values(?,?,?)", extracted)
    connection.commit()


def read(extracted):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",extracted)
    return cursor.fetchall()


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        if extracted != "No upcoming tours":
            extracted = extracted.split(",")
            extracted = [item.strip() for item in extracted]
            dtbs = read(extracted)
            if not dtbs:
                store(extracted)
        time.sleep(3)
