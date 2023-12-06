import httpx
from bs4 import BeautifulSoup

courses = []

async def get_cursoemvideo_courses() -> list:
  
  async with httpx.AsyncClient() as client:
    response = await client.get(f'https://www.cursoemvideo.com/cursos/')
    soup = BeautifulSoup(response.text, "html.parser")
  
    cells = soup.find_all("div", class_="fl-post-column")
    for cell in cells:
      link = cell.find("a").get('href')
      title = cell.find("h3").get_text(strip=True)
      
      course = [title, link]
      courses.append(course)

  return courses