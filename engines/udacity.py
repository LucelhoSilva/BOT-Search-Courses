"""Coleta cursos gratuitos da Udacity a partir da API de catálogo."""

import httpx

COURSE_KEYS = [
    'ep245', 'ud1110', 'ud120', 'st101', 'cs271', 'ud509', 'ud282', 'ud170',
    'ud803', 'ud198', 'cs215', 'ud187', 'ud9012', 'ud001', 'cs373', 'ud617',
    'ud123', 'ud9011', 'ud905', 'ud893', 'cs212', 'ud262', 'ud501', 'ud849',
]
CATALOG_URL = f'https://www.udacity.com/api/get-catalog-item?keys={",".join(COURSE_KEYS)}'
COURSE_BASE_URL = 'https://www.udacity.com/course'


async def get_udacity_courses() -> list:
    """Consulta o catálogo e devolve os cursos correspondentes a ``COURSE_KEYS``.

    Returns:
        Lista de cursos no formato ``[código, título, link]``.
    """
    courses = []

    async with httpx.AsyncClient() as client:
        response = await client.get(CATALOG_URL)
        json_response = response.json()

        for item in json_response:
            code = item['key']
            title = item['title']
            link = f'{COURSE_BASE_URL}/{item["slug"]}'

            courses.append([code, title, link])

    return courses
