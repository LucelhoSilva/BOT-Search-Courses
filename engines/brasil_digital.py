import httpx
from bs4 import BeautifulSoup

async def get_brasil_digital_courses() -> list:
    
    courses = []   
    stacks = ['informatica', 'carga-horaria-de-80-horas']

    for stack in stacks:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'https://www.unovacursos.com.br/segmento/{stack}')
            soup = BeautifulSoup(response.text, "html.parser")
            cells = soup.find_all("article", class_="card card_course jmore_courses")

            for cell in cells:
                title = cell.find("h5").get_text(strip=True)
                link = cell.find("a").get('href')

            course = [title, link]
            courses.append(course)

    return courses


    