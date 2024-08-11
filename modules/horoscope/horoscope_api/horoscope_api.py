import time
from bs4 import BeautifulSoup
import requests

from .cache import Cache

signs = {
    'aries': '1',
    'taurus': '2',
    'gemini': '3',
    'cancer': '4',
    'leo': '5',
    'virgo': '6',
    'libra': '7',
    'scorpio': '8',
    'sagittarius': '9',
    'capricorn': '10',
    'aquarius': '11',
    'pisces': '12'
}

class Horoscope:
    def __init__(self, cacheTTL=20):
        self.url = "https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx"
        self.cache = Cache()
        self.cacheTTL = cacheTTL
        
    def get_horoscope(self, sign):
        # use beautifulsoup to scrape the horoscope
        signCode = signs[sign.lower()]
        key = f"{self.url}?sign={signCode}"
        # check if the horoscope is in the cache
        horoscope = self.cache.get(key)
        if horoscope:
            return horoscope
        # if not, scrape the horoscope
        response = requests.get(key)
        soup = BeautifulSoup(response.text, 'html.parser')
        horoscope = soup.find_all('div', class_='main-horoscope')[0]
        # get p tag
        horoscope = horoscope.find_all('p')[0].text
        # remove the extra white space
        horoscope = horoscope.strip()
        # cache the horoscope
        self.cache.set(key, horoscope, self.cacheTTL)
        return horoscope

