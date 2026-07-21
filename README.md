# Bot de busca de cursos gratuitos 🤖📚

![GitHub](https://img.shields.io/github/license/LucelhoSilva/BOT-Search-Courses)
![GitHub stars](https://img.shields.io/github/stars/LucelhoSilva/BOT-Search-Courses)
![GitHub forks](https://img.shields.io/github/forks/LucelhoSilva/BOT-Search-Courses)
![GitHub issues](https://img.shields.io/github/issues/LucelhoSilva/BOT-Search-Courses)

Bot de Discord que varre plataformas de ensino em busca de cursos gratuitos e
publica cada novidade em um canal, sem repetir cursos já enviados.

## Plataformas monitoradas

| Plataforma | Fonte | Dados publicados |
| --- | --- | --- |
| Coursera | scraping do catálogo | empresa, curso, link, habilidades, descrição |
| Curso em Vídeo | scraping da página de cursos | curso, link |
| HRBR Cursos | scraping da página de cursos | curso, link |
| Microsoft Learn | API pública de conteúdo | curso, dificuldade, stack, link |
| Udacity | API de catálogo | curso, link |
| Unova Cursos | scraping por segmento | curso, link |
| Udemy (Udemy Freebies) | scraping das ofertas gratuitas | curso, link |

## Como funciona

1. Ao iniciar, o bot dispara o evento `on_started` (`main.py`).
2. Cada plataforma listada em `COURSE_SOURCES` é consultada em sequência.
3. Os cursos ainda não publicados são formatados e enviados ao canal, com uma
   pausa de 60 segundos entre mensagens para respeitar o rate limit do Discord.
4. O identificador de cada curso enviado fica em `sent_courses`, evitando repetição.

## Estrutura do projeto

```
BOT-Search-Courses/
├── main.py                    # Bot: orquestra as engines e publica no Discord
├── requirements.txt           # Dependências
└── engines/                   # Um módulo por plataforma
    ├── coursera.py
    ├── cursoemvideo.py
    ├── hrbrcursos.py
    ├── learnMicrosoft.py
    ├── udacity.py
    ├── udemy.py
    └── unovacursos.py
```

Cada engine expõe uma única função assíncrona `get_<plataforma>_courses()` que
devolve uma lista de cursos. O primeiro item de cada curso é o identificador
usado na deduplicação.

## Instalação

```bash
git clone https://github.com/LucelhoSilva/BOT-Search-Courses.git
cd BOT-Search-Courses

python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Configuração

As credenciais não ficam no código: são lidas do `keyring` do sistema operacional,
no serviço `bot_cursos`. Cadastre o token do bot e o ID do canal:

```bash
python -c "import keyring; keyring.set_password('bot_cursos', 'token', 'SEU_TOKEN_DO_DISCORD')"
python -c "import keyring; keyring.set_password('bot_cursos', 'channel', 'ID_DO_CANAL')"
```

O bot precisa estar em um servidor do Discord com permissão para enviar mensagens
no canal informado.

## Execução

```bash
python main.py
```

## Como adicionar uma nova plataforma

1. Crie `engines/<plataforma>.py` com uma função `async def get_<plataforma>_courses() -> list`
   que devolva uma lista de listas (o primeiro item é o identificador do curso).
2. Se o formato da mensagem for `[título, link]`, reaproveite `format_simple_course`;
   caso contrário, escreva um novo formatador em `main.py`.
3. Adicione a dupla `(coletor, formatador)` em `COURSE_SOURCES`.

## Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE).
