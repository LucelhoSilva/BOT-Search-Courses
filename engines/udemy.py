import httpx
from bs4 import BeautifulSoup


async def get_udemy_courses() -> list:
    base_url = "https://www.udemyfreebies.com/"
    courses = []

    for page in range(1, 176):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{base_url}free-udemy-courses/{page}')
            soup = BeautifulSoup(response.content, 'html.parser')

            cells = soup.find_all("div", class_="theme-block")

            for cell in cells:
                title = cell.find("h4").get_text(strip=True)
                link = cell.find("a").get('href')
                link = link.replace('free-udemy-course', 'out')

                course = [title, link]
                courses.append(course)

    return courses
