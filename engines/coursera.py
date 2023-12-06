import httpx
from bs4 import BeautifulSoup

async def get_cursera_courses() -> list:

    courses = []

    for page in range (1, 84):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'https://www.coursera.org/courses?query=free&page={page}&topic=Computer%20Science&topic=Data%20Science&topic=Information%20Technology&topic=Math%20and%20Logic&topic=Personal%20Development')
            soup = BeautifulSoup(response.text, "html.parser")
            cells = soup.find_all("li", class_="cds-9 css-0 cds-11 cds-grid-item cds-56 cds-64 cds-76")

            for cell in cells:
                curses = cell.find("div", class_="cds-ProductCard-content")
                if curses:
                    company = curses.find("p", class_="cds-119 cds-ProductCard-partnerNames css-dmxkm1 cds-121").get_text()
                    title = curses.find("h3", class_="cds-119 cds-CommonCard-title css-e7lgfl cds-121").get_text()
                    link = curses.find("a", class_="cds-119 cds-113 cds-115 cds-CommonCard-titleLink css-si869u cds-142").get('href')
                    link = f'https://www.coursera.org{link}'

                    descricao_element = curses.find("div", class_="cds-CommonCard-bodyContent")
                    descricao = descricao_element.get_text().strip() if descricao_element else "Descrição não disponível"

                    course = [company, title, link, descricao]
                    courses.append(course)


    return courses