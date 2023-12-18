import httpx

async def get_udacity_courses() -> list:

    courses = []

    async with httpx.AsyncClient() as client:
        response = await client.get('https://www.udacity.com/api/get-catalog-item?keys=ep245,ud1110,ud120,st101,cs271,ud509,ud282,ud170,ud803,ud198,cs215,ud187,ud9012,ud001,cs373,ud617,ud123,ud9011,ud905,ud893,cs212,ud262,ud501,ud849')
        json_reponse = response.json()

        for course in json_reponse:
            code = course['key']
            title = course['title']
            url = course['slug']
            link = f'https://www.udacity.com/course/{url}'

            course = [code, title, link]
            courses.append(course)

    return courses




