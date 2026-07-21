"""Bot do Discord que publica cursos gratuitos coletados de várias plataformas."""

import asyncio

import hikari
import keyring
from hikari import intents

from engines.coursera import get_cursera_courses
from engines.cursoemvideo import get_cursoemvideo_courses
from engines.hrbrcursos import get_hrbrcursos_courses
from engines.learnMicrosoft import get_learnMicrosft_courses
from engines.udacity import get_udacity_courses
from engines.udemy import get_udemy_courses
from engines.unovacursos import get_unovacursos_courses

KEYRING_SERVICE = 'bot_cursos'
SEND_INTERVAL_SECONDS = 60
SEPARATOR = '-' * 50

bot = hikari.GatewayBot(
    keyring.get_password(KEYRING_SERVICE, 'token'),
    intents=intents.Intents.ALL,
)
channel_id = keyring.get_password(KEYRING_SERVICE, 'channel')

# Títulos (ou códigos) já publicados, para não repetir o mesmo curso no canal.
sent_courses = []


def format_simple_course(course: list) -> str:
    """Formata cursos que trazem apenas ``[título, link]``."""
    return f'{SEPARATOR}\n\nCURSO: {course[0]}\nLINK: {course[1]}'


def format_coursera_course(course: list) -> str:
    """Formata cursos da Coursera: ``[empresa, título, link, habilidades, descrição]``."""
    return (
        f'{SEPARATOR}\n\n'
        f'EMPRESA: {course[0]}\n'
        f'CURSO: {course[1]}\n'
        f'LINK: {course[2]}\n'
        f'HABILIDADES QUE VOCÊ TERÁ: {course[3]}\n'
        f'DESCRIÇÃO: {course[4]}'
    )


def format_learn_microsoft_course(course: list) -> str:
    """Formata cursos do Microsoft Learn: ``[título, nível, stack, link]``."""
    return (
        f'{SEPARATOR}\n\n'
        f'CURSO: {course[0]}\n'
        f'DIFICULDADE: {course[1]}\n'
        f'STACK: {course[2]}\n'
        f'LINK: {course[3]}'
    )


def format_udacity_course(course: list) -> str:
    """Formata cursos da Udacity: ``[código, título, link]``."""
    return f'{SEPARATOR}\n\nCURSO: {course[1]}\nLINK: {course[2]}'


# Ordem em que as plataformas são consultadas: (coletor, formatador da mensagem).
COURSE_SOURCES = [
    (get_cursera_courses, format_coursera_course),
    (get_cursoemvideo_courses, format_simple_course),
    (get_hrbrcursos_courses, format_simple_course),
    (get_learnMicrosft_courses, format_learn_microsoft_course),
    (get_udacity_courses, format_udacity_course),
    (get_unovacursos_courses, format_simple_course),
    (get_udemy_courses, format_simple_course),
]


async def publish_courses(courses: list, format_course) -> None:
    """Envia ao canal os cursos ainda não publicados, um a cada minuto.

    Args:
        courses: Cursos devolvidos por uma engine.
        format_course: Função que transforma o curso na mensagem do Discord.
    """
    for course in courses:
        identifier = course[0]
        if identifier in sent_courses:
            continue

        sent_courses.append(identifier)
        await bot.rest.create_message(channel_id, format_course(course))
        await asyncio.sleep(SEND_INTERVAL_SECONDS)


@bot.listen()
async def on_started(event: hikari.StartedEvent) -> None:
    """Consulta cada plataforma de ``COURSE_SOURCES`` e publica os cursos novos.

    As plataformas são percorridas em sequência, com uma pausa de um minuto
    entre cada mensagem e entre uma plataforma e a seguinte, para respeitar o
    rate limit do Discord.
    """
    for get_courses, format_course in COURSE_SOURCES:
        courses = await get_courses()
        await publish_courses(courses, format_course)
        await asyncio.sleep(SEND_INTERVAL_SECONDS)


bot.run()
