import hikari
from hikari import intents
import asyncio
import keyring

from engines.udemy import get_udemy_courses
from engines.coursera import get_cursera_courses
from engines.cursoemvideo import get_cursoemvideo_courses
from engines.hrbrcursos import get_hrbrcursos_courses

bot = hikari.GatewayBot(keyring.get_password('bot_cursos', 'token'), intents=intents.Intents.ALL)
channel_id = keyring.get_password('bot_cursos', 'channel')

sent_courses = []

@bot.listen()
async def on_started(event: hikari.StartedEvent) -> None:
    '''
    Assynchronous function that searches for new jobs every 60 seconds and sends them to the Discord channel.
    The function searches for vacancies in the following websites:
    * Curso em Vídeo
    * HRBR Cursos
    * Coursera
    '''

    # Coursera
    results = await get_cursera_courses()
    for result in results:
        if result[0] not in sent_courses:
            sent_courses.append(result[0])
            course_info = f'{"-"*50}\n\nEMPRESA: {result[0]}\nCURSO: {result[1]}\nLINK: {result[2]}\nDESCRIÇÃO: {result[3]}'
            await bot.rest.create_message(channel_id, course_info)
            await asyncio.sleep(60)
    await asyncio.sleep(60)
    
    # Curso em Vídeo
    results = await get_cursoemvideo_courses()
    for result in results:
        if result[0] not in sent_courses:
            sent_courses.append(result[0])
            course_info = f'{"-"*50}\n\nCURSO: {result[0]}\nLINK: {result[1]}'
            await bot.rest.create_message(channel_id, course_info)
            await asyncio.sleep(60)
    await asyncio.sleep(60)

    # HRBR Cursos
    results = await get_hrbrcursos_courses()
    for result in results:
        if result[0] not in sent_courses:
            sent_courses.append(result[0])
            course_info = f'{"-"*50}\n\nCURSO: {result[0]}\nLINK: {result[1]}'
            await bot.rest.create_message(channel_id, course_info)
            await asyncio.sleep(60)
    await asyncio.sleep(60)

    # Udemy
    results = await get_udemy_courses()
    for result in results:
        if result[0] not in sent_courses:
            sent_courses.append(result[0])
            course_info = f'{"-"*50}\n\nCURSO: {result[0]}\nLINK: {result[1]}'
            await bot.rest.create_message(channel_id, course_info)
            await asyncio.sleep(60)
    await asyncio.sleep(60)

bot.run()
