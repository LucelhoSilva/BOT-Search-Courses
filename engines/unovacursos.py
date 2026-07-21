"""Coleta cursos gratuitos dos segmentos selecionados da Unova Cursos."""

import httpx
from bs4 import BeautifulSoup

BASE_URL = 'https://www.unovacursos.com.br/segmento'
STACKS = ['informatica', 'carga-horaria-de-80-horas']
CARD_CLASS = 'card card_course jmore_courses'


async def get_unovacursos_courses() -> list:
    """Percorre os segmentos em ``STACKS`` e devolve os cursos encontrados.

    Returns:
        Lista de cursos no formato ``[título, link]``.
    """
    courses = []

    for stack in STACKS:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{BASE_URL}/%7Bstack%7D')
            soup = BeautifulSoup(response.text, 'html.parser')
            cells = soup.find_all('article', class_=CARD_CLASS)

            for cell in cells:
                title = cell.find('h5').get_text(strip=True)
                link = cell.find('a').get('href')

            courses.append([title, link])

    return courses
