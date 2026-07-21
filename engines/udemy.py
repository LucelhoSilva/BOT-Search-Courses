"""Coleta cupons de cursos gratuitos da Udemy via Udemy Freebies."""

import httpx
from bs4 import BeautifulSoup

BASE_URL = 'https://www.udemyfreebies.com'
TOTAL_PAGES = 176
CARD_CLASS = 'theme-block'

# O site publica o link na rota de detalhe; /out leva direto ao cupom da Udemy.
DETAIL_PATH = 'free-udemy-course'
REDIRECT_PATH = 'out'


async def get_udemy_courses() -> list:
    """Percorre as páginas de cursos gratuitos e devolve os cursos encontrados.

    Returns:
        Lista de cursos no formato ``[título, link]``.
    """
    courses = []

    for page in range(1, TOTAL_PAGES):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{BASE_URL}/free-udemy-courses/{page}')
            soup = BeautifulSoup(response.content, 'html.parser')
            cells = soup.find_all('div', class_=CARD_CLASS)

            for cell in cells:
                title = cell.find('h4').get_text(strip=True)
                link = cell.find('a').get('href').replace(DETAIL_PATH, REDIRECT_PATH)

                courses.append([title, link])

    return courses
