import os
import asyncio
import json
from random import choice
from typing import List

import aiohttp
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


async def get_response(link: str) -> list | None:
    '''
    Function returns list object from provided link

    :param link : any http/https link
    :type link : str
    :returns : raw html object
    :rtype : html.HtmlElement | None
    '''
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=link,
            proxy=PROXY,
            headers={'user-agent': HEADERS['user_agents'][0]} if HEADERS else {}
        ) as response:
            if response.status != 200:
                print(response, response.status, sep='\n')
                return None
            content = await response.json()
            return content


async def get_data_from_opendota():
    '''
    Function collects data from opendota and save in data.json file
    '''
    with open('backend/config/opendota_links.json', 'r', encoding='utf-8') as link_file:
        opendota_link = json.load(link_file)

    teams = await get_response(opendota_link['link'])

    with open('backend/config/data.json', 'w', encoding='utf-8') as record_file:
        json.dump(teams['rows'], record_file, indent=4)


# asyncio.run(get_data_from_opendota())
