import requests
from bs4 import BeautifulSoup

def get_udacity() -> list: 

    response = requests.get('https://www.udacity.com/api/get-catalog-item?keys=ep245,ud1110,ud120,st101,cs271,ud509,ud282,ud170,ud803,ud198,cs215,ud187,ud9012,ud001,cs373,ud617,ud123,ud9011,ud905,ud893,cs212,ud262,ud501,ud849')
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup)

get_udacity()

