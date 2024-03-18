import os
import asyncio
import json
from random import choice
from typing import List

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

async def get_teams(dotabuff_link: str) -> List[dict]:
    '''
    Function returns top-21 dota 2 pro teams

    :param dotabuff_link : link on dotabuff team list
    :type dotabuff_link : str
    :returns : dotabuff top-21 team list with links
    :rtype : List[{'name': str, 'dotabuff_link': str},]
    '''
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=dotabuff_link,
            proxy=PROXY,
            headers={'user-agent': choice(HEADERS['user_agents'])} if HEADERS else {}
        ) as response:
            if response.status != 200:
                return []
            content = await response.text()
            tree: html.HtmlElement = html.fromstring(content)
            team_links: List[str] = tree.xpath('//*[@id="teams-all"]/table/tbody/tr/td[2]/a')
            teams: List[dict] = []
            for team in team_links[:21]:
                teams.append(
                    {
                        'name': team.text_content(),
                        'dotabuff_link': 'https://www.dotabuff.com' + team.get('href')
                    }
                )
            return teams


async def get_players(dotabuff_link: str) -> List[dict]:
    '''
    Function returns dotabuff team players with links and status

    :param dotabuff_link : link on dotabuff team
    :type dotabuff_link : str
    :returns : dotabuff player list with links
    :rtype : List[{'name': str, 'dotabuff_link': str, 'is_active': bool},]
    '''
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=dotabuff_link,
            proxy=PROXY,
            headers={'user-agent': choice(HEADERS['user_agents'])} if HEADERS else {}
        ) as response:
            if response.status != 200:
                return []
            content = await response.text()
            tree: html.HtmlElement = html.fromstring(content)
            player_links: List[str] = tree.xpath(
                '/html/body/div[2]/div[2]/div[3]/div[5]/div[1]/div[1]/' \
                    'section[1]/article/div/table/tbody/tr/td[2]'
            )
            players: List[dict] = []
            for player in player_links:
                is_active = player.xpath('small/acronym')
                players.append(
                    {
                        'name': player.xpath('a[2]')[0].text_content(),
                        'dotabuff_link': 'https://www.dotabuff.com' \
                            + player.xpath('a[2]')[0].get('href'),
                        'is_active': (is_active[0].text_content() == 'Active') \
                            if is_active else 0,
                    }
                )
            print(players)
            return players
        

async def get_player(dotabuff_link: str) -> List[dict]:
    '''
    Function returns dotabuff team players with links and status

    :param dotabuff_link : link on dotabuff team
    :type dotabuff_link : str
    :returns : dotabuff player list with links
    :rtype : List[{'hero': str, 'win_percentage': str},]
    '''
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=dotabuff_link,
            proxy=PROXY,
            headers={'user-agent': choice(HEADERS['user_agents'])} if HEADERS else {}
        ) as response:
            if response.status != 200:
                return []
            content = await response.text()
            tree: html.HtmlElement = html.fromstring(content)
            heroes_stats: List[str] = tree.xpath(
                '/html/body/div[2]/div[2]/div[3]/div[5]/div[1]/div[1]/' \
                    'section[1]/article/div/table/tbody/tr'
            )
            heroes: List[dict] = []
            for hero in heroes_stats:
                heroes.append(
                    {
                        'hero': hero.xpath('td[2]/a[2]')[0].text_content(),
                        'win_percentage': hero.xpath('td[4]')[0].text_content(),
                    }
                )
            print(heroes)
            return heroes

# asyncio.run(get_player('https://www.dotabuff.com/esports/players/113331514-miposhka/heroes'))
