"""Coleta trilhas e módulos gratuitos da API pública do Microsoft Learn."""

import httpx

SEARCH_URL = (
    'https://learn.microsoft.com/api/contentbrowser/search'
    '?environment=prod'
    '&locale=en-us'
    '&facet=roles'
    '&facet=levels'
    '&facet=products'
    '&facet=subjects'
    '&facet=resource_type'
    '&showHidden=false'
    '&fuzzySearch=false'
)
COURSE_BASE_URL = 'https://learn.microsoft.com/pt-br'

PAGE_SIZE = 30
TOTAL_ITEMS = 4800


async def get_learnMicrosft_courses() -> list:
    """Pagina a API de conteúdo e devolve os cursos encontrados.

    Returns:
        Lista de cursos no formato ``[título, nível, stack, link]``.
    """
    courses = []

    for skip in range(0, TOTAL_ITEMS, PAGE_SIZE):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{SEARCH_URL}&%24skip={skip}&%24top={PAGE_SIZE}')
            json_response = response.json()

            for item in json_response['results']:
                title = item['title']
                link = COURSE_BASE_URL + item['url']
                level = ', '.join(item['display_levels'])
                stack = ', '.join(item['display_roles'])

                courses.append([title, level, stack, link])

    return courses
