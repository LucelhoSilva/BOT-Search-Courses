import discord
import asyncio
import keyring
from discord.ext import commands

from engines.udemy import get_udemy_courses

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
channel_id = 1181318614087897221

sent_courses = []

async def search_cursos():
    '''
    Assynchronous function that searches for new jobs every 60 seconds and sends them to the Discord channel.
    The function searches for vacancies in the following websites:
    * udemy
    '''
    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id)
    while not bot.is_closed():

        # Udemy
        results = await get_udemy_courses()
        for result in results:
            if result[0] not in sent_courses:
                sent_courses.append(result[0])
                course_info = f'{"-"*50}\n\nCURSO: {result[0]}\nLINK: {result[1]}'
                await channel.send(course_info)
                await asyncio.sleep(60)
        await asyncio.sleep(60)


@bot.event
async def on_ready():
    bot.loop.create_task(search_cursos())

bot.run('MTE0NDgyNTY3NzQ2NDQ4MTgxMw.GFsZ4M.VkQvQ6CeSYpNRLIxmhVnAGV8XlwnTcT5aP9pWE')
