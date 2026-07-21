"""Coleta os cursos gratuitos publicados pelo Curso em Vídeo."""

import httpx
from bs4 import BeautifulSoup

COURSES_URL = 'https://www.cursoemvideo.com/cursos/'
CARD_CLASS = 'fl-post-column'


async def get_cursoemvideo_courses() -> list:
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
            link = cell.find('a').get('href')
            title = cell.find('h3').get_text(strip=True)

            courses.append([title, link])

    return courses
