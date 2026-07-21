"""Coleta os cursos gratuitos publicados pela HRBR Cursos."""

import httpx
from bs4 import BeautifulSoup

COURSES_URL = 'https://www.hrbrcursos.com/cursos/'
CARD_CLASS = 'pp-content-grid-inner pp-content-body clearfix'


async def get_hrbrcursos_courses() -> list:
    """Devolve os cursos listados na página de cursos.

    Returns:
        Lista de cursos no formato ``[título, link]``.
    """
    courses = []

    async with httpx.AsyncClient() as client:
        response = await client.get(COURSES_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        cells = soup.find_all('div', class_=CARD_CLASS)

        for cell in cells:
            title = cell.find('h3').get_text(strip=True)
            link = cell.find('a').get('href')

            courses.append([title, link])

    return courses
