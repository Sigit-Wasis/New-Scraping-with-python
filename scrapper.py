#  scrapper ini untuk mengabil url dari web

import requests, json # untuk melakukan permintaan HTTP
from bs4 import BeautifulSoup # untuk menangani semua pemrosesan HTML Anda

def get(url):
    request = requests.get(url) 
    content = request.content
    return BeautifulSoup(content, "html5lib")