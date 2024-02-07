import requests
import selectorlib
import time
import sqlite3

URL = "https://programmer100.pythonanywhere.com/tours/"


class Event:
    def scrape(self, url):
        """Scrape the page from the URL."""
        response = requests.get(url)
        source = response.text
        return source

    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tour"]
        return value


class DataBase:
    def __init__(self, database_path):
        self.connection = sqlite3.connect(database_path)

    def store(self, extracted):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events Values(?,?,?)", extracted)
        self.connection.commit()

    def read(self, extracted):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE"
                       " band=? AND city=? AND date=?", extracted)
        return cursor.fetchall()


if __name__ == "__main__":
    while True:
        event = Event()
        database = DataBase(database_path="data.db")
        scraped = event.scrape(URL)
        extracted = event.extract(scraped)
        if extracted != "No upcoming tours":
            extracted = extracted.split(",")
            extracted = [item.strip() for item in extracted]
            dtbs = database.read(extracted)
            if not dtbs:
                database.store(extracted)
        time.sleep(3)
