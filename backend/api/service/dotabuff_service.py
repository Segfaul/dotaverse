import os
import asyncio
import json
from random import choice

import aiohttp
from lxml import html
from dotenv import load_dotenv

env = os.environ.get
load_dotenv('./.env')

PROXY = env('PROXY')
HEADERS = {
    "user_agents": [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/538 "\
            "(KHTML, like Gecko) Chrome/36 Safari/538",
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 " \
            "(KHTML, like Gecko) Chrome/49.0.2599.0 Safari/537.36"
    ]
}

async def get_team(dotabuff_link: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=dotabuff_link,
            proxy=PROXY,
            headers={'user-agent': choice(HEADERS['user_agents'])} if HEADERS else {}
        ) as response:
            if response.status == 200:
                content = await response.text()
                tree = html.fromstring(content)
                teams = tree.xpath('//*[@id="teams-all"]/table/tbody/tr/td[2]/a')
                print(len([team.get('href') for team in teams[:21]]))
            # return content

# asyncio.run(get_team('https://www.dotabuff.com/esports/teams'))
