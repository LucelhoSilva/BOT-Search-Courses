import requests

from bs4 import BeautifulSoup

courses = []

def get_freecodecamp() -> list:

  response = requests.get('https://www.freecodecamp.org/portuguese/learn/')
  soup = BeautifulSoup(response.text, "html.parser")
  print(soup)


get_freecodecamp()
