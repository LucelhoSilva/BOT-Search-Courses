import httpx
from bs4 import BeautifulSoup

courses = []


async def get_hrbrcursos_courses() -> list:
  
  async with httpx.AsyncClient() as client:
    response = await client.get(f'https://www.hrbrcursos.com/cursos/')
    soup = BeautifulSoup(response.text, 'html.parser')

    cells = soup.find_all('div', class_="pp-content-grid-inner pp-content-body clearfix")
    for cell in cells :
        title = cell.find('h3').get_text(strip=True)
        link = cell.find('a').get('href')

        course = [title, link]
        courses.append(course)


    return courses
