from bs4 import BeautifulSoup
import httpx
import asyncio

async def get_freecodecamp() -> list:
  async with httpx.AsyncClient() as client:
    response = await client.get('https://www.freecodecamp.org/portuguese/learn/')
    curses = []

    soup = BeautifulSoup(response.content, 'html.parser')
    cells = soup.find_all('li', class_="curriculum-map-button")
    for cell in cells:
      link = cell.find("a").get('href')
      curses.append([link])
  return curses


async def main():
  jobs = await get_freecodecamp()
  for job in jobs:
    print(job)

if __name__ == "__main__":
  asyncio.run(main())
