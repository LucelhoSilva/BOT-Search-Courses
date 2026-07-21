"""Coleta cursos gratuitos do catálogo da Coursera."""

import httpx
from bs4 import BeautifulSoup

BASE_URL = 'https://www.coursera.org'
SEARCH_URL = (
    f'{BASE_URL}/courses'
    '?query=free'
    '&topic=Computer%20Science'
    '&topic=Data%20Science'
    '&topic=Information%20Technology'
    '&topic=Math%20and%20Logic'
    '&topic=Personal%20Development'
)
TOTAL_PAGES = 84

CARD_CLASS = 'cds-9 css-0 cds-11 cds-grid-item cds-56 cds-64 cds-76'
CONTENT_CLASS = 'cds-ProductCard-content'
COMPANY_CLASS = 'cds-119 cds-ProductCard-partnerNames css-dmxkm1 cds-121'
TITLE_CLASS = 'cds-119 cds-CommonCard-title css-e7lgfl cds-121'
LINK_CLASS = 'cds-119 cds-113 cds-115 cds-CommonCard-titleLink css-si869u cds-142'
SKILLS_CLASS = 'cds-CommonCard-bodyContent'
METADATA_CLASS = 'cds-CommonCard-metadata'

SKILLS_PREFIX = "Skills you'll gain: "
SKILLS_FALLBACK = 'Descrição não disponível'


async def get_cursera_courses() -> list:
    """Percorre as páginas do catálogo e devolve os cursos encontrados.

    Returns:
        Lista de cursos no formato ``[empresa, título, link, habilidades, descrição]``.
    """
    courses = []

    for page in range(1, TOTAL_PAGES):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{SEARCH_URL}&page={page}')
            soup = BeautifulSoup(response.text, 'html.parser')
            cells = soup.find_all('li', class_=CARD_CLASS)

            for cell in cells:
                card = cell.find('div', class_=CONTENT_CLASS)
                if not card:
                    continue

                company = card.find('p', class_=COMPANY_CLASS).get_text()
                title = card.find('h3', class_=TITLE_CLASS).get_text()
                link = BASE_URL + card.find('a', class_=LINK_CLASS).get('href')

                skills_tag = card.find('div', class_=SKILLS_CLASS)
                skills = skills_tag.get_text().strip() if skills_tag else SKILLS_FALLBACK
                skills = skills.replace(SKILLS_PREFIX, '')

                description = card.find('div', class_=METADATA_CLASS).get_text(strip=True)

                courses.append([company, title, link, skills, description])

    return courses
