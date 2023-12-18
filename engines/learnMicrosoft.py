import httpx
from bs4 import BeautifulSoup

async def get_learnMicrosft_courses():

    courses = []

    for page in range(0, 4800, 30):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'https://learn.microsoft.com/api/contentbrowser/search?environment=prod&locale=en-us&facet=roles&facet=levels&facet=products&facet=subjects&facet=resource_type&%24skip={page}&%24top=30&showHidden=false&fuzzySearch=false')
            json_response = response.json()
            for job in json_response['results']:
            
                title = job['title']
                url = job['url']
                link = f'https://learn.microsoft.com/pt-br'+url
                level = ', '.join(job['display_levels'])
                stack = ', '.join(job['display_roles'])

                course = [title, level, stack, link]
                courses.append(course)

    return courses

